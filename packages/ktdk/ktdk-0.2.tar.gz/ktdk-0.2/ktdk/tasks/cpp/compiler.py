import logging

from ktdk.asserts.matchers import IsNotEmpty
from ktdk.core.tasks import Task
from ktdk.tasks.build_task import BuildTask
from ktdk.tasks.fs.tasks import FindFiles

log = logging.getLogger(__name__)


class RawCompilerTask(Task):
    class InternalCompilerTask(BuildTask):
        def __init__(self, executable, use_default_options=True, **kwargs):
            super().__init__(**kwargs)
            self.executable = executable
            self._use_default_options = use_default_options

        @property
        def compiler_options(self):
            return self.context.config['cpp_compiler_flags']

        def process_result(self, exec_path):
            self.context.config.add_test('exec', {self.executable: exec_path})

        def run_compile(self):
            found_files = self.context.config['found_files']
            self.asserts.require(found_files, matcher=IsNotEmpty("No input files to compile!"))
            str_files = [str(file_to_str) for file_to_str in found_files]
            build_dir = self.get_build_dir()
            exec_path = build_dir / self.executable
            if self.compiler_options and self._use_default_options:
                self.args.extend(self.compiler_options)
            self.args += ['-o', str(exec_path)]
            self.args += str_files
            self.execute()
            self.process_result(exec_path)

        def get_build_dir(self):
            return self.context.paths.workspace_path('build', create=True)

        def _run(self, *args, **kwargs):
            log.debug('[BLD] Compile')
            self.move_to_dir(self.target)
            self.run_compile()

    def __init__(self, executable, files, compiler=None, use_default_options=True, **kwargs):
        super().__init__(**kwargs)
        self.add_tags('compile')
        self.files = files
        self._compiler = compiler
        self.executable = executable
        self._use_default_options = use_default_options

    @property
    def compiler(self):
        if self._compiler is None:
            self._compiler = self.context.config.get('cpp_compiler')
        return self._compiler

    def _run(self, *args, **kwargs):
        find_files = FindFiles(pattern=self.files, from_dir=self.context.paths.workspace)
        find_files.add_task(RawCompilerTask.InternalCompilerTask(
            command=self.compiler,
            executable=self.executable,
            use_default_options=self._use_default_options
        ))
        self.add_task(find_files)


class CCompilerTask(RawCompilerTask):
    @property
    def compiler_options(self):
        return self.context.config['c_compiler_flags']

    @property
    def compiler(self):
        if self._compiler is None:
            self._compiler = self.context.config.get('c_compiler')
        return self._compiler


class CPPCompilerTask(RawCompilerTask):
    @property
    def compiler(self):
        if self._compiler is None:
            self._compiler = self.context.config.get('cpp_compiler')
        return self._compiler

    @property
    def compiler_options(self):
        return self.context.config['cpp_compiler_flags']
