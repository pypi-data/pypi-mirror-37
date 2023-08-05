from ktdk.core.tasks import Task


class DirLayoutActions(object):
    def __init__(self, task, source, subdir, destination=None):
        self.source = source
        self.destination = destination or 'workspace'
        self.task = task
        self.subdir = subdir or ''

    def init_task(self, task):
        task.source = self.source
        task.destination = self.destination
        task.subdir = self.subdir
        return task

    def add_task(self, *tasks):
        for task in tasks:
            self.init_task(task)
            self.task.add_task(task)

    def check_that(self, check):
        self.task.check_that(self.init_task(check))

    def require_that(self, check):
        self.task.require_that(self.init_task(check))


class FileTasks(Task):
    def _run(self, *args, **kwargs):
        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = self.name or 'files'

    def workspace(self, subdir=None):
        return DirLayoutActions(task=self, subdir=subdir, source='workspace')

    def submission(self, subdir=None):
        return DirLayoutActions(task=self, subdir=subdir, source='submission')

    def test_files(self, subdir=None):
        return DirLayoutActions(task=self, subdir=subdir, source='test_files')
