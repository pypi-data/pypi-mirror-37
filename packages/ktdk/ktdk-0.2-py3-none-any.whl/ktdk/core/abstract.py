import abc
import logging
from json import JSONEncoder

from ktdk.core import results
from ktdk.core.results import Result
from ktdk.utils.basic import BasicObject
from ktdk.utils.naming import normalize_name

log = logging.getLogger(__name__)


class RunnerConfig(BasicObject):
    @property
    @abc.abstractmethod
    def default_runner(self):
        return None

    @property
    def default_config(self):
        return {}

    def __init__(self, runner=None, **params):
        super().__init__()
        self.runner = runner or self.default_runner
        self.config = {**self.default_config, **params}

    def get_instance(self, context=None, **params):
        """Creates instance of the runner
        Args:
            context(Context): Context fot the runner
        Returns:
            Runner: Runner instance
        """
        return self.runner(context=context, config=self.config, **params)

    def update_config(self, runner=None, **config):
        self.config = {**self.config, **config}
        self.update_runner(runner=runner)

    def update_runner(self, runner=None):
        self.runner = runner or self.default_runner


class GeneralObject(BasicObject):
    def __init__(self, name: str = None, desc: str = None, tags: set = None):
        super().__init__()
        self.name = name or self.__class__.__name__
        self._desc = desc
        self._tags = set(tags or {})
        self._runner = RunnerConfig()

    def to_dict(self) -> dict:
        """Converts the object to dictionary
        Returns(dict):
        """
        return {
            'name': self.name,
            'namespace': self.namespace,
            'description': self.desc,
            'tags': list(self.tags),
            }

    @property
    def runner(self):
        return self._runner

    @property
    def name(self):
        return getattr(self, '_name')

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value

    @name.setter
    def name(self, value):
        setattr(self, '_name', normalize_name(value))

    @property
    def namespace(self):
        return self.name

    def add_tags(self, *tags):
        self._tags = self._tags.union(tags)

    @property
    def tags(self):
        return self._tags


class ResultHolder(JSONEncoder):
    def __init__(self):
        super().__init__()
        self._effective_result: Result = None

    def default(self, o):  # pylint: disable=E0202
        return o.to_dict()

    @property
    def current(self) -> Result:
        return results.NONE

    @property
    def effective(self) -> Result:
        if self._effective_result is None:
            self._effective_result = self._compute_effective_result()
        return self._effective_result

    @abc.abstractmethod
    def _compute_effective_result(self) -> Result:
        return results.NONE

    def reset_result_cache(self):
        self._effective_result = None

    def to_dict(self):
        return {
            'type': 'task',
            'effective': self.effective.to_dict(),
            'current': self.current.to_dict(),
            }
