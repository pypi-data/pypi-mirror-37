import logging
import subprocess
from pathlib import Path

from ktdk.utils import naming
from ktdk.utils.basic import BasicObject
from ktdk.utils.naming import unique_suffix

log = logging.getLogger(__name__)


class Command(object):
    def __init__(self, command, args: list = None, output_name=None, task=None, **config):
        """ Creates instance of the command
        Args:
            command(str): Command string
            args(list): Command arguments
            **config: Configuration dictionary
        """
        self.command = str(command)
        self._args = args if args else []
        self.config = {**self.__default_config, **config}
        self._output_name = output_name
        self._unique_suffix = None
        self._task = None

    @property
    def unique_suffix_for_command(self):
        if self._unique_suffix is None:
            self._unique_suffix = unique_suffix(context=self.context)
        return self._unique_suffix

    def output_file_name(self, suffix, name=None):
        """Name with the unique suffix
        Args:
            suffix(str): Suffix
            name(str): Name of the file (default is extracted from command)
        Returns(str): Full name with unique name
        """
        name = name or Path(self.command).name
        if self._output_name:
            name = f"{name}::{self._output_name}"
        name = naming.slugify(name)
        if self.unique_suffix_for_command is not None:
            name = f"{name}_{self.unique_suffix_for_command}"
        if self.task and self.task.test:
            name = self.task.test.namespace + "::" + name
        return name + "." + suffix

    def set_task(self, task):
        """Injects context
        Args:
            task(Task): Context
        """
        self._task = task
        return self

    @property
    def context(self):
        """Gets Context instance
        Returns(Context): Context instance
        """
        if self._task is None:
            return None
        return self._task.context

    @property
    def task(self):
        return self._task

    @property
    def results_path(self):
        """Results path (None if not context)
        Returns(Path): the path to the results
        """
        if not self.context:
            return None
        return self.context.paths.results

    def timeout(self, timeout):
        """Sets timeout
        Args:
            timeout(int): Timeout
        Returns(Command): Command instance
        """
        self.config['timeout'] = timeout
        return self

    def stdin(self, input_stream):
        """Sets stdin
        Args:
            input_stream: Input stream
        Returns(Command): Command instance
        """
        self.config['stdin'] = input_stream
        return self

    def shell(self, shell: bool):
        """Sets whether to use shell
        Args:
            shell(bool): Shell
        Returns(Command): Command instance
        """
        self.config['shell'] = shell
        return self

    def cwd(self, current_working_dir):
        """Sets current working directory
        Args:
            current_working_dir(path): Current working directory path
        Returns(Command): Command instance
        """
        self.config['cwd'] = current_working_dir
        return self

    def check(self, check: bool):
        """Whether to check the command return core
        Args:
            check(bool): Check the command return core
        Returns(Command): Command instance
        """
        self.config['check'] = check
        return self

    def add_args(self, *args):
        """Adds arguments to command
        Args:
            *args: Command arguments
        Returns(Command): Command instance
        """
        self._args.extend(args)
        return self

    def stdout(self, out_stream):
        """Sets the stdout
        Args:
            out_stream: STD Output stream
        Returns(Command): Command instance
        """
        self.config['stdout'] = out_stream
        return self

    def stderr(self, out_stream):
        """Sets the stderr
        Args:
            out_stream: ERR Output stream
        Returns(Command): Command instance
        """
        self.config['stderr'] = out_stream
        return self

    @property
    def args(self):
        """Gets list of the arguments
        Returns(list): List of the arguments
        """
        return self._args

    @property
    def full_command(self):
        """Gets full command with arguments
        Returns(list): Command with arguments
        """
        full = [self.command]
        full.extend([*self.args])
        return full

    @property
    def __default_config(self):
        """Gets default config
        Returns(dict): Returns the dictionary
        """
        return {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "shell": False,
            "cwd": None,
            "timeout": None,
            "check": False,
            "encoding": None,
            "errors": None,
        }

    def invoke(self, **kwargs):
        """Invokes the command
        Returns: Command result
        """
        return self.run(**kwargs)

    def execute(self, **kwargs):
        """Executes the command
         Returns: Command result
         """
        config = {**self.config}
        config.update(**kwargs)
        log.debug(f"[EXE] Command: \"{self.full_command}\" with config: ({config})")
        log.debug(f"[CMD_EXEC] Exec: {' '.join(self.full_command)}")
        try:
            if config['timeout'] is None:
                config['timeout'] = self.context.config['timeout'] if self.context else 60
            return subprocess.run(self.full_command, **config)
        except subprocess.TimeoutExpired as ex:
            log.warning(f"{ex}")
            return ex

    def process(self, result):
        """Process the command
        Args:
            result: Command result
        Returns(CommandResult): Returns the custom command result wrapper
        """
        return CommandResultProcessor(result=result, command=self).process()

    def run(self, **kwargs):
        result = self.execute(**kwargs)
        log.debug(f"[EXE] Result: \"{self.command}\": {result}")
        return self.process(result)


class CommandResultProcessor(object):
    def __init__(self, command, result):
        """Creates instance of the command result processor
        Args:
            command(Command): Command
            result: Command execution result
        """
        self.command = command
        self.result = result
        self.outputs = {}

    @property
    def context(self):
        """Gets instance of the context
        Returns(Context): Instance of the context
        """
        return self.command.context

    def save_buffer(self, buffer, suffix):
        """Saves the buffer to the file
        Args:
            buffer(str): Buffer to be saved
            suffix(str): File path suffix
        Returns(str): filename
        """
        if not self.context:
            return None

        file_name = self.command.output_file_name(suffix)
        full_path = Path("outputs") / file_name
        path = self.context.paths.save_result(full_path, content=buffer)
        return path

    def __save_outputs(self):
        def __save_output(which, buffer):
            self.outputs[which] = self.save_buffer(buffer, suffix=which)

        __save_output('stdout', self.result.stdout.decode('utf-8'))
        __save_output('stderr', self.result.stderr.decode('utf-8'))

    def process(self):
        """Processes the command result
        Returns(CommandResult): Command result instance
        """
        self.__save_outputs()
        return CommandResult(self.result, self.outputs)


class CommandBytesBuffer(object):
    def __init__(self, str_bytes, path=None):
        """Creates Bytes buffer
        Args:
            str_bytes(bytes): Bytes
        """
        self.path = path
        self.bytes = str_bytes

    @property
    def empty(self) -> bool:
        """Whether the output is empty
        Returns(bool): true if the buffer is empty
        """
        return not self.bytes

    @property
    def content(self):
        """String content
        Returns(str): Buffer content represented by string
        """
        return self.bytes.decode('utf-8')

    def __call__(self):
        """Returns the bytes output
        Returns(bytes): Output buffer
        """
        return self.bytes

    def __str__(self):
        """Returns the output buffer as string
        Returns(str): Output string
        """
        return self.content


class CommandResult(BasicObject):
    def __init__(self, result, outputs):
        """Initializes Command result
        Args:
            result: Command execution result
            outputs(dict): Dictionary with generated outputs
        """
        super().__init__()
        self.result = result
        self.outputs = outputs

    @property
    def stdout(self):
        """ Stdout buffer
        Returns (CommandBytesBuffer): Command bytes buffer
        """
        return CommandBytesBuffer(self.result.stdout, self.outputs.get('stdout'))

    @property
    def stderr(self):
        """Stderr buffer
        Returns (CommandBytesBuffer): Command bytes buffer
        """
        return CommandBytesBuffer(self.result.stderr, self.outputs.get('stderr'))

    @property
    def return_code(self):
        """Return core of the
        Returns (int): Status core of the program execution
        """
        if hasattr(self.result, "returncode"):
            return self.result.returncode
        return 1

    @property
    def ok(self):
        """Program existed OK
        Returns(bool): True if return core is zero or it didn't timeout
        """
        return not self.timeout and self.return_code == 0

    @property
    def nok(self):
        """Program does not existed with OK
        Returns(bool): Unless OK
        """
        return not self.ok

    @property
    def timeout(self):
        """Program timed out
        Returns(bool): True if timeout
        """
        if hasattr(self.result, "timeout"):
            return self.result.timeout
        return False
