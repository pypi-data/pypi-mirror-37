from ktdk.tasks.cpp.cmake import CMakeBuildTask
from tests.utils import get_test_context


def prepare_dir(tmpdir):
    path = tmpdir.mkdir('workspace')
    src = path.mkdir('src')
    c_file = src.join('main.c')
    c_file.write("""
        #include <stdio.h>\n
        int main() { printf("ahoj svet!\\n"); return 0; }
    """)
    cmake_file = src.join('CMakeLists.txt')
    cmake_file.write("""
        add_executable(hello main.c)
    """)
    return path


def create_context(tmpdir):
    config = dict(workspace=prepare_dir(tmpdir))
    return get_test_context(suite_config=config)


def test_cmake_tasks(tmpdir):
    cmake = CMakeBuildTask(source='src')
    context = create_context(tmpdir=tmpdir)
    runner = cmake.runner.get_instance(context=context)
    runner.invoke()
    assert cmake.result.effective.passed
    assert context.config['exec']
