from typing import Optional

from ktdk.asserts.checks.general import AbstractMatchesTask


class AbstractStyleResultMatchesTask(AbstractMatchesTask):
    @property
    def style_result(self) -> Optional[str]:
        if not self.context:
            return None
        return self.context.config['tidy_result']


class StyleResultMatchesCheck(AbstractStyleResultMatchesTask):
    def _run(self, *args, **kwargs):
        self.asserts.check(self.style_result, self.matcher)


class ClangTidyResultMatchesCheck(AbstractMatchesTask):
    @property
    def tidy_result(self) -> Optional[str]:
        if not self.context:
            return None
        return self.context.config['tidy_result']

    def _run(self, *args, **kwargs):
        self.asserts.check(self.tidy_result, self.matcher)
