class ScanWrapperError(Exception):
    pass


class ModuleNameError(ScanWrapperError):
    def __str__(self):
        return "ScanWrapper: Not set module name in kwargs"


class WorkerError(ScanWrapperError):
    def __str__(self):
        return "ScanWrapper: Error in worker function"


class NotEnoughArgsError(ScanWrapperError):
    def __str__(self):
        return "ScanWrapper: Take me more arguments"


class BadPackageDataError(ScanWrapperError):
    def __str__(self):
        return "ScanWrapper: Data does not match the scanner"


class ExpiredTimeError(ScanWrapperError):
    def __str__(self):
        return "ScanWrapper: Max Task time is expired"


class NoHostnameError(ScanWrapperError):
    def __str__(self):
        return "ScanWrapper: Hostname not provided"


class RequiredArgsNotSpecified(ScanWrapperError):
    def __init__(self, args):
        self.args = args

    def __str__(self):
        return "ScanWrapper: Required arguments are not specified: " + str(self.args)

# class (ScanWrapperError):
#     def __str__(self):
#         return ""
