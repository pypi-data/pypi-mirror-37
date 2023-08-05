import logging
from copy import deepcopy
from pathlib import Path
from typing import Union

from ktdk.runtime.tags import TagsEvaluator
from ktdk.utils.basic import BasicObject

log = logging.getLogger(__name__)


def deep_merge(source, destination):
    """Deep merge
    Examples:
    >>> a = { 'first' : { 'all_rows': { 'pass': 'dog', 'number': '1' } } }
    >>> b = { 'first' : { 'all_rows': { 'fail': 'cat', 'number': '5' } } }
    >>> deep_merge(b, a) == {'first':{'all_rows':{'pass': 'dog', 'fail': 'cat', 'number': '5'}}}
    True
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            deep_merge(value, node)
        else:
            destination[key] = value

    return destination


class ContextDirs(object):
    """Context dirs wrapper for paths
    """

    def __init__(self, context: 'Context'):
        """Creates instance of the paths dirs
        Args:
            context(Context): Context instance
        """
        self.context = context

    @property
    def workspace(self) -> Path:
        """Gets workspace path
        Returns(Path): Workspace path
        """
        return Path(self.context.config['workspace_dir'])

    @property
    def test_files(self) -> Path:
        """Test files path
        Returns(Path): Test file path
        """
        return Path(self.context.config['test_files_dir'])

    @property
    def submission(self) -> Path:
        """Submission files path
        Returns:

        """
        return Path(self.context.config['submission_dir'])

    def submission_path(self, sub_path: Union[str, Path], create=False) -> Path:
        return self.__get_subdir(self.submission, sub_path, create)

    def test_path(self, sub_path: Union[str, Path], create=False) -> Path:
        return self.__get_subdir(self.test_files, sub_path, create)

    def result_path(self, sub_path: Union[str, Path], create=False) -> Path:
        return self.__get_subdir(self.results, sub_path, create)

    def workspace_path(self, sub_path: Union[str, Path], create=False) -> Path:
        return self.__get_subdir(self.workspace, sub_path, create)

    def __get_subdir(self, where: Path, sub_path, create=False):
        full_path = where / Path(sub_path)
        if create and not full_path.exists():
            full_path.mkdir(parents=True)
        return full_path

    @property
    def results(self) -> Path:
        """Gets results path
        Returns(Path): Results path

        """
        results_dir = self.context.config['results_dir']
        if not results_dir:
            results_dir = self.workspace / 'results'
        return Path(results_dir)

    def get_dir(self, name) -> Path:
        return getattr(self, name)

    def resolve(self, name) -> Path:
        return getattr(self, name, name)

    def save_result(self, sub_path: Union[str, Path], content) -> Path:
        path = self.results / Path(sub_path)
        base_dir: Path = path.parent
        if not base_dir.exists():
            base_dir.mkdir(parents=True)
        log.debug(f"[SAVE] Save content to the results file: {sub_path}")
        path.write_text(content, encoding='utf-8')
        return path


class ContextConfig(object):
    def __init__(self, suite_config=None, test_config=None, task_config=None):
        self._suite = suite_config if suite_config is not None else {}
        self._test = test_config if test_config is not None else {}
        self._task = task_config if task_config is not None else {}

    @property
    def suite(self):
        return self._suite

    @property
    def test(self):
        return self._test

    @property
    def task(self):
        return self._task

    @property
    def all(self):
        config = {}
        config = deep_merge(self.suite, config)
        config = deep_merge(self.test, config)
        config = deep_merge(self.task, config)
        return config

    def __set_any(self, which, name, value):
        collection = getattr(self, which)
        if name in collection:
            log.debug(f"[CTX] Overriding: ({collection[name]}) by ({value})!")
        else:
            log.debug(f"[CTX] SET: {which}['{name}'] = {value}")
        collection[name] = value

    def __add_any(self, which, name, value):
        collection = getattr(self, which)
        old_value = collection.get(name, None)
        new_value = deepcopy(value)

        if isinstance(value, list):
            new_value = old_value + value if old_value else deepcopy(value)

        if isinstance(value, dict):
            new_value = deep_merge(old_value or {}, new_value)

        log.debug(f"[CTX] Adding ({which}): {old_value} + {value} -> {new_value}")
        collection[name] = new_value

    def add_suite(self, name, value):
        self.__add_any('suite', name, value)

    def add_test(self, name, value):
        self.__add_any('test', name, value)

    def add_task(self, name, value):
        self.__add_any('task', name, value)

    def set_suite(self, name, value):
        self.__set_any('suite', name, value)

    def set_test(self, name, value):
        self.__set_any('test', name, value)

    def set_task(self, name, value):
        self.__set_any('task', name, value)

    def clone(self, clone_test=False):
        test_config = deepcopy(self.test) if clone_test else self.test
        task_config = deepcopy(self.task)
        config = ContextConfig(suite_config=self.suite,
                               test_config=test_config,
                               task_config=task_config)
        return config

    def __getitem__(self, item):
        return self.all.get(item)

    def get(self, name):
        return self.all.get(name)

    def __str__(self):
        return str(self.all)

    def __repr__(self):
        return str(self.all)


class Context(BasicObject):
    def __init__(self, suite_config=None, test_config=None, task_config=None, config=None):
        super().__init__()
        self._config = config or ContextConfig(suite_config=suite_config,
                                               test_config=test_config,
                                               task_config=task_config)
        self._tags_evaluator = TagsEvaluator(self.config['tags'], self.config['registered_tags'])
        self._context_dirs = ContextDirs(self)

    @property
    def tags(self):
        return self._tags_evaluator

    @property
    def devel(self):
        return self.config.all.get('devel', False)

    @property
    def dirs(self) -> ContextDirs:
        return self._context_dirs

    @property
    def paths(self) -> ContextDirs:
        return self.dirs

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    def clone(self, clone_test=False):
        return Context(config=self.config.clone(clone_test=clone_test))

    def to_dict(self):
        return self.config
