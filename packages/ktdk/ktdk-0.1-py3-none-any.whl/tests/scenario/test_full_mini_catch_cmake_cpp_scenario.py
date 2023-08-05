import os
import shutil
from pathlib import Path

import pytest

from ktdk import KTDK, scenarios
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
    create_cmake(path, 'fails', 'tests')
    return submission_dir


@pytest.fixture()
def scenario(prepared_sources):
    return scenarios.CppMiniCatchCmakeFullScenario(executables=['tests'], points=3,
                                                   student_files=['src/*.*'])


@pytest.fixture()
def fail_scenario(prepared_sources):
    return scenarios.CppMiniCatchCmakeFullScenario(executables=['fails'], points=3,
                                                   student_files=['src/*.*'])


@pytest.fixture()
def both_scenario(prepared_sources):
    return scenarios.CppMiniCatchCmakeFullScenario(executables=['fails', 'tests'], points=3,
                                                   student_files=['src/*.*'])


@pytest.fixture()
def ktdk_instance(test_files_dir, workspace_dir, submission_dir):
    return KTDK(
        test_files=test_files_dir,
        submission=submission_dir,
        workspace=workspace_dir,
        devel=True
    )


@pytest.fixture()
def ktdk(scenario, ktdk_instance):
    ktdk_instance.suite.add_task(scenario)
    return ktdk_instance


@pytest.fixture()
def fail_ktdk(fail_scenario, ktdk_instance):
    ktdk_instance.suite.add_task(fail_scenario)
    return ktdk_instance


@pytest.fixture()
def both_ktdk(both_scenario, ktdk_instance):
    ktdk_instance.suite.add_task(both_scenario)
    return ktdk_instance


def test_passing_scenario(ktdk):
    ktdk.invoke()
    assert ktdk.suite.result.effective.passed
    assert round(ktdk.suite.result.effective_points, 3) == 3


def test_failing_scenario(fail_ktdk):
    fail_ktdk.invoke()
    assert fail_ktdk.suite.result.effective.failed
    assert round(fail_ktdk.suite.result.effective_points, 3) == 2.143


def test_both_scenario(both_ktdk):
    both_ktdk.invoke()
    assert both_ktdk.suite.result.effective.failed
    assert round(both_ktdk.suite.result.effective_points, 3) == 2.571
