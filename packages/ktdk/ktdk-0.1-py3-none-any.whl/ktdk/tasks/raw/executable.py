import logging

from ktdk.asserts import matchers
from ktdk.tasks.command_task import CommandTask
from ktdk.tasks.cpp.valgrind import ValgrindCommand

log = logging.getLogger(__name__)


class ExecutableTask(CommandTask):
    def __init__(self, executable, *args, **kwargs):
        super().__init__(command=None, args=args, **kwargs)
        self.executable_name = executable

    @property
    def command_path(self):
        executables = self.context.config['exec']
        if not executables:
            log.error(f"[EXEC] Executables has not been found in the context")
        self.asserts.require(executables, matcher=matchers.IsNotNone())
        executable = executables.get(self.executable_name)
        if not executable:
            log.error(f"[EXEC] Executable not exists {self.executable_name}")
        self.asserts.require(executable, matcher=matchers.IsNotNone())
        return executable

    def _run(self, *args, **kwargs):
        result = self.execute()
        self.context.config.set_test('exec_result', result)


class ValgrindExecutableTask(ExecutableTask):
    def __init__(self, executable, *args, executor=ValgrindCommand, **kwargs):
        super().__init__(executable, *args, executor=executor, **kwargs)
