from ktdk.asserts.utils import get_context_diff


class GeneralMatcher(object):
    def __init__(self, message=None, symbol=None):
        self.message = message
        self._symbol = symbol or '(+)'

    def __call__(self, orig):
        return self.invoke(orig)

    @property
    def symbol(self):
        return self._symbol

    # pylint: disable=no-self-use
    def message_footer(self, orig):
        return f"Provided: {orig}"

    def predicate(self, orig):
        return orig is not None

    def get_object(self, orig):
        return orig

    # pylint: enable=no-self-use

    def generate_message(self, orig):
        full_message = ""
        if self.message:
            full_message += str(self.message) + "\n"
        full_message += self.message_footer(orig) + "\n"
        return full_message

    def invoke(self, orig):
        cond = self.predicate(orig)
        message = self.generate_message(orig)
        obj = self.get_object(orig)
        return cond, obj, message


class GeneralExpectedMatcher(GeneralMatcher):
    def __init__(self, expected, message=None, use_diff=False, symbol=None):
        super().__init__(message=message, symbol=symbol)
        self._use_diff = use_diff
        self.expected = expected

    def obj_message(self, orig):
        return f"{orig} {self.symbol} {self.expected}"

    def generate_message(self, orig):
        return f"{self.obj_message(orig)}\n{self.message_footer(orig)}"

    def message_footer(self, orig):
        if self._use_diff:
            return get_context_diff(expected=self.expected, provided=orig)
        return f"Expected: {self.expected}\nProvided: {orig}"

    def predicate(self, orig):
        return orig == self.expected
