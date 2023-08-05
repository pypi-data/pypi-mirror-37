import pytest

from ktdk.tasks.cpp.compiler import CCompilerTask, RawCompilerTask
from tests.utils import get_test_context


@pytest.fixture
def prepared_dir(tmpdir):
    path = tmpdir.mkdir('workspace')
    src = path.mkdir('src')
    c_file = src.join('main.c')
    c_file.write("""
        #include <stdio.h>\n
        int main() { printf("ahoj svet!\\n"); return 0; }
    """)
    return path


@pytest.fixture
def context(prepared_dir):
    config = dict(workspace=prepared_dir, devel=True, c_compiler='clang')
    return get_test_context(suite_config=config, test_config={})


def test_compile_tasks(context):
    compiler = RawCompilerTask(compiler='gcc', executable='hello', files=['src/main.c'])
    runner = compiler.runner.get_instance(context=context)
    runner.invoke()
    assert compiler.result.effective.passed
    assert context.config['exec']


def test_compile_with_c_compiler_tasks(context):
    compiler = CCompilerTask(executable='hello', files=['src/main.c'])
    runner = compiler.runner.get_instance(context=context)
    runner.invoke()
    assert compiler.result.effective.passed
    assert context.config['exec']
