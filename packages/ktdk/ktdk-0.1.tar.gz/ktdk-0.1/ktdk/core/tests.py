import logging

from ktdk.core import results
from ktdk.core.abstract import GeneralObject, ResultHolder, RunnerConfig
from ktdk.core.mixins import CheckersMixin, ContextMixin
from ktdk.core.results import Result
from ktdk.runtime.runners import TestRunner
from ktdk.utils import flatters

log = logging.getLogger(__name__)


class TestRunnerConfig(RunnerConfig):
    @property
    def default_runner(self):
        return TestRunner

    def __init__(self, test, **params):
        super().__init__(**params)
        self.test = test

    # pylint: disable=arguments-differ
    def get_instance(self, **params):
        """Creates instance of the test runner
        Args:
            params: params
        Returns:
            TestRunner: TestRunner instance
        """
        return super(TestRunnerConfig, self).get_instance(test=self.test, **params)
    # pylint: enable=arguments-differ


class TestResultHolder(ResultHolder):
    def __init__(self, test: 'Test'):
        super().__init__()
        self.test = test
        self._tasks_result: Result = None
        self._subtests_result: Result = None
        self._effective_result: Result = None

    def reset_result_cache(self):
        self._tasks_result = None
        self._effective_result = None
        self._subtests_result = None

    @property
    def tasks(self) -> Result:
        if self._tasks_result is None:
            self._tasks_result = self.__compute_task_result()
        return self._tasks_result

    @property
    def current(self) -> Result:
        return self.tasks

    @property
    def subtests(self):
        if self._subtests_result is None:
            self._subtests_result = self.__compute_subtests_result()
        return self._subtests_result

    def _compute_effective_result(self) -> Result:
        if not self.tasks.passed:
            return self.tasks
        return self.subtests

    def __compute_subtests_result(self):
        if any(t.result.effective.errored for t in self.test.tests):
            return results.ERROR
        if any(t.result.effective.failed for t in self.test.tests):
            return results.FAIL
        return results.PASS

    def __compute_task_result(self):
        if any(task.result.effective.errored for task in self.test.tasks):
            return results.ERROR
        if any(task.result.effective.failed for task in self.test.tasks):
            return results.FAIL
        return results.PASS

    @property
    def checked_tasks(self):
        return [task for task in flatters.flatten_tasks(self.test) if task.checked]

    @property
    def failed_tasks(self):
        return [task for task in self.checked_tasks if task.result.effective.failed]

    @property
    def errored_tasks(self):
        return [task for task in self.checked_tasks if task.result.effective.errored]

    @property
    def passed_tasks(self):
        return [task for task in self.checked_tasks if task.result.effective.passed]

    @property
    def skipped_tasks(self):
        return [task for task in self.checked_tasks if task.result.effective.skipped]

    @property
    def nok_tasks(self):
        return self.errored_tasks + self.failed_tasks

    @property
    def reduced_points(self):
        return self.__reduce_points()

    @property
    def effective_points(self):
        return self.reduced_points + sum(test.result.effective_points for test in self.test.tests)

    def to_dict(self):
        return {
            'type': 'test',
            'subtests': self.subtests.to_dict(),
            'tasks': self.tasks.to_dict(),
            'effective_points': self.effective_points,
            'reduced_points': self.reduced_points,
            **super().to_dict()
        }

    def __reduce_points(self):
        points = self.test.points
        for task in self.nok_tasks:
            points *= task.points_multiplier
        return points


class Test(GeneralObject, CheckersMixin, ContextMixin):
    """Test instance

      Attributes:
          name(str): Name of the test
          desc(str): Description of the test
          tags(set): Test tags
          weight(float): Number of points for the test
      """

    def __init__(self, tests=None, tasks=None, weight: float = 1.0, points: float = 0,
                 before=None, after=None, before_each=None, after_each=None, **kwargs):
        """Creates instance of the Test (internal)

        Args:
            name(str): name of the test
            desc(str): description of the test
            tags(set): Collection of the tags
            tests(list): Collection of child tests
            tasks(list): Collection of checks for the test
            before(list): Tasks that will be executed before the test run
            after(list): Tasks that will be executed after the test run
            before_each(list): Tasks that will be executed before each child test
            after_each(list): Tasks that will be executed after each child test
        """
        super().__init__(**kwargs)
        self._parent = None

        self.add_task(*(tasks or []))
        self.add_before(*(before or []))
        self.add_after(*(after or []))

        self.add_before(*(before_each or []), scope='each')
        self.add_after(*(after_each or []), scope='each')
        self.add_test(*(tests or []))
        self._weight = weight
        self._points = points

        self._runner = TestRunnerConfig(self)
        self._result = TestResultHolder(self)

    @property
    def result(self) -> TestResultHolder:
        """Gets an instance of the result holder (wrapper over the test)
        Returns(TestResultHolder): Result holder for the test
        """
        return self._result

    def to_dict(self):
        """Converts test to dictionary representation
        Returns:

        """
        return \
            {
                **(super().to_dict()),
                'tags': list(self.tags),
                'effective_tags': list(self.effective_tags),
                'forward_tags': list(self.forward_tags),
                'backward_tags': list(self.backward_tags),
                'points': self.points,
                'before_tasks': [t.to_dict() for t in self.before],
                'tasks': [t.to_dict() for t in self.tasks],
                'tests': [t.to_dict() for t in self.tests],
                'after_tasks': [t.to_dict() for t in self.after],
                'result': self.result.to_dict()
            }

    @property
    def effective_tags(self) -> set:
        """Gets an effective tags set
        Returns(set): Effective tags set
        """
        return self.forward_tags.union(self.backward_tags)

    @property
    def forward_tags(self) -> set:
        """Gets an forward tags set
        Returns(set): Forward tags set
        """
        parent_tags = self.parent.tags if self.parent else []
        return self.tags.union(parent_tags)

    @property
    def backward_tags(self) -> set:
        """Gets an backward tags set
        Returns(set): Backward tags set
        """
        backward_set = set()
        for test in self.tests:
            backward_set = backward_set.union(test.effective_tags)
        backward_set = backward_set.union(self.tags)
        return backward_set

    @property
    def tests(self) -> list:
        """Gets tests collection
        Returns:
            List of tests
        """
        return getattr(self, '_tests', [])

    @property
    def tasks(self) -> list:
        """Gets tasks collection
        Returns:
            List of tasks
        """
        return getattr(self, '_tasks', [])

    @property
    def before(self) -> list:
        """Gets before task
        Returns(List[Task]):
            List of tasks
        """
        return getattr(self, '_before', [])

    @property
    def after(self) -> list:
        """Gets after tasks
        Returns(List[Task]):
            List of tasks
        """
        return getattr(self, '_after', [])

    @property
    def before_each(self) -> list:
        """Gets before each test tasks
        Returns(List[Task]):
            List of tasks
        """
        return getattr(self, '_before_each', [])

    @property
    def after_each(self) -> list:
        """Gets after each test tasks
        Returns(List[Task]):
            List of tasks
        """
        return getattr(self, '_after_each', [])

    @property
    def parent(self) -> 'Test':
        """Gets parent of the test
        Returns(Test):
            Test: Instance of the parent test
        """

        return self._parent

    @parent.setter
    def parent(self, value: 'Test'):
        """ Sets the parent class of the test

        Test will reset the _log and _report
        If test already has a parent, it will warn user of the class
        Args:
            value (Test): Parent of the test
        """
        if self.parent is not None:
            log.warning(f'Overriding parent of the test: '
                        f'\"{self.name}\"; '
                        f'old: \"{self.parent.namespace}\" '
                        f'new: \"{value.namespace}\"')
        setattr(self, '_log', None)
        self._parent = value

    @property
    def namespace(self) -> str:
        """Namespace of the test
        Returns(str): Full namespace of the test
        """
        name = []
        if self.parent is not None:
            name.append(self.parent.namespace)
        name.append(self.name)
        return "::".join(name)

    @property
    def points(self) -> float:
        return self._points

    @points.setter
    def points(self, value: float):
        self._points = value

    def add_task(self, *tasks):
        """ Adds the test checks
        Args:
            *tasks: Test checks that will be added to the test
        """
        self.__add_tasks('_tasks', *tasks)

    def add_test(self, *tests: 'Test'):
        """Adds child tests to the test
        Args:
            *tests: Collection of the child tests

        """
        if not hasattr(self, '_tests'):
            setattr(self, '_tests', [])

        for test in tests:
            test.parent = self
            log.debug(f"[REG] Adding test ({self.namespace}): {test.name} [{test.namespace}]")
            self.tests.append(test)

    def add_before(self, *tasks, scope='all'):
        """Adds before checks

        Before checks are checks that will be all executed before
        the actual test and its subtests
        If the scope is set to 'each',
        the checks will be executed before **each child test**

        Args:
            *tasks: Collection of the checks
            scope(str): Either 'all' or 'each' (default: 'all')
        """
        collection = '_before' if scope == 'all' else '_before_each'
        self.__add_tasks(collection, *tasks)

    def add_after(self, *tasks, scope='all'):
        """Adds after checks

        After checks are checks that will be all executed after
        the actual test and its subtests
        If the scope is set to 'each',
        the checks will be executed after **each child test**

        Args:
            *tasks: Collection of the checks
            scope: Either 'all' of 'each' (default: 'all')

        Returns:

        """
        collection = '_after' if scope == 'all' else '_after_each'
        self.__add_tasks(collection, *tasks)

    def __add_tasks(self, collection, *tasks):
        if not hasattr(self, collection):
            setattr(self, collection, [])
        col = getattr(self, collection)
        for task in tasks:
            task.test = self
            log.debug(f"[ADD] Task {self.namespace}: {task.name} [{task.namespace}]")
            col.append(task)
