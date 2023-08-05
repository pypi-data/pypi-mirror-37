import logging
from typing import Union

import junitparser
from junitparser import JUnitXml, TestCase, TestSuite

from ktdk.asserts.checks.general import TaskResultCheck
from ktdk.asserts.matchers import IsNone, ResultPassed
from ktdk.core.tasks import Task
from ktdk.core.tests import Test

log = logging.getLogger(__name__)


class _ProcessTestCaseTask(Task):
    def __init__(self, case: TestCase, **kwargs):
        super().__init__(**kwargs)
        self.case = case

    def _run(self, *args, **kwargs):
        self.asserts.check(self.case.result, matcher=IsNone())
        self.context.config.add_test('xunit_case', self.case)


def create_test(test_case: Union[TestCase, TestSuite], test: Test = None):
    test = Test() if test is None else test
    test.desc = test_case.name
    test.name = test_case.name
    return test


def build_test_case(test_case: TestCase):
    test = create_test(test_case=test_case)
    test.add_tags('junit_case')
    process_task = _ProcessTestCaseTask(test_case)
    process_task.check_that(TaskResultCheck(matcher=ResultPassed()))
    test.add_task(process_task)
    return test


class JUnitParseTask(Task):
    def __init__(self, junit_file=None, **kwargs):
        super().__init__(**kwargs)
        self._junit_file = junit_file
        self._root = None

    @property
    def xml_root(self):
        if self._root is None:
            self._root = JUnitXml.fromfile(self._junit_file)
        return self._root

    def parse_xunit(self):
        for suite in self.xml_root:
            self._handle_suite(suite)

    def _handle_suite(self, suite: TestSuite):
        log.debug(f"[HANDLE] SUITE: {suite}")
        self.add_task(_JUnitRunTheSuite(suite=suite))

    def _run(self, *args, **kwargs):
        log.debug(f"[JUNIT] Parse: {self.test.namespace}")
        return self.parse_xunit()


def _handle_case(test_case: TestCase, suite_test: Test):
    log.debug(f"[XUN] Test Case {test_case.name} [{test_case.result}]: {test_case}")
    case_test = build_test_case(test_case=test_case)
    suite_test.add_test(case_test)
    return suite_test


class _JUnitRunTheSuite(Task):
    def __init__(self, suite=None, **kwargs):
        super().__init__(**kwargs)
        self._suite: junitparser.TestSuite = suite

    @property
    def suite(self) -> junitparser.TestSuite:
        return self._suite

    def _run(self, *args, **kwargs):
        log.debug(f"[XUN] Test Suite {self.suite.name}: {self.suite}")
        self.context.config.set_test('xunit_suite', self.suite)
        suite_test = create_test(self.suite, test=self.test)
        suite_test.add_tags('junit_suite')
        for case in self.suite:
            _handle_case(case, suite_test=suite_test)
        return suite_test
