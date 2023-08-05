import json

import pytest

from ktdk import KTDK
from ktdk.asserts import matchers
from ktdk.asserts.checks.executable import *
from ktdk.asserts.checks.general import *
from ktdk.asserts.checks.style import StyleResultMatchesCheck
from ktdk.asserts.matchers import Equals, IsEmpty
from ktdk.core.tests import Test
from ktdk.tasks.command import Command
from ktdk.tasks.cpp.checkstyle import ClangFormatTask
from ktdk.tasks.cpp.cmake import CMakeBuildTask
from ktdk.tasks.cpp.valgrind import ValgrindCommand
from ktdk.tasks.fs.tasks import CopyFiles, ExistFiles, MakeDir
from ktdk.tasks.fs.tools import *
from ktdk.tasks.raw.executable import ExecutableTask, ValgrindExecutableTask


def create_file(where, name, content=None):
    default = (
        """#include <stdio.h>

int main() {
  printf("Hello %s!\\n");
  return 0;
}""" % name)
    content = content or default
    path = where.join(f'{name}.c')
    path.write(content)
    return path


def create_cmake(src, *names):
    content = """
    cmake_minimum_required (VERSION 3.0)
    project (kontr_tests)
    
    add_compile_options(-std=c99)

    
    """

    for name in names:
        content += f"add_executable({name} {name}.c)\n"
    cmake_file = src.join('CMakeLists.txt')
    cmake_file.write(content)


@pytest.fixture
def workspace_dir(tmpdir):
    workspace = tmpdir.mkdir('workspace')
    return workspace


@pytest.fixture
def test_files_dir(tmpdir):
    test_files = tmpdir.mkdir('test_files')
    return test_files


@pytest.fixture
def submission_dir(tmpdir):
    submission = tmpdir.mkdir('submission')
    return submission


@pytest.fixture()
def sources_dir(submission_dir):
    return submission_dir.mkdir('src')


@pytest.fixture()
def prepared_sources(sources_dir):
    create_file(sources_dir, 'main')
    create_file(sources_dir, 'ahoj')
    create_cmake(sources_dir, 'main', 'ahoj')
    return sources_dir


@pytest.fixture()
def hello_test():
    hello_test = Test(name="hello_test", desc="Super hello test", points=1)
    hello = ExecutableTask(executable='main', executor=Command)
    hello_test.add_task(hello)

    hello.check_that(ReturnCodeMatchesCheck(matcher=Equals(0)))
    hello.check_that(StdOutMatchesCheck(matcher=Equals("Hello main!\n")))
    hello.check_that(StdErrMatchesCheck(matcher=IsEmpty()))
    return hello_test


@pytest.fixture()
def ahoj_test():
    ahoj_test = Test(name="ahoj_test", desc="Super ahoj test", points=1)
    ahoj = ValgrindExecutableTask(executable='ahoj', executor=ValgrindCommand)
    ahoj_test.add_task(ahoj)

    ahoj.check_that(ReturnCodeMatchesCheck(matcher=Equals(0)))
    ahoj.check_that(ValgrindPassedCheck())
    ahoj.check_that(StdOutMatchesCheck(matcher=Equals("Hello ahoj!\n")))
    ahoj.check_that(StdErrMatchesCheck(matcher=IsEmpty()))
    return ahoj_test


@pytest.fixture()
def stylecheck_test():
    style_check_test = Test(name='style_check_test', desc='Style check test', points=0.5)
    clang_format = ClangFormatTask(file='src/main.c', style='Google')
    style_check_test.add_task(clang_format)
    clang_format.check_that(StyleResultMatchesCheck(matcher=IsEmpty()))
    return style_check_test


@pytest.fixture()
def naostro(hello_test, stylecheck_test):
    naostro = Test(name="naostro", desc="Test nanecisto", tags=['naostro'])
    naostro.add_test(hello_test)
    naostro.add_test(stylecheck_test)
    return naostro


@pytest.fixture()
def nanecisto(prepared_sources, ahoj_test):
    nanecisto = Test(name="nanecisto", desc="Test nanecisto", tags=['nanecisto'])
    nanecisto.add_test(ahoj_test)
    return nanecisto


@pytest.fixture()
def file_tasks():
    ft = FileTasks()
    ft.workspace('src').add_task(MakeDir())
    ft.submission('src').require_that(ExistFiles('main.c'))
    ft.submission('src').require_that(ExistFiles('ahoj.c'))

    ft.submission('src').add_task(CopyFiles('*.c'))
    ft.submission('src').add_task(CopyFiles('*.txt'))

    ft.workspace('src').check_that(ExistFiles("main.c"))
    ft.workspace('src').check_that(ExistFiles("ahoj.c"))
    ft.workspace('src').check_that(ExistFiles("CMakeLists.txt"))
    return ft


@pytest.fixture()
def ktdk(workspace_dir, test_files_dir, submission_dir, cmake, nanecisto, naostro, file_tasks):
    ktdk = KTDK(
        test_files=test_files_dir,
        submission=submission_dir,
        workspace=workspace_dir
    )
    ktdk.suite.add_task(file_tasks)
    ktdk.suite.add_task(cmake)
    ktdk.suite.add_test(nanecisto)
    ktdk.suite.add_test(naostro)
    return ktdk


@pytest.fixture
def cmake():
    cmake = CMakeBuildTask(source='src')
    cmake.require_that(TestResultCheck(matcher=matchers.ResultPassed()))
    return cmake


def test_ktdk_run(prepared_sources, ktdk):
    ktdk.invoke()
    assert ktdk.suite.result.effective.passed
    assert ktdk.suite.result.effective_points == 2.5
