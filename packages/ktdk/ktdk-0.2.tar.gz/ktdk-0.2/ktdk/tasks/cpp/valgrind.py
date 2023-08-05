from ktdk.tasks.command import Command


class ValgrindCommand(Command):
    def __init__(self, command, args=None, **kwargs):
        """Creates Valgrind command instance
        Args:
            command(str): Command name
            args(list): Command arguments
        """
        super().__init__(command, args=args, **kwargs)
        self._vargs = []

    @property
    def valgrind_log_file(self):
        """Gets name of the valgrind log file
        Returns(str): Valgrind log file
        """
        if not hasattr(self, '__valgrind_log_file'):
            setattr(self, '__valgrind_log_file', self.output_file_name(suffix='valgrind.log'))
        return getattr(self, '__valgrind_log_file')

    @property
    def valgrind_command(self):
        """Valgrind command with arguments and sets log file
        Returns(list): valgrind command with valgrind arguments
        """
        args = ['valgrind']
        if self.context:
            file_path = self.context.paths.results.joinpath(self.valgrind_log_file)
            args.append(f'--log-file={file_path}')
        return ['valgrind',
                f'--log-file={file_path}',
                '--leak-check=full',
                *self._vargs]

    def add_vargs(self, *args):
        """Adds the valgrind arguments
        Args:
            *args: Valgrind arguments
        Returns(ValgrindCommand): Valgrind command instance
        """
        self._vargs.extend(args)
        return self

    @property
    def executable_command(self):
        """Executable command with arguments
        Returns(list): Executable command with arguments list
        """
        return [self.command, *self.args]

    @property
    def full_command(self):
        """Full command list
        Returns(list): Full command with valgrind and executable
        """
        return [*self.valgrind_command, *self.executable_command]

    def process(self, result):
        """Processes the result
        Args:
            result: Command execution result
        Returns: Processes result
        """
        process_result = super().process(result)
        process_result.outputs['valgrind_log'] = self.valgrind_log_file

        self.context.config.set_test('valgrind_log', self.valgrind_log_file)
        return process_result
