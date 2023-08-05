import logging

from ktdk import Task, Test
from ktdk.asserts import checks, matchers
from ktdk.asserts.checks import ReturnCodeMatchesCheck, StdErrMatchesCheck, \
    ValgrindPassedCheck
from ktdk.asserts.matchers import Equals, IsEmpty
from ktdk.tasks.command import Command
from ktdk.tasks.cpp.valgrind import ValgrindCommand
from ktdk.tasks.raw.executable import ExecutableTask
from ktdk.tasks.xunit import junit
from ktdk.utils import flatters, naming

log = logging.getLogger(__name__)


class CatchRunTestsOneByOneTask(Task):
    def __init__(self, executable=None, executor=Command, test_args=None, applied_check=None,
                 **kwargs):
        super().__init__(**kwargs)
        self._executable = executable
        self.executor = executor
        self.applied_check = applied_check
        self._test_args = test_args or []

    @property
    def executable(self):
        return self._executable

    @property
    def command_path(self):
        return self.context.config['exec'][self.executable]

    # https://github.com/catchorg/Catch2/blob/master/docs/command-line.md
    def get_the_tests_list(self):
        result = self.run_only_command(self.command_path, '--list-test-names-only',
                                       executor=Command)
        stdout = result.stdout.content
        return stdout.splitlines()

    def run_one_test_by_name(self, test_name):
        test = Test(name=test_name, desc=test_name)
        params = [*self._test_args, '-r', 'junit', '-n', naming.slugify(test_name), test_name]
        exec_task = self.run_command(self.executable, *params)
        test.add_task(exec_task)
        if self.test is not None:
            self.test.add_test(test)  # Add the newly created test to the test
        return exec_task

    def run_command(self, binary, *params, executor=None):
        executor = executor or self.executor
        task = ExecutableTask(binary, *params, executor=executor)
        return task

    def _run(self, *args, **kwargs):
        tests = self.get_the_tests_list()
        for test_name in tests:
            log.debug(f"[CATCH_RUN] Catch run the test: {test_name}")
            task = self.run_one_test_by_name(test_name=test_name)
            self.process_test_run(task)
            self.check_test_result(task, task.test)

    def run_only_command(self, binary, *params, executor=Command):
        cmd = executor(binary, args=params)
        cmd.set_task(self)
        return cmd.invoke()

    def check_test_result(self, task: Task, test=None):
        test = self.test

        def __default_check(task, test, executor=None):
            task.check_that(ReturnCodeMatchesCheck(matcher=Equals(0)))
            task.check_that(StdErrMatchesCheck(matcher=IsEmpty()))
            if executor == ValgrindCommand:
                task.check_that(ValgrindPassedCheck())

        if self.applied_check is not None:
            return self.applied_check(task, test, self.executor)
        else:
            return __default_check(task=task, test=test, executor=self.executor)

    def process_test_run(self, task):
        log.debug(f"[CATCH] Process and run: {task.test.namespace}")
        task.add_task(_ProcessJUnitTestRunTask())


class _ProcessJUnitTestRunTask(Task):
    def _run(self, *args, **kwargs):
        log.debug(f"[PROC_JUNIT] JUNIT process: {self.test.namespace} ")
        test = self.test
        exec_result = self.context.config['exec_result']
        stdout_path = exec_result.stdout.path
        if stdout_path:
            self.add_task(junit.JUnitParseTask(junit_file=stdout_path))
        return test


class CatchCheckAndComputePoint(Task):
    def __init__(self, max_points=1.0, **kwargs):
        super().__init__(**kwargs)
        self._max_points = max_points

    def _run(self, *args, **kwargs):
        tests = flatters.flatten_tests(self.test, include_self=False)
        num_tests = len(tests)
        for test in tests:
            test.points = self._max_points / num_tests
            test.check_that(checks.XUnitSuiteErrorsCheck(matcher=matchers.Equals(0)))
            test.check_that(checks.XUnitSuiteFailsCheck(matcher=matchers.Equals(0)))
            test.check_that(checks.ValgrindPassedCheck())


class CatchCheckCasesAndComputePoint(Task):
    def __init__(self, max_points=1.0, **kwargs):
        super().__init__(**kwargs)
        self._max_points = max_points

    def _run(self, *args, **kwargs):
        tests = flatters.flatten_tests(self.test, include_self=False)
        tests = [test for test in tests if 'junit_case' in test.tags]
        num_tests = len(tests)
        for test in tests:
            test.points = self._max_points / num_tests
            test.check_that(checks.XUnitCaseCheck(matcher=matchers.Equals(0)))
            test.check_that(checks.ValgrindPassedCheck())
