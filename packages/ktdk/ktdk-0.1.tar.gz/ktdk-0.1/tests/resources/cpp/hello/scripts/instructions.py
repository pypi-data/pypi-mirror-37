from ktdk.asserts import matchers
from ktdk.asserts.matchers import Equals, IsEmpty
from ktdk.asserts.checks.executable import *
from ktdk.asserts.checks.general import *
from ktdk.core.tests import Test
from ktdk import KTDK

from ktdk.tasks.cpp.cmake import CMakeBuildTask
from ktdk.tasks.cpp.valgrind import ValgrindCommand
from ktdk.tasks.fs.tasks import MakeDir, ExistFiles, CopyFiles
from ktdk.tasks.fs.tools import *
from ktdk.tasks.raw.executable import ExecutableTask


ktdk = KTDK.get_instance()

naostro = Test(name="naostro", desc="Test nanecisto")
ktdk.suite.add_test(naostro)

ft = FileTasks()
ft.workspace('src').add_task(MakeDir())
ft.workspace('results').add_task(MakeDir())
ft.submission('src').require_that(ExistFiles('main.c'))
ft.test_files().require_that(ExistFiles('CMakeLists.txt'))

ft.submission('src').add_task(CopyFiles('*.c'))
ft.test_files().add_task(CopyFiles('CMakeLists.txt'))

ft.workspace('src').check_that(ExistFiles("main.c"))

ktdk.suite.add_task(ft)


cmake = CMakeBuildTask()
cmake.check_that(TestResultCheck(matcher=matchers.ResultPassed()))
ktdk.suite.add_task(cmake)

hello_test = Test(name="hello_test", desc="Super hello test")
hello = ExecutableTask(executable='hello', executor=ValgrindCommand)
hello_test.add_task(hello)


hello.check_that(ReturnCodeMatchesCheck(matcher=Equals(0)))
hello.check_that(StdOutMatchesCheck(matcher=Equals("Hello world!")))
hello.check_that(StdErrMatchesCheck(matcher=IsEmpty()))

naostro.add_test(hello_test)

