from ktdk import Test
from ktdk.asserts import checks, matchers
from ktdk.scenarios import FullScenario
from ktdk.tasks import fs
from ktdk.tasks.cpp import CMakeBuildTask, ValgrindCommand, catch


class CppMiniCatchCmakeFullScenario(FullScenario):
    def __init__(self, executables=None, points=3, executor=ValgrindCommand,
                 student_files=None, test_files=None, test_per_exec=False, **kwargs):
        super().__init__(**kwargs)
        self.executables = executables
        self.points = points
        self.executor = executor
        self.student_files = student_files or []
        self.test_files = test_files or []
        self._test_per_exec = test_per_exec

    @property
    def compute_points(self) -> catch.CatchCheckCasesAndComputePoint:
        return catch.CatchCheckCasesAndComputePoint(max_points=self.points)

    def catch_task(self, executable: str) -> catch.CatchRunTestsOneByOneTask:
        return catch.CatchRunTestsOneByOneTask(executable=executable, executor=self.executor)

    def file_tasks(self):
        for student in self.student_files:
            self.ft.submission().add_task(fs.CopyFiles(student))
        for test in self.test_files:
            self.ft.test_files().add_task(fs.CopyFiles(test))

    def compile_tasks(self):
        cmake = CMakeBuildTask()
        cmake.require_that(checks.TaskResultCheck(matcher=matchers.ResultPassed()))
        self.root_test.add_task(cmake)
        return cmake

    def run_tasks(self):
        for executable in self.executables:
            test = self.root_test
            if self._test_per_exec:
                test = Test(name=executable, desc=f'Subtest for exec: {executable}')
                self.root_test.add_test(test)
            test.add_task(self.catch_task(executable=executable))

    def evaluate_tasks(self):
        self.root_test.check_that(self.compute_points, after_tasks=True)
