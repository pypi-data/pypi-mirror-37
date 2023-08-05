from typing import List

import ktdk.tasks.cpp.checkstyle as cpp_style
from ktdk import Test
from ktdk.asserts.checks import ClangTidyResultMatchesCheck, StyleResultMatchesCheck
from ktdk.asserts.matchers import IsEmpty, StdoutIsEmpty
from ktdk.scenarios import scenario


class StyleCheckScenario(scenario.Scenario):
    def __init__(self, files=None, headers=None, files_glob=None,
                 checkstyle_points=0, tidy_points=0, style=None,
                 clang_tidy_klass=cpp_style.CPPClangTidyCheckStyle, **kwargs):
        super().__init__(**kwargs)
        self._files = files
        self._headers = headers
        self._files_glob = files_glob
        self._checkstyle_points = checkstyle_points
        self._tidy_points = tidy_points
        self._clang_tidy_klass = clang_tidy_klass
        self._format_style = style

    @property
    def files(self) -> List:
        if self._files:
            return self._files
        else:
            return list(self.context.paths.workspace.glob(self._files_glob))

    def run_clang_tidy(self, files: list = None):
        files = files or self.files
        tidy_test = Test(name="clang_tidy", desc="Clang Tidy test for given files",
                         points=self._tidy_points)
        tidy_task = self._clang_tidy_klass(files=files, headers=self._headers)
        tidy_task.check_that(ClangTidyResultMatchesCheck(matcher=StdoutIsEmpty()))
        tidy_test.add_task(tidy_task)
        self.test.add_test(tidy_test)

    def run_clang_format_test(self, file, points: float = 0):
        format_test = Test(name="clang_format", desc=f"Clang format tests for {file.name}",
                           points=points)
        self.test.add_test(format_test)
        format_task = cpp_style.ClangFormatTask(file=file, style=self._format_style)
        format_task.check_that(StyleResultMatchesCheck(matcher=IsEmpty()))
        format_test.add_task(format_task)

    def _run(self, *args, **kwargs):
        self.run_clang_tidy()
        files = self.files
        files_count = len(files)
        part = self._checkstyle_points / files_count
        for file in files:
            self.run_clang_format_test(file, points=part)
