from ktdk.runtime.context import Context
from ktdk.tasks.fs.tasks import *

from ktdk.tasks.fs.tools import FileTasks


def prepare_dir(tmpdir, name):
    path = tmpdir.mkdir(name)
    for i in range(10):
        path.join(f"{name}_{i}.txt").write(f"{name}_{i}")
    return path


def create_context(tmpdir):
    config = dict(gc=0,
                  submission=prepare_dir(tmpdir, 'submission'),
                  workspace=prepare_dir(tmpdir, 'workspace'),
                  test_files=prepare_dir(tmpdir, 'test_files'))
    context = Context(config, {'lc': 0})
    return context


def test_files_copy_tasks(tmpdir):
    ft = FileTasks()
    ft.submission().add_task(CopyFiles('submission*'))
    ft.workspace().add_task(ExistFiles('submission*'))
    context = create_context(tmpdir=tmpdir)
    runner = ft.runner.get_instance(context=context)
    result = runner.invoke()
    assert result


def test_files_exist_tasks(tmpdir):
    ft = FileTasks()
    ft.workspace().add_task(ExistFiles('workspace*'))
    context = create_context(tmpdir=tmpdir)
    runner = ft.runner.get_instance(context=context)
    result = runner.invoke()
    assert result


def test_files_non_exist_tasks(tmpdir):
    ft = FileTasks()
    ft.workspace().check_that(ExistFiles('submission*'))
    context = create_context(tmpdir=tmpdir)
    runner = ft.runner.get_instance(context=context)
    result = runner.invoke()
    assert result


class CheckFoundFilesTask(Task):
    def _run(self, *args, **kwargs):
        self.asserts.check(self.context.config['found_files'], matcher=IsNotNone())


def test_files_find_task(tmpdir):
    ft = FileTasks()
    files = FindFiles('submission*')
    files.check_that(CheckFoundFilesTask())
    ft.workspace().add_task(files)
    context = create_context(tmpdir=tmpdir)
    runner = ft.runner.get_instance(context=context)
    result = runner.invoke()
    assert result
