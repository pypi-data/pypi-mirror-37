import difflib


def get_context_diff(expected, provided, keep_ends=True):
    def _split_string(orig):
        if isinstance(orig, str):
            orig = orig.splitlines(keepends=keep_ends)
        return orig

    expected = _split_string(expected)
    provided = _split_string(provided)
    return difflib.context_diff(expected, provided, fromfile='expected', tofile='provided')
