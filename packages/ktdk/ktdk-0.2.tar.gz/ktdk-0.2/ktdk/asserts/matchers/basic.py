from ktdk.asserts.matchers.general import GeneralExpectedMatcher, GeneralMatcher
from ktdk.asserts.utils import get_context_diff


class IsTrue(GeneralMatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='is')
        self.message = self.message or 'Is not true'

    def predicate(self, orig):
        return orig is True


class IsFalse(GeneralMatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='is')
        self.message = self.message or 'Is not false'

    def predicate(self, orig):
        return orig is False


class Equals(GeneralExpectedMatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='==')
        self.message = self.message or 'Does not equals'

    def predicate(self, orig):
        return orig == self.expected


class NotEquals(GeneralExpectedMatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='!=')
        self.message = self.message or 'Does equals'

    def predicate(self, orig):
        return orig != self.expected


class Greater(GeneralExpectedMatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='>')
        self.message = self.message or 'Is not Greater'

    def predicate(self, orig):
        return orig > self.expected


class Less(GeneralExpectedMatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='<')
        self.message = self.message or 'Is not Less'

    def predicate(self, orig):
        return orig < self.expected


class LessEquals(GeneralExpectedMatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='<=')
        self.message = self.message or 'Is not less equal'

    def predicate(self, orig):
        return orig <= self.expected


class GreaterEquals(GeneralExpectedMatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='>=')
        self.message = self.message or 'Is not greater equal'

    def predicate(self, orig):
        return orig >= self.expected


class IsNone(GeneralMatcher):
    def predicate(self, orig):
        return orig is None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='is None')
        self.message = self.message or 'Is not None'


class IsNotNone(GeneralMatcher):
    def predicate(self, orig):
        return orig is not None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='is not None')
        self.message = self.message or 'Is None'


class Contains(GeneralExpectedMatcher):
    def predicate(self, orig):
        return orig in self.expected

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='in')
        self.message = self.message or 'Does not contains'


class NotContains(GeneralExpectedMatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='not in', message='Does contains')
        self.message = self.message or 'Does contains'

    def predicate(self, orig):
        return orig not in self.expected


class IsNotEmpty(GeneralMatcher):
    def predicate(self, orig):
        return orig

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='is not Empty')
        self.message = self.message or 'Is empty'


class IsEmpty(GeneralMatcher):
    def predicate(self, orig):
        return not orig

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='is Empty')
        self.message = self.message or 'Is not empty'


class Diff(GeneralExpectedMatcher):
    def __init__(self, *args, keep_ends=True, diff_options=None, **kwargs):
        super().__init__(*args, **kwargs, symbol='diff')
        self.message = self.message or 'Diff is not empty - strings are not the same'
        self._diff_opts = diff_options
        self._keep_ends = keep_ends

    def invoke(self, orig):
        compare = get_context_diff(expected=self.expected, provided=orig, keep_ends=self._keep_ends)
        list_cmp = list(compare)
        cond = not list_cmp
        message = "\n" + ''.join(list_cmp)
        obj = self.get_object(orig)
        return cond, obj, message
