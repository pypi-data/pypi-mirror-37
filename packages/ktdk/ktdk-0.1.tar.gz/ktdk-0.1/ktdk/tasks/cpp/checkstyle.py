import os.path
from pathlib import Path
from typing import Optional, Union

from ktdk import Task
from ktdk.asserts.utils import get_context_diff
from ktdk.tasks.command_task import CommandTask


# clang-format --style=file "/path/to/file" | diff -B -rupN "/path/to/file" -
# https://clang.llvm.org/docs/ClangFormat.htmls

class ClangFormatFilesTask(Task):
    def __init__(self, files: list, style: str, command=None, **kwargs):
        self.command = command
        self.style = style
        self.files = files
        super().__init__(**kwargs)

    def _run(self, *args, **kwargs):
        for fpath in self.files:
            self.add_task(ClangFormatTask(file=fpath, style=self.style, command=self.command))


class ClangFormatTask(CommandTask):
    def __init__(self, file: Union[str, Path], style: str = None, command=None, **kwargs):
        command = command or 'clang-format'
        super().__init__(command=command, **kwargs)
        self.add_tags('checkstyle', 'format')
        self._file = file
        self._style = style

    @property
    def file(self) -> Path:
        if os.path.isabs(self._file):
            return Path(self._file)
        return self.context.paths.workspace_path(self._file)

    def get_diff_with_same_file(self, stdout: str):
        content = Path(self.file).read_text(encoding='utf-8')
        diff = get_context_diff(expected=content, provided=stdout)
        return diff

    def _run(self, *args, **kwargs):
        if self._style:
            self.args.extend(['--style', self._style])
        self.args.extend([str(self.file)])
        result = self.execute()
        diff = self.get_diff_with_same_file(stdout=result.stdout.content)
        diff_list = list(diff)
        diff_str = ''.join(diff_list)
        self.context.paths.save_result(f'diff/format_diff_{self.file.name}.diff', diff_str)
        self.context.config.set_test('command_result', result)
        self.context.config.set_test('tidy_result', diff_list)


# http://clang.llvm.org/extra/clang-tidy/
# clang-tidy -extra-arg-before=-x -extra-arg-before=c++
#   -extra-arg=-std=c++14
#   -header-filter='^(room.h)|(course.h)|(reservation.h)|(rsystem.h)|(handler.h)$'
#   main.cpp "handler.cpp" "rsystem.cpp" | sed -r 's#/([^/]+/)+_tmp_/([^/]+/)+##g'
class ClangTidyCheckStyle(CommandTask):
    def __init__(self, files: list, headers: list = None, command=None,
                 extra_args: list = None, extra_before=None, **kwargs):
        command = command or 'clang-tidy'
        super().__init__(command=command, **kwargs)
        self.add_tags('checkstyle', 'tidy')
        self._files = files
        self._headers = headers or []
        self._extra_args = extra_args or []
        self._extra_before = extra_before or []

    def file_path(self, fpath: str) -> str:
        if os.path.isabs(fpath):
            return str(fpath)
        return str(self.context.paths.workspace_path(fpath))

    @property
    def cwd(self) -> str:
        return str(self.context.paths.workspace)

    @property
    def files(self):
        return [self.file_path(fpath) for fpath in self._files]

    @property
    def headers(self) -> list:
        return self._headers

    @property
    def _header_filter(self) -> Optional[str]:
        if not self.headers:
            return None
        header_filter = "|".join([f"({header})" for header in self.headers])
        return f"\"^{header_filter}$\""

    @property
    def extra_args(self) -> list:
        return self._extra_args

    @property
    def extra_before(self) -> list:
        return self._extra_before

    def build_command_args(self) -> list:
        result = []
        for arg in self.extra_before:
            result.append(f'-extra-arg-before={arg}')
        for arg in self.extra_args:
            result.append(f'-extra-arg={arg}')
        header_filter = self._header_filter
        if header_filter:
            result.append(self._header_filter)
        result.extend(self.files)
        return result

    def _run(self, *args, **kwargs):
        self.args.extend(self.build_command_args())
        result = self.execute(cwd=self.cwd)
        self.context.config.set_test('command_result', result)
        self.context.config.set_test('tidy_result', result)

    def _process(self):
        super(ClangTidyCheckStyle, self)._process()


class CPPClangTidyCheckStyle(ClangTidyCheckStyle):
    def __init__(self, files: list, **kwargs):
        super().__init__(files, **kwargs)
        self.extra_args.extend(['-std=c++14'])
        self.extra_before.extend(['-x', 'c++'])


# http://clang.llvm.org/extra/clang-tidy/
# clang-tidy -extra-arg-before=-x -extra-arg-before=c++
#   -extra-arg=-std=c++14
#   -header-filter='^(room.h)|(course.h)|(reservation.h)|(rsystem.h)|(handler.h)$'
#   main.cpp "handler.cpp" "rsystem.cpp" | sed -r 's#/([^/]+/)+_tmp_/([^/]+/)+##g'
class CClangTidyCheckStyle(ClangTidyCheckStyle):
    def __init__(self, files: list, **kwargs):
        super().__init__(files, **kwargs)
        self.extra_args.extend(['-std=c99'])
        self.extra_before.extend(['-x', 'c'])
