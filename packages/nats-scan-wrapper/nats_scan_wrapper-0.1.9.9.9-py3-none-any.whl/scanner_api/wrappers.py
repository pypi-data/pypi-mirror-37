import asyncio
from queue import Queue
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import logging
import traceback
import nats.aio.client
from nats.aio.errors import ErrTimeout
import json
import socket
from datetime import datetime, timezone
from dateutil import parser
from .errors import *
from .modes import function_mode_old, process_mode
from ._version import __version__

logging.basicConfig(
    format=u'%(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.INFO
)


class scanner_wrapper:
    non_json_serializable_fields = (
        "tls",
        "worker_function",
        "input_handler",
        "output_handler",
        "mode"
    )
    config = {
        # This args more important
        "tls": None,
        "worker_function": None,
        # Return array of args for process. Calling: input_handler(data, meta)
        "input_handler": None,
        # Processing lines from process. Return array with results. Calling: output_handler(line)
        # Line - not decoded
        "output_handler": None,
        # Set in\out or do not use it. Set fields which needs to start
        "fields_in": [],
        "fields_out": [],
        # TODO login password etc
        # FLAGS --------------
        "send_meta": True,
        # each result from array will be sended directly to NATS
        "send_raw": False,
        # output handler must take array with lines if chunked_send not True
        # collect all output of module and send to your handler function
        "chunked_send": False,
        # result must be DICT! and then its added to previous
        "add_result_to_data": False,
        # Process lines or bytes
        "readline": False,
        # print out stderr from procee or not
        "print_stderr": False,
        # receive only one message or all from NATS queue
        "one_message_receive": True,
        # message pack counter
        "receive_messages_count": 50,
        # the next word in pipeline put into worker as arg
        "pipeline_arg": False,
        # module registration in webAPI
        "registration": True,
        "mode": None,
    }
    # when you subscribes to two queues may been created two processes
    # control that with semaphore
    sem = asyncio.Semaphore(1)

    def __init__(self, **kwargs):
        if "name" not in kwargs:
            raise ModuleNameError()

        self.nc = nats.aio.client.Client()
        self.config.update(kwargs)

        self.config["hostname"] = socket.gethostname()
        if self.config["hostname"] == "":
            raise NoHostnameError()

    async def nats_report_publisher(self, **kwargs):
        """
        Send all kwargs in data package to reporter. If results_array in kwargs pop and send each result.
        :param meta: meta info from nats
        :param result_array: each of result will be sent to nats
        :param kwargs: args sents too
        """

        data = {
            "worker_name": self.config["name"],
            "worker_unique_name": self.config["unique_name"],
            "library_version": __version__,
        }
        results_array = None
        if 'results_array' in kwargs:
            results_array = kwargs.pop('results_array')

        for key, value in kwargs.items():
            data[key] = value

        if results_array:
            for result in results_array:
                data['results'] = result
                await self.nc.publish("_reporter", json.dumps(data).encode())
        else:
            await self.nc.publish("_reporter", json.dumps(data).encode())

    async def subscribe_on_one_msg(self, name, queue, callback):
        """
        Subscrbe to NATS for only one message
        :param name:
        :param queue:
        :param callback:
        :return: sid
        """
        sid = await self.nc.subscribe(name, queue, cb=callback, is_async=True)
        await self.nc.auto_unsubscribe(sid, 1)
        return sid

    @staticmethod
    def task_time_is_expired(meta):
        if meta["start_time"]:
            start_time = parser.parse(meta["start_time"])
            return (datetime.now(timezone.utc) - start_time).seconds > int(meta["max_working_time"])
        return False

    async def _run(self, loop):
        async def disconnected_cb():
            logging.info("Got disconnected!")

        async def reconnected_cb():
            # See who we are connected to on reconnect.
            logging.info("Got reconnected to " +
                         str(self.nc.connected_url.netloc))

        async def error_cb(e):
            logging.error("There was an error: " + traceback.format_exc())

        async def closed_cb():
            logging.info("Connection is closed")

        async def connect():
            """

            :return:
            """
            while not self.nc.is_connected:
                try:
                    await self.nc.connect(**options)
                    logging.info("Connected to NATS %s.", self.nc.connected_url.netloc)
                    # logging.info("Subscribe to: '%s', '%s', '%s'", self.config["name"],
                    #              self.config["name"] + self.config["hostname"], self.config["name"] + ".>")
                except nats.aio.client.ErrNoServers as e:
                    logging.error("Could not connect to any server in cluster.")
                    logging.error(traceback.format_exc())

        async def message_handler(msg):
            """Create another process from args send output to output_handler(output_line)
            and then calling result_publisher
            """
            with (await self.sem):
                status = None
                status_detail = None
                cur_pipeline = msg.subject
                try:
                    data = json.loads(msg.data.decode())

                    logging.info("Received from '%s':", cur_pipeline)
                    logging.info("Data: '%s'", data)

                    # Task begin report
                    if self.config["send_meta"]:
                        await self.nats_report_publisher(
                            status="begin",
                            databox_id=data['databox_id']
                        )
                        logging.info("Begin report has been sended.")
                        # Fix no time for send. Swap context to await.
                        await asyncio.sleep(0)

                    try:
                        if not self.config["mode"]:
                            if self.config["worker_function"]:
                                await function_mode_old(self, data)
                            elif self.config["input_handler"] and self.config["output_handler"]:
                                await process_mode(self, data)
                            else:
                                raise NotEnoughArgsError()
                        else:
                            await self.config["mode"](self, data, loop)

                    except NotEnoughArgsError as e:
                        raise NotEnoughArgsError()

                    except BadPackageDataError as e:
                        status = "error"
                        status_detail = "Bad Package"
                        logging.error("Bad Package")

                    except Exception as e:
                        status = "error"
                        status_detail = "Bad Worker"
                        logging.error(
                            "Exception in worker! Report will be sended!")
                        logging.error(traceback.format_exc())

                    # Task end report
                    if status:
                        if self.config["send_meta"]:
                            await self.nats_report_publisher(
                                status=status,
                                status_detail=status_detail,
                                databox_id=data['databox_id']
                            )
                            logging.info("Error status report has been sended.")

                    if self.config["send_meta"]:
                        await self.nats_report_publisher(
                            status="end",
                            databox_id=data['databox_id']
                        )
                        logging.info("End report has been sended.")

                except Exception as e:
                    logging.error("Unexpected exception in main logic!!!")
                    logging.error(traceback.format_exc())

                if self.config["one_message_receive"]:
                    # resub on one message mechanism
                    pipes = cur_pipeline.split(".")
                    resub_pipeline = pipes[0]
                    resub_queue = pipes[0]
                    if len(pipes) > 1:
                        resub_pipeline = self.config["name"] + ".>"
                        resub_queue = self.config["name"]
                    await self.subscribe_on_one_msg(
                        resub_pipeline,
                        resub_queue,
                        message_handler
                    )

        async def subscribe(name, unique_name, one_message_receive):
            """
            Subscribe to NATS channels:
                name
                name.>
                unique_name
            on one message or message flow
            :param name: string `masscan`
            :param unique_name: string `lkhkbjn`
            :param one_message_receive: bool default `True`
            :return:
            """
            logging.debug("Subscribe function called: (name: %s, unique_name: %s, one_message_receive: %s)", name,
                          unique_name, one_message_receive)
            if one_message_receive:
                await self.subscribe_on_one_msg(
                    name,
                    name,
                    message_handler
                )
                await self.subscribe_on_one_msg(
                    name + ".>",
                    name,
                    message_handler
                )
                await self.subscribe_on_one_msg(
                    unique_name,
                    unique_name,
                    message_handler
                )
            else:
                await self.nc.subscribe(
                    name,
                    name,
                    cb=message_handler,
                    # is_async=True,
                    pending_msgs_limit=self.config["receive_messages_count"]
                )
                await self.nc.subscribe(
                    name + ".>",
                    name,
                    cb=message_handler,
                    # is_async=True,
                    pending_msgs_limit=self.config["receive_messages_count"]
                )
                await self.nc.subscribe(
                    unique_name,
                    unique_name,
                    cb=message_handler,
                    # is_async=True,
                    pending_msgs_limit=self.config["receive_messages_count"]
                )
            logging.info("Subscribe to %s, %s, %s", name, name + ".>", unique_name)

        # Configuring nats
        options = {
            # Setup pool of servers from a NATS cluster.
            "servers": self.config['nats'],
            "tls": self.config['tls'],
            "name": self.config['name'],
            "io_loop": loop,
            # Will try to connect to servers in order of configuration,
            # by defaults it connect to one in the pool randomly.
            "dont_randomize": True,
            # Optionally set reconnect wait and max reconnect attempts.
            # This example means 10 seconds total per backend.
            # Next two lines configure client to try to reconnect approximately 7 days ( 8960 * 10 )- 7 days in seconds
            "max_reconnect_attempts": 8960,
            "reconnect_time_wait": 3,
            # Setup callbacks to be notified on disconnects and reconnects
            "disconnected_cb": disconnected_cb,
            "reconnected_cb": reconnected_cb,
            # Setup callbacks to be notified when there is an error
            # or connection is closed.
            "error_cb": error_cb,
            "closed_cb": closed_cb,
        }

        logging.info("Started module named '{name}'.".format(name=self.config["name"]))
        logging.info("Nats module wrapper. Version '%s'", __version__)
        await connect()

        if self.nc.is_connected:
            # register request
            self.config["unique_name"] = self.config["name"] + self.config["hostname"]
            if self.config["registration"]:
                while True:
                    try:
                        # register_data = json.dumps({key: value for key, value in self.config.items() if
                        #                             key not in self.non_json_serializable_fields})
                        register_data = json.dumps({"hostname": self.config["hostname"], "type": self.config["name"]})
                        register_response = await self.nc.request("_registration", register_data.encode(), 1)
                        register_response = json.loads(register_response.data.decode())
                        self.config["unique_name"] = register_response["unique_hostname"]
                        logging.info("Module registered! Module unique_name is: %s", self.config["unique_name"])
                        break
                    except ErrTimeout:
                        logging.warning("Module registration is not possible! The registrar is not responding.")
                    await asyncio.sleep(10, loop=loop)

                options["name"] = self.config["unique_name"]

                logging.info("Module will be reconnected to change name!")
                await self.nc.close()
                await connect()

            await subscribe(self.config["name"], self.config["unique_name"], self.config["one_message_receive"])

            while True:
                if not self.nc.is_connected:
                    await self.nc.close()
                    await connect()
                    await subscribe(self.config["name"], self.config["unique_name"], self.config["one_message_receive"])
                await asyncio.sleep(5, loop=loop)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run(loop))
        loop.close()


class queue_worker_wrapper:
    config = {
        # This args more important
        "tls": None,
        "worker_function": None,
        # Set in\out or do not use it. Set fields which needs to start
        "fields_in": [],
        "fields_out": [],
        # TODO login password etc
        # FLAGS --------------
        "name": None,
        "unique_name": None,
        "hostname": None,
        "max_queue_size": 100,
        "one_message_receive": False,
        "receive_messages_count": 100
    }
    non_json_serializable_fields = ('tls', 'worker_function')
    required_fields = ('name', 'worker_function', 'fields_in', 'fields_out')

    def __init__(self, **kwargs):
        not_spec_args = self.required_fields - kwargs.keys()
        if not_spec_args:
            raise RequiredArgsNotSpecified(not_spec_args)

        self.config.update(kwargs)

        if self.config["hostname"] is None:
            hostname = socket.gethostname()
            if hostname == "":
                raise NoHostnameError()
            self.config["hostname"] = hostname

        self.nc = nats.aio.client.Client()

        # Infinity queues
        self.tasks_queue = Queue(maxsize=0)

        cpu_count = multiprocessing.cpu_count()

        self.pool = ThreadPoolExecutor(max_workers=cpu_count)
        self.loop = asyncio.get_event_loop()

    async def _run(self):
        async def disconnected_cb():
            """
            Disconnect callback. Implement him!
            :return:
            """
            logging.info("Got disconnected!")

        async def reconnected_cb():
            """
            Reconnect callback. Implement him!
            :return:
            """
            logging.info("Got reconnected to " + str(self.nc.connected_url.netloc))

        async def error_cb(e):
            """
            Error callback. Implement him!
            :param e:
            :return:
            """
            logging.error("There was an error: " + traceback.format_exc())

        async def closed_cb():
            """
            Closed connecton callback. Implement him!
            :return:
            """
            logging.info("Connection is closed")

        async def connect(options):
            """
            Connect to nats function
            :return:
            """
            while not self.nc.is_connected:
                try:
                    await self.nc.connect(**options)
                    logging.info("Connected to NATS %s.", self.nc.connected_url.netloc)
                except nats.aio.client.ErrNoServers as e:
                    logging.error("Could not connect to any server in cluster.")
                    logging.error(traceback.format_exc())

        async def _send_nats_reporter_message(msg_dict):
            """
            Here you can define message template
            :param msg_dict: dict with data
            :return:
            """
            await self.nc.publish("_reporter", json.dumps({
                'worker_name': self.config['name'],
                'worker_unique_name': self.config['unique_name'],
                **msg_dict
            }).encode())

        async def send_begin_message(task_data):
            """
            Send to reporter begin message. Reporter send this to Django.
            :param task_data: {'payload': {'hostname': '24REAL.RU'}, 'databox_id': 27894}
            :return:
            """
            await _send_nats_reporter_message({'databox_id': task_data['databox_id'], 'status': 'begin'})

        async def send_end_message(task_data):
            """
            Send to reporter end message. Reporter send this to Django.
            :param task_data: {'payload': {'hostname': '24REAL.RU'}, 'databox_id': 27894}
            :return:
            """
            await _send_nats_reporter_message({'databox_id': task_data['databox_id'], 'status': 'end'})

        async def send_results(task_data):
            """
            Send to reporter message with result. Reporter send this to Django.
            :param task_data: {'payload': {'hostname': '24REAL.RU'}, 'databox_id': 27894, 'results': [{..}, {..}, {..}]}
            :return:
            """
            for result in task_data['results']:
                await _send_nats_reporter_message({
                    'databox_id': task_data['databox_id'],
                    'status': 'results',
                    'results': result,
                    'payload': task_data['payload']
                })

        async def send_queue_overflow_warning(size):
            """
            Send warning message to reporter. Reporter send this to Django. You can use this for scale.
            :param size: current size of task queue
            :return:
            """
            await self.nc.publish("_reporter_warnings", json.dumps({
                'worker_name': self.config['name'],
                'worker_unique_name': self.config['unique_name'],
                'queue_size': size,
                'max_queue_size': self.config['max_queue_size']
            }).encode())

        async def message_handler_queuer(msg):
            # DECODE DATA
            try:
                task_data = json.loads(msg.data.decode())
                logging.info("Received: %s", task_data)
            except Exception as e:
                logging.error("Receive strange message, from another islands! (Not decode to json)")
                logging.error("Data: %s Subject: %s Reply: %s", msg.data.decode(), msg.subject, msg.reply)
                return
            # SEND BEGIN MESSAGE
            try:
                await send_begin_message(task_data)
            except Exception as e:
                logging.error("Task data can't decode to send begin: %s", task_data)
                return

            # ADD TO QUEUE
            self.tasks_queue.put(task_data)

            size = self.tasks_queue.qsize()

            if size > self.config["max_queue_size"]:
                await send_queue_overflow_warning(size)

        def worker_handler(task_data):
            """
            Make work here
            :param task_data: {'payload': {'hostname': '24REAL.RU'}, 'databox_id': 27894}
            :return: task_data: {'payload': {'hostname': '24REAL.RU'}, 'databox_id': 27894, 'results': [{}, {}, {}]}
            """
            try:
                results = self.config['worker_function'](task_data['payload'])
            except Exception:
                logging.error("Exception in worker_function")
                logging.error(traceback.format_exc())

            if type(results) is not list:
                results = [results]

            task_data['results'] = results
            return task_data

        options = {
            # Setup pool of servers from a NATS cluster.
            "servers": self.config['nats'],
            # Set TLS context
            "tls": self.config['tls'],
            # Set name
            "name": self.config['name'],
            "io_loop": self.loop,
            # Will try to connect to servers in order of configuration,
            # by defaults it connect to one in the pool randomly.
            "dont_randomize": True,
            # Optionally set reconnect wait and max reconnect attempts.
            # This example means 3 seconds total per backend.
            # Next two lines configure client to try to reconnect approximately 3 days ( 8960 * 3 )- 3 days in seconds
            "max_reconnect_attempts": 8960,
            "reconnect_time_wait": 3,
            # Setup callbacks to be notified on disconnects and reconnects
            "disconnected_cb": disconnected_cb,
            "reconnected_cb": reconnected_cb,
            # Setup callbacks to be notified when there is an error
            # or connection is closed.
            "error_cb": error_cb,
            "closed_cb": closed_cb,
        }

        await connect(options)

        if self.nc.is_connected:
            for i in range(5):
                # TODO REMOVE THIS
                self.config["unique_name"] = 'hl_test01'
                break
                try:
                    # register_data = json.dumps({key: value for key, value in self.config.items() if
                    #                             key not in self.non_json_serializable_fields})
                    register_data = json.dumps({"hostname": self.config["hostname"], "type": self.config["name"]})

                    register_response = await self.nc.request("_registration", register_data.encode(), 1)

                    register_response = json.loads(register_response.data.decode())
                    self.config["unique_name"] = register_response["unique_hostname"]
                    logging.info("Module registered! Module unique_name is: %s", self.config["unique_name"])
                    break
                except ErrTimeout:
                    logging.warning("Module registration is not possible! The registrar is not responding.")
                await asyncio.sleep(10, loop=self.loop)
            options["name"] = self.config["unique_name"]

            logging.info("Module will be reconnected to change name!")
            await self.nc.close()
            await connect(options)

            await self.nc.subscribe(
                self.config["unique_name"],
                self.config["unique_name"],
                cb=message_handler_queuer,
                is_async=True
            )
            await self.nc.subscribe(
                self.config["name"],
                self.config["name"],
                cb=message_handler_queuer,
                is_async=True
            )

        while True:
            if not self.nc.is_connected:
                await self.nc.close()
                await connect(options)
                await self.nc.subscribe(
                    self.config["unique_name"],
                    self.config["unique_name"],
                    cb=message_handler_queuer,
                    is_async=True
                )
                await self.nc.subscribe(
                    self.config["name"],
                    self.config["name"],
                    cb=message_handler_queuer,
                    is_async=True
                )
            while not self.tasks_queue.empty():
                try:
                    task_data = await self.loop.run_in_executor(self.pool, worker_handler, self.tasks_queue.get())
                    await send_results(task_data)
                    await send_end_message(task_data)
                except Exception as e:
                    logging.error("Error in main logic")
                    logging.error(traceback.format_exc())

            await asyncio.sleep(1, loop=self.loop)

    def run(self):
        self.loop.run_until_complete(self._run())
        self.loop.close()
