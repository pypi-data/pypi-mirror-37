import logging
import os
import shutil
from pathlib import Path

from ktdk.asserts.matchers import IsNotEmpty, IsNotNone, IsTrue
from ktdk.core.tasks import PipeTask, Task

log = logging.getLogger(__name__)


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        source = os.path.join(src, item)
        destination = os.path.join(dst, item)
        if os.path.isdir(source):
            shutil.copytree(source, destination, symlinks, ignore)
        else:
            shutil.copy2(source, destination)


class FileActionWrapper(object):
    def __init__(self, action, path):
        self.action = action
        self.path = path

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__dict__


class AbstractFilesTask(Task):
    def __init__(self, pattern='', subdir='', from_dir=None, to_dir=None, output_subdir=None,
                 source='submission', destination='workspace',
                 **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.destination = destination
        self.subdir = subdir or ''
        self.output_subdir = output_subdir or ''
        self._from_dir = Path(from_dir) if from_dir is not None else None
        self._to_dir = Path(to_dir) if to_dir is not None else None
        self.pattern = [pattern] if isinstance(pattern, str) else pattern

    @property
    def from_path(self) -> Path:
        if self._from_dir is not None:
            return self._from_dir
        return self.context.dirs.get_dir(self.source) / self.subdir

    @property
    def to_path(self):
        if self._to_dir is not None:
            return self._from_dir
        return self.context.dirs.get_dir(self.destination) / self.subdir / self.output_subdir

    def _glob_files(self, path=None):
        path = path or self.from_path
        found = []
        for pat in self.pattern:
            found += path.glob(pat)
        return found

    def _glob_dirs(self, path=None):
        path = path or self.from_path
        found = []
        if self.pattern:
            for pat in self.pattern:
                found += path.glob(pat)
            return found
        return [path]

    def _process_files(self, subdir='', transform_path=None, action=None, **kwargs):
        found = self._glob_dirs()
        path = self.to_path
        final_dir = path.joinpath(subdir)
        for i in found:
            if transform_path:
                i = transform_path(i)
            final_path = str(final_dir.resolve())
            if final_dir.is_dir():
                final_path += "/"
            if final_dir.exists():
                log.debug(f"[FSM] Manip ({action.__name__}): {i} -> {final_path}")
                self.context.config.add_suite('work_files', [str(i)])
                action(i, final_path, **kwargs)
            else:
                log.error(f"[FILE] Cannot find file path: {final_dir}")


class CopyFiles(AbstractFilesTask):
    def _run(self, *args, **kwargs):
        self._process_files(action=shutil.copy2, **kwargs)


class CopyDir(AbstractFilesTask):
    def _run(self, *args, **kwargs):
        self._process_files(action=copytree, **kwargs)


class MoveFiles(AbstractFilesTask):
    def _run(self, *args, **kwargs):
        self._process_files(action=shutil.move, transform_path=str, **kwargs)


class DeleteFiles(AbstractFilesTask):
    def _run(self, *args, **kwargs):
        files = self._glob_files(path=self.to_path)
        for file_to_delete in files:
            log.debug(f"[DEL] Deleting file: {file_to_delete}")
            file_to_delete.unlink()


class ExistFiles(AbstractFilesTask):
    def _run(self, *args, **kwargs):
        files = self._glob_files(path=self.from_path)
        self.asserts.check(
            files,
            IsNotEmpty(message=f'Files not found! Pattern {self.pattern} in {self.from_path}')
        )
        exist = all(f.exists() for f in files)
        message = f"Not found files for pattern: {self.pattern} in {self.from_path}"
        self.asserts.check(exist, IsTrue(message=message))


class FindFiles(AbstractFilesTask):
    def _run(self, *args, **kwargs):
        files = self._glob_files(path=self.from_path)
        log.debug(f"[FND] Found files ({self.from_path}/{self.pattern}): {files}")
        self.context.config.add_task('found_files', files)
        self.asserts.check(files, IsNotNone(message=f"Cannot find any files: {self.pattern}"))


class MakeDir(AbstractFilesTask):
    def _run(self, *args, **kwargs):
        log.debug(f"[DIR] Create: {self.from_path}")
        self.from_path.mkdir(parents=True, exist_ok=True)


class ProcessFiles(AbstractFilesTask):
    def __init__(self, pattern, action=None, **kwargs):
        super().__init__(pattern, **kwargs)
        self.action = action

    def _run(self, *args, **kwargs):
        self._process_files(action=self.action)


class FileGlobPipeTask(PipeTask):
    def __init__(self, pattern, **kwargs):
        super().__init__(**kwargs)
        self.pattern = pattern

    def pipe_action(self):
        return self.context.paths.workspace.glob(self.pattern)
