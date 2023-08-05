from ktdk.asserts import matchers
from ktdk.core.tasks import Task
from ktdk.tasks.command import Command


class CommandTask(Task):
    def __init__(self, command=None, args=None, executor=Command,
                 command_config=None, output_name=None, **kwargs):
        super().__init__(**kwargs)
        self.add_tags('command')
        self.name = self.name or command
        self.executor = executor or Command
        self._cmd = command
        self.command_config = command_config or {}
        self.args = args or []
        self._output_name = output_name

    def build_args(self, *args):
        arr = []
        arr.extend(args)
        arr.extend(self.args)
        return arr

    @property
    def command_path(self):
        return self._cmd

    def command(self):
        path = str(self.command_path)
        args = self.build_args()
        return self.executor(path, args=args, output_name=self._output_name, **self.command_config)

    def execute(self, **kwargs):
        return self.command().set_task(self).invoke(**kwargs)

    def _run(self, *args, **kwargs):
        result = self.execute()
        self.asserts.check(result, matchers.CommandOK())
        self.context.config.set_test('command_result', result)
