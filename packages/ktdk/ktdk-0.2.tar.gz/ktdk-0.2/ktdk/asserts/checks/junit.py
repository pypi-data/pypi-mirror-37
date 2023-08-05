import junitparser

from ktdk.asserts.checks.general import AbstractMatchesTask


class AbstractXUnitSuiteCheck(AbstractMatchesTask):
    @property
    def suite(self) -> junitparser.TestSuite:
        return self.context.config['xunit_suite']


class AbstractXUnitCaseCheck(AbstractMatchesTask):
    @property
    def case(self) -> junitparser.TestCase:
        return self.context.config['xunit_case']

class XUnitSuiteFailsCheck(AbstractXUnitSuiteCheck):
    def _run(self, *args, **kwargs):
        self.asserts.check(self.suite.failures, matcher=self.matcher)


class XUnitSuiteErrorsCheck(AbstractXUnitSuiteCheck):
    def _run(self, *args, **kwargs):
        self.asserts.check(self.suite.errors, matcher=self.matcher)


class XUnitSuiteNokCheck(AbstractXUnitSuiteCheck):
    def _run(self, *args, **kwargs):
        noks = self.suite.errors + self.suite.failures
        self.asserts.check(noks, matcher=self.matcher)


class XUnitCaseCheck(AbstractXUnitCaseCheck):
    def _run(self, *args, **kwargs):
        self.asserts.check(self.case.result, matcher=self.matcher)

