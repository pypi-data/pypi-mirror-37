"""Задача каждого mode принять decode_data пришедших из NATS,
отработать с помощью ползовательских функций, и вернуть массив с результатами
TODO запускать функцию workera в отдельном процессе
"""

import asyncio
import logging


async def process_mode(context, data):
    line_buffer = []
    # User input_handler here, you can set this args
    args = context.config["input_handler"](data['payload'])

    another_args = {}
    if not context.config["print_stderr"]:
        another_args["stderr"] = asyncio.subprocess.DEVNULL

    create = asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        **another_args)
    logging.info("Create process %s", args[0])

    proc = await create

    while True:
        try:
            if context.config["readline"]:
                line = await proc.stdout.readline()
                if line.decode().strip() == "":
                    break
            else:
                line, stderr = await proc.communicate()
                line_buffer.append(line)
                # TODO RM THIS
                break
        except Exception as e:
            print(e, e.with_traceback, e.args)
            break

        logging.info("Process output: '%s'", line)

        if context.config['chunked_send']:
            result_array = context.config["output_handler"](line)
            if type(result_array) is not list:
                result_array = [result_array]

            # logging.info("Result: %s", packages)
            if context.config["send_meta"]:
                await context.nats_report_publisher(
                    results_array=result_array,
                    status="results",
                    databox_id=data['databox_id'],
                    payload=data['payload']
                )

                logging.info("Report has been sended.")

            logging.info("Line processed.")
        else:
            line_buffer.append(line)

    await proc.wait()

    if not context.config['chunked_send']:
        result_array = context.config["output_handler"](line_buffer)
        if type(result_array) is not list:
            result_array = [result_array]

        # logging.info("Result: %s", packages)
        if context.config["send_meta"]:
            await context.nats_report_publisher(
                results_array=result_array,
                status="results",
                databox_id=data['databox_id'],
                payload=data['payload']
            )
            logging.info("Report has been sended.")
        logging.info("Line array processed.")
    logging.info("'%s' completed.", args[0])


async def function_mode_old(context, data):
    logging.info("Starting '%s' worker function.", context.config["name"])
    # Scanning (start function)
    if 'status' in data:
        result_array = context.config["worker_function"](data)
    else:
        result_array = context.config["worker_function"](data['payload'])

    if type(result_array) is not list:
        result_array = [result_array]

    # logging.info("Result: %s", packages)
    if context.config["send_meta"]:
        await context.nats_report_publisher(
            results_array=result_array,
            status="results",
            databox_id=data['databox_id'],
            payload=data['payload']
        )
        logging.info("Report has been sended.")
