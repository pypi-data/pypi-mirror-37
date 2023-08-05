
class KTDKError(RuntimeError):
    pass


class KTDKAssertionError(KTDKError):
    pass


class RequireFailedError(KTDKAssertionError):
    pass


class RequiredTaskFailed(KTDKAssertionError):
    pass


class TaskRunFailed(KTDKError):
    pass
