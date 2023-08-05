"""
Tasks module
"""
import logging
from enum import Enum

from ktdk.asserts import AssertionMixin
from ktdk.core import results
from ktdk.core.abstract import GeneralObject, ResultHolder, RunnerConfig
from ktdk.core.mixins import CheckersMixin, ContextMixin
from ktdk.core.results import Result
from ktdk.runtime.runners import TaskRunner

log = logging.getLogger(__name__)


class TaskRunnerConfig(RunnerConfig):
    """Task runner configuration
    """

    @property
    def default_runner(self):
        """Gets a default runner for the task
        Returns:
        """
        return TaskRunner

    def __init__(self, task: 'Task', **params):
        """Creates a task runner
        Args:
            task(Task):
            **params:
        """
        super().__init__(**params)
        self.task = task

    # pylint: disable=arguments-differ
    def get_instance(self, **params):
        """Creates instance of the test runner
        Args:
            params: params
        Returns:
            TestRunner: TestRunner instance
        """
        return super(TaskRunnerConfig, self).get_instance(task=self.task, **params)
    # pylint: enable=arguments-differ


class TaskResultHolder(ResultHolder):
    """Keeps the results of the task, effective and current task
    """

    def __init__(self, task: 'Task'):
        super().__init__()
        self.task = task
        self._task_result = None
        self._subtasks_result: Result = None

    def reset_result_cache(self):
        super().reset_result_cache()
        self._subtasks_result = None
        self._task_result = None

    def set(self, result: Result):
        self._task_result = result

    @property
    def current(self) -> Result:
        return self._task_result or results.NONE

    @property
    def subtasks(self) -> Result:
        if self._subtasks_result is None:
            self._subtasks_result = self.__compute_subtasks_result()
        return self._subtasks_result

    def _compute_effective_result(self) -> Result:
        if not self.current.passed:
            return self.current
        return self.subtasks

    def __compute_subtasks_result(self) -> Result:
        if any(t.result.effective.errored for t in self.task.tasks):
            return results.ERROR
        if any(t.checked and t.result.effective.failed for t in self.task.tasks):
            return results.FAIL
        return results.PASS

    def to_dict(self):
        return {
            'type': 'task',
            'subtasks': self.subtasks.to_dict(),
            **super().to_dict(),
        }


class TaskType(Enum):
    """Defines Task types
    Types:
        - 'normal'
        - 'required'
        - 'checked'
    """
    NORMAL = 'normal'
    REQUIRED = 'required'
    CHECKED = 'checked'


class Task(GeneralObject, AssertionMixin, ContextMixin, CheckersMixin):
    """Task instance

    Attributes:
        desc(str): Description of the task
        name(str): Name of the task
        tasks(list): Child task that should be executed
        required(bool): Whether this task is required to be successful
    """

    def __init__(self, name: str = None, test=None, parent: 'Task' = None,
                 tasks: list = None, task_type: TaskType = None, **kwargs):
        """Creates instance of the task
        Args:
            name(str): Name of the task
            test(Test): Name of the test
            parent(Task): Parent task
            tasks(list): List of tasks
            **kwargs: Arguments provided to General Object
        """
        super().__init__(name=name, **kwargs)
        self._type = task_type or TaskType.NORMAL
        self.tasks: list = list(tasks or [])
        self._runner: TaskRunnerConfig = TaskRunnerConfig(self)
        self.__test = test
        self.__parent = parent
        self._result = TaskResultHolder(self)
        self._points_multiplier = 1

    @property
    def points_multiplier(self):
        """Gets a point multiplier
        Returns:

        """
        return self._points_multiplier

    @property
    def result(self) -> TaskResultHolder:
        """Gets a result for a Task
        Returns(TaskResultHolder):

        """
        return self._result

    @property
    def checked(self) -> bool:
        """Gets information whether task is checked or required or not
        Returns(bool): True if task is checked or required
        """
        return self.type in (TaskType.CHECKED, TaskType.REQUIRED)

    @property
    def required(self) -> bool:
        """Gets whether task is
        Returns:

        """
        return self.type == TaskType.REQUIRED

    @property
    def type(self) -> TaskType:
        """Gets type of the task
        """
        return self._type

    @property
    def effective_checked(self) -> bool:
        """Gets whether task is effective checked

        Task is effective checked, if the task itself is checked, or it's descendant tasks are
        checked.
        Returns(bool): true - if task is effective checked

        """
        if self.checked:
            return True
        if not self.tasks:
            return False
        return any(t.effective_checked for t in self.tasks)

    @property
    def test(self):
        """Gets an instance of the the owning test
        Returns(Test):
        """
        return self.__test

    @test.setter
    def test(self, value):
        """Sets an instance of the owning test
        Args:
            value(Test): Test instance
        """
        if self.__test is not None:
            log.warning(f'Overriding the test of the task: '
                        f'\"{self.name}\"; '
                        f'old: \"{self.test.namespace}\" '
                        f'new: \"{value.namespace}\"')
        setattr(self, '_log', None)
        self.__test = value

        for child in self.tasks:
            child.test = self.__test

    @property
    def parent(self) -> 'Task':
        """Gets an instance of the the parent task
        Returns(Task): Parent task instance
        """
        return self.__parent

    @parent.setter
    def parent(self, value: 'Task'):
        """Sets an instance of the the parent task
        Args:
            value(Task): Parent task instance
        """
        if self.parent is not None:
            log.warning(f'Overriding parent of the task: '
                        f'\"{self.name}\"; '
                        f'old: \"{self.parent.namespace}\" '
                        f'new: \"{value.namespace}\"')
        setattr(self, '_log', None)
        self.__parent = value

    @property
    def test_namespace(self) -> str:
        """Gets a test namespace
        Returns(str): Test namespace
        """
        return self.test.namespace if self.test else None

    @property
    def task_namespace(self) -> str:
        """Gets a task namespace
        Returns(str): Task namespace
        """
        name = []
        if self.parent is not None:
            name.append(self.parent.task_namespace)
        name.append(self.name)
        return ".".join(name)

    @property
    def namespace(self) -> str:
        """Gets a full namespace
        Returns(str): Full namespace
        """
        return ".".join([(self.test_namespace or ''), self.task_namespace])

    def add_task(self, *tasks: 'Task'):
        """Adds subtask
        Args:
            *tasks(Task):
        """
        self.__add_tasks(self.tasks, *tasks)

    def _run(self, *args, **kwargs):
        """Runs the task
        Args:
            *args: optional positional ars for run
            **kwargs: Keywords arguments for the run
        """
        pass

    def invoke(self, *args, **kwargs):
        """Invokes the task - runs and process the task
        Args:
            *args: optional positional ars for run
            **kwargs: Keywords arguments for the run
        """
        self._run(*args, **kwargs)
        return self._process()

    # pylint: disable=no-self-use
    def _process(self):
        """Process the task
        """
        return True

    # pylint: enable=no-self-use

    def to_dict(self) -> dict:
        """Converts the task to dictionary
        Returns(dict): task serialized do dictionary
        """
        res = {
            **(super().to_dict()),
            'result': self.result.to_dict(),
            'type': self.type.value,
        }
        if self.asserts:
            res['checks'] = self.asserts.to_dict()
        if self.tasks:
            res['tasks'] = [task.to_dict() for task in self.tasks]
        return res

    def __add_tasks(self, collection, *tasks):
        for task in tasks:
            task.test = self.test
            task.parent = self
            log.debug(f"[ADD] Task {self.namespace}: {task.name} [{task.namespace}]")
            collection.append(task)


class PipeTask(Task):
    def __init__(self, task=None, pipe=None, task_params=None, **kwargs):
        super().__init__(**kwargs)
        self.task = task or Task
        self.pipe = pipe
        self.task_params = task_params or {}

    def _run(self):
        params = {**self.task_params}
        params[self.pipe] = self.pipe_action()
        piped_task = self.task(**params)
        self.add_task(piped_task)

    def pipe_action(self):
        return None
