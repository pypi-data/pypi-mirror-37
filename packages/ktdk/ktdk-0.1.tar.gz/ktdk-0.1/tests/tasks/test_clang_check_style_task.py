import pytest

from ktdk.tasks.cpp.checkstyle import ClangFormatTask
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
def context(prepared_dir):
    config = dict(workspace=prepared_dir, devel=True)
    return get_test_context(suite_config=config, test_config={})


def test_clang_check_style_valid_task(context):
    checkstyle = ClangFormatTask(file='main.cpp', style='Google')
    runner = checkstyle.runner.get_instance(context=context)
    runner.invoke()
    assert checkstyle.result.effective.passed
    style_result = context.config['tidy_result']
    assert not style_result
