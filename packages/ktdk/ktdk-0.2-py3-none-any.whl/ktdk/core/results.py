from json import JSONEncoder

from ktdk.utils.basic import BasicObject


class Result(BasicObject, JSONEncoder):
    FAIL = "FAIL"
    ERROR = "ERROR"
    PASS = "PASS"
    SKIP = "SKIP"
    NONE = "NONE"

    def __init__(self, state: str):
        super().__init__()
        self._state = state

    @property
    def state(self):
        return self._state

    @property
    def passed(self):
        return self.state == Result.PASS

    @property
    def ok(self):
        return self.passed or self.state == Result.SKIP

    @property
    def nok(self):
        return not self.ok

    @property
    def errored(self):
        return self.state == Result.ERROR

    @property
    def failed(self):
        return self.state == Result.FAIL

    @property
    def skipped(self):
        return self.state == Result.SKIP

    @property
    def reason(self):
        return f'{self.state}'

    def to_dict(self):
        return {
            "state": self.state,
            "ok": self.ok
            }


PASS = Result(Result.PASS)
ERROR = Result(Result.ERROR)
FAIL = Result(Result.FAIL)
SKIP = Result(Result.SKIP)
NONE = Result(Result.NONE)
