import os
import shutil
import subprocess

import pytest

from ktdk import Test
from ktdk.tasks.cpp.catch import CatchRunTestsOneByOneTask
from ktdk.utils.flatters import flatten_tests
from tests.paths import TEST_RESOURCES_BASE
from tests.utils import get_test_context


def prepare_and_build(path):
    old_dir = os.getcwd()
    os.chdir(path)
    subprocess.run(['clang++', '-std=c++14', '-o', 'tests', 'tests.cpp'])
    subprocess.run(['clang++', '-std=c++14', '-o', 'fails', 'fails.cpp'])
    os.chdir(old_dir)
    return path


@pytest.fixture
def prepared_dir(tmpdir):
    path = tmpdir.mkdir('workspace')
    path = os.path.join(path, 'build')
    shutil.copytree(str(TEST_RESOURCES_BASE / 'catch'), path)
    return prepare_and_build(path)


@pytest.fixture
def context(prepared_dir):
    config = dict(workspace=prepared_dir)
    pass_path = os.path.join(prepared_dir, 'tests')
    fail_path = os.path.join(prepared_dir, 'fails')
    test_config = dict(exec={'tests': pass_path, 'fails': fail_path})
    return get_test_context(suite_config=config, test_config=test_config)


@pytest.fixture()
def task(context):
    return CatchRunTestsOneByOneTask(executable='tests')


@pytest.fixture()
def fail_task(context):
    return CatchRunTestsOneByOneTask(executable='fails')


@pytest.fixture()
def test(context, task) -> Test:
    test = Test(name='test_task')
    test.add_task(task)
    return test


@pytest.fixture()
def fail_test(context, fail_task) -> Test:
    test = Test(name='test_task')
    test.add_task(fail_task)
    return test


def test_catch_one_by_one_task(context, test, task):
    runner = test.runner.get_instance(context=context)
    runner.invoke()
    assert test.result.effective.passed
    assert test.tests
    for t in flatten_tests(test, include_self=False):
        test_suite = t.context.config['xunit_suite']
        assert test_suite
        assert test_suite.errors == 0
        assert test_suite.failures == 0


def test_catch_failed_task(context, fail_task, fail_test):
    test = fail_test

    runner = test.runner.get_instance(context=context)
    runner.invoke()
    assert test.result.effective.failed
    assert test.tests
