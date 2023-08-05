import re

from ktdk.asserts.checks.general import AbstractExecResultMatchesTask


class ReturnCodeMatchesCheck(AbstractExecResultMatchesTask):
    def _run(self, *args, **kwargs):
        self.asserts.check(self.exec_result.return_code, self.matcher)


class StdOutMatchesCheck(AbstractExecResultMatchesTask):
    def _run(self, *args, **kwargs):
        self.asserts.check(self.exec_result.stdout.content, self.matcher)


class StdErrMatchesCheck(AbstractExecResultMatchesTask):
    def _run(self, *args, **kwargs):
        self.asserts.check(self.exec_result.stderr.content, self.matcher)


class ValgrindPassedCheck(AbstractExecResultMatchesTask):
    REGEX = re.compile(r'ERROR SUMMARY: (\d+) errors')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def points_multiplier(self):
        if self._points_multiplier:
            return self._points_multiplier
        else:
            return self.context.config['valgrind_penalization'] or 0

    @property
    def valgrind_log(self) -> str:
        return self.context.config['valgrind_log']

    def __read_log_content(self):
        valgrind_log = self.valgrind_log
        if valgrind_log is None:
            return None
        valgrind_log = self.context.paths.results / valgrind_log
        with open(valgrind_log, 'r') as content_file:
            return content_file.read()

    def _run(self, *args, **kwargs):
        self.asserts.check(self._asserted_zero_errors(), self.matcher)

    def _asserted_zero_errors(self):
        content = self.__read_log_content()
        if content is None:
            return False
        for line in content.splitlines():
            match = ValgrindPassedCheck.REGEX.search(line)
            if match:
                errors = match.group(1)
                return int(errors) == 0
        return True
