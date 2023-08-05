import logging
import re

from ktdk.asserts import matchers
from ktdk.asserts.matchers import IsNotEmpty
from ktdk.core.tasks import Task
from ktdk.tasks.build_task import BuildTask

log = logging.getLogger(__name__)


class MakeResultParser(BuildTask):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subdir = ''
        self.build_regex = re.compile(r"Built target ([\w\-_\.]+)")

    def _run(self, *args, **kwargs):
        names = self.__parse_b_names()
        log.debug(f"[PRC] Binaries: {names}")
        self.asserts.check(names, IsNotEmpty("Binaries have not been found."))
        executables = {}
        for name in names:
            path = self.target / self.subdir / name
            executables[name] = path
        self.context.config.set_test('exec', executables)

    def __parse_b_names(self):
        names = []
        result = self.context.config['make_result']
        for line in result.stdout.content.splitlines():
            name = self.__parse_b_name(line)
            if name:
                names.append(name)
        return names

    def __parse_b_name(self, line):
        match = self.build_regex.search(line)
        return match.group(1) if match else None


class MakeTask(BuildTask):
    def __init__(self, **kwargs):
        super().__init__(command='make', **kwargs)
        self.args.extend(['-j', '4'])
        self.add_tags('make')

    def process_make(self, result):
        self.asserts.check(result, matchers.CommandOK())
        self.context.config.set_task('make_result', result)
        return result

    def run_make(self):
        result = self.execute()
        return self.process_make(result)

    def _run(self, *args, **kwargs):
        log.debug('[BLD] Make')
        self.move_to_dir(self.target)
        self.run_make()


class CMakeTask(BuildTask):
    def __init__(self, **kwargs):
        super().__init__(command='cmake', **kwargs)
        self.name = self.name or 'cmake'
        self.add_tags('cmake', 'compile')

    def run_cmake(self):
        self.args.append(str(self.source))
        result = self.execute()
        self.asserts.check(result, matchers.CommandOK())

    def _run(self, *args, **kwargs):
        log.debug('[BLD] CMake')
        self.move_to_dir(self.target)
        self.run_cmake()


class CMakeBuildTask(Task):
    def __init__(self, target='', source='', cwd=None, cmake_location=None, **kwargs):
        super().__init__(**kwargs)
        self.target = target
        self.source = source
        self.cmake_location = cmake_location
        self.name = 'cmake_build'
        self.cmake = CMakeTask(target_dir=target, source_dir=source, cwd=cwd)
        self.make = MakeTask(target_dir=target, source_dir=source, cwd=cwd)
        self.make.add_task(MakeResultParser(target_dir=target, source_dir=source))
        self.add_task(self.cmake)
        self.add_task(self.make)
        self._cwd = cwd
