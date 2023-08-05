import json
import os
import shutil
from pathlib import Path

import pytest

from ktdk import KTDK, Test
from ktdk.asserts import matchers
from ktdk.asserts.checks import TaskResultCheck
from ktdk.tasks.cpp import CMakeBuildTask, ValgrindCommand, catch
from ktdk.tasks.fs import CopyFiles, ExistFiles, FileTasks, MakeDir
from tests.paths import TEST_RESOURCES_BASE


def create_cmake(src, *names):
    content = """
    cmake_minimum_required (VERSION 3.0)
    project (kontr_tests)
    
    add_compile_options(-std=c++11)
    """
    src = Path(src)
    for name in names:
        content += f"add_executable({name} {name}.cpp)\n"
    cmake_file = src.joinpath('CMakeLists.txt')
    cmake_file.write_text(content)


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
def prepared_sources(submission_dir):
    path = os.path.join(submission_dir, 'src')
    shutil.copytree(str(TEST_RESOURCES_BASE / 'catch'), path)
    create_cmake(path, 'fails')
    return submission_dir


@pytest.fixture
def cmake():
    cmake = CMakeBuildTask(source='src', cwd='src')
    cmake.require_that(TaskResultCheck(matcher=matchers.ResultPassed()))
    return cmake


@pytest.fixture()
def file_tasks():
    ft = FileTasks()
    ft.workspace('src').add_task(MakeDir())
    ft.submission('src').require_that(ExistFiles('fails.cpp'))

    ft.submission('src').add_task(CopyFiles('*.*'))
    ft.submission('src').add_task(CopyFiles('CMakeLists.txt'))
    ft.workspace('src').check_that(ExistFiles("CMakeLists.txt"))
    ft.workspace('src').check_that(ExistFiles("fails.cpp"))
    return ft


@pytest.fixture()
def catch_test():
    catch_test = Test(name="catch_test", desc="Super catch test")
    catch_task = catch.CatchRunTestsOneByOneTask(executable='fails', executor=ValgrindCommand)
    catch_test.add_task(catch_task)
    catch_test.check_that(catch.CatchCheckCasesAndComputePoint(max_points=3), after_tasks=True)
    return catch_test


@pytest.fixture()
def naostro(catch_test):
    naostro = Test(name="naostro", desc="Test nanecisto", tags=['naostro'])
    naostro.add_test(catch_test)
    return naostro


@pytest.fixture()
def ktdk(workspace_dir, test_files_dir, submission_dir, cmake, naostro, file_tasks):
    ktdk = KTDK(
        test_files=test_files_dir,
        submission=submission_dir,
        workspace=workspace_dir,
        devel=True
    )
    ktdk.suite.add_task(file_tasks)
    ktdk.suite.add_task(cmake)
    ktdk.suite.add_test(naostro)
    return ktdk


def test_catch_run(prepared_sources, ktdk):
    ktdk.invoke()
    assert ktdk.suite.result.effective.failed
    assert round(ktdk.suite.result.effective_points, 2) == 2.14
