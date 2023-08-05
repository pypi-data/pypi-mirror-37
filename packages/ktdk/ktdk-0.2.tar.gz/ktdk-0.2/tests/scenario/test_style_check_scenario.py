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


@pytest.fixture(autouse=True)
def prepared_sources(workspace_dir):
    path = os.path.join(workspace_dir, 'src')
    shutil.copytree(str(TEST_RESOURCES_BASE / 'cpp' / 'checkstyle'), path)
    create_cmake(path, 'correct', 'fail_format', 'fail_tidy')
    return workspace_dir


@pytest.fixture()
def scenario(prepared_sources):
    return scenarios.StyleCheckScenario(checkstyle_points=3, tidy_points=1,
                                        files_glob="src/*.cpp", headers=["src/meta.h"])


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


def test_checkstyle_scenario(ktdk):
    ktdk.invoke()
    assert ktdk.suite.result.effective.failed
    assert ktdk.stats['final_points'] == 1
