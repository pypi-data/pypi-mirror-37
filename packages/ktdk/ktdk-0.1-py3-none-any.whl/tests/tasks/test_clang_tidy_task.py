import pytest

from ktdk.tasks.command import CommandResult
from ktdk.tasks.cpp.checkstyle import CPPClangTidyCheckStyle
from tests.utils import get_test_context


@pytest.fixture
def prepared_dir(tmpdir):
    path = tmpdir.mkdir('workspace')
    c_file = path.join('main.cpp')
    c_file.write(
        """#include <iostream>

int main() {
  std::cout << "ahoj svet!" << std::endl;
  return 0;
}
""")
    return path


@pytest.fixture
def prepared_failing_dir(tmpdir):
    path = tmpdir.mkdir('workspace')
    c_file = path.join('main.cpp')
    c_file.write(
        """#include <iostream>

int main() {
  std::cout << "ahoj svet!" << std::endl;
  char *str = new char[];
  delete str;
  return 0;
}
""")
    return path


@pytest.fixture
def context(prepared_dir):
    config = dict(workspace=prepared_dir, devel=True)
    return get_test_context(suite_config=config, test_config={})


@pytest.fixture
def fail_context(prepared_failing_dir):
    config = dict(workspace=prepared_failing_dir, devel=True)
    return get_test_context(suite_config=config, test_config={})


def test_clang_check_style_valid_task(context):
    tidy = CPPClangTidyCheckStyle(files=['main.cpp'])
    runner = tidy.runner.get_instance(context=context)
    runner.invoke()
    assert tidy.result.effective.passed
    tidy_result: CommandResult = tidy.context.config['tidy_result']
    assert tidy_result
    assert not tidy_result.stdout.bytes


def test_clang_check_style_failing_task(fail_context):
    tidy = CPPClangTidyCheckStyle(files=['main.cpp'])
    runner = tidy.runner.get_instance(context=fail_context)
    runner.invoke()
    assert tidy.result.effective.passed
    tidy_result: CommandResult = tidy.context.config['tidy_result']
    assert tidy_result
    assert tidy_result.stdout.bytes
