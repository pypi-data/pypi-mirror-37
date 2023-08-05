import logging
import os

from ktdk.tasks.command_task import CommandTask

log = logging.getLogger(__name__)


class BuildTask(CommandTask):
    def __init__(self, source_dir=None, target_dir=None, cwd=None, **kwargs):
        super().__init__(**kwargs)
        self._source_dir = source_dir or ''
        self._target_dir = target_dir or 'build'
        self._cwd = cwd
        self.add_tags('build')

    @property
    def source(self):
        return self.base / self._source_dir

    @property
    def base(self):
        return self.context.paths.workspace

    @property
    def target(self):
        return self.base / self._target_dir

    def source_dir(self, source):
        self._source_dir = source
        return self

    def target_dir(self, target):
        self._target_dir = target
        return self

    def __create_dir(self, directory=None, create=True):
        directory = directory or self.target
        if not directory.exists() and create:
            log.debug(f"[DIR] Create: {directory}")
            directory.mkdir(parents=True)

    def move_to_dir(self, directory, create=True):
        self.__create_dir(directory, create=create)
        os.chdir(directory)
