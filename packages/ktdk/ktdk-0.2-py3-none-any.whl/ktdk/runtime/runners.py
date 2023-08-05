"""
Runners for the test suite
"""
import abc
import logging

from ktdk.asserts import AssertionsChecks
from ktdk.core import results
from ktdk.core.errors import RequireFailedError, RequiredTaskFailed
from ktdk.utils.basic import BasicObject

log = logging.getLogger(__name__)


class Runner(BasicObject):
    def invoke(self, *args, **kwargs):
        self._run(*args, **kwargs)
        return self._process()

    @abc.abstractmethod
    def _run(self, *args, **kwargs):
        pass

    # pylint: disable=no-self-use
    def _process(self):
        return True
    # pylint: enable=no-self-use


class ExecutedTasksRegister(object):
    def __init__(self):
        self.collection = []

    def add_task(self, task):
        log.debug(f"[EXEC] Executed task: {task.namespace}")
        self.collection.append(task)

    def select(self, predicate=None):
        tasks = self.collection
        tasks = filter(predicate, tasks)
        return tasks

    def any(self, predicate=None):
        return any(self.select(predicate=predicate))


class TestRunner(Runner):
    def __init__(self, test, config, context):
        """Creates instance of the Test runner

        Args:
            test (Test): Test instance
            config (Dict): Runners configuration
            context (Context):
        """
        super().__init__()
        self.executed_tasks = ExecutedTasksRegister()
        self.test = test
        self.config = config
        self.context = context
        self.task_checks = []
        self.subtest_checks = []
        self.__init_test(context)

    # pylint: disable=no-self-use
    def _should_run(self):
        return self.context.tags.evaluate(*self.test.effective_tags)

    # pylint: enable=no-self-use

    def _run(self, *args, **kwargs):
        if not self._should_run():
            self.test.result = results.SKIP

        log.info(f"[RUN] Test: {self.test.namespace}")
        self._run_before_tasks()
        self._run_tasks()
        self._run_tests()
        self._run_after_tasks()

    def _process(self):
        return self.test

    def _run_tasks_collection(self, *args, collection=None, **kwargs):
        for task in collection:
            clone = self.context.clone()
            task_runner = task.runner.get_instance(
                context=clone,
                executed_tasks=self.executed_tasks
                )
            try:
                task_runner.invoke(*args, **kwargs)
            except RequiredTaskFailed as ex:
                log.info(f"[FAIL] Test [{self.test.namespace}] failed on task: {ex}")
                return False
        return True

    def _run_before_tasks(self):
        if self.test.parent:
            self._run_tasks_collection(collection=self.test.parent.before_each)
        return self._run_tasks_collection(collection=self.test.before)

    def _run_tasks(self):
        return self._run_tasks_collection(collection=self.test.tasks)

    def _run_after_tasks(self):
        if self.test.parent:
            self._run_tasks_collection(collection=self.test.parent.after_each)
        return self._run_tasks_collection(collection=self.test.after)

    def _run_tests(self):
        for child in self.test.tests:
            self._run_subtest(child)
        return all(test.result.effective.passed for test in self.test.tests)

    def _run_subtest(self, child):
        clone_context = self.context.clone(clone_test=True)
        child_runner = child.runner.get_instance(context=clone_context)
        child_runner.invoke()

    def __init_test(self, context):
        self.test.inject_context(context=context)


class TaskRunner(Runner):
    def __init__(self, task, config, context, executed_tasks=None):
        """Creates instance of the Task runner

       Args:
           task (Task): Task instance
           config (Dict): Runners configuration
           context (Context):
       """
        super().__init__()
        self.executed_tasks: ExecutedTasksRegister = executed_tasks or ExecutedTasksRegister()
        self.config = config
        self.context = context
        self.task = self.__init_task(task)

    # pylint: disable=no-self-use
    def _should_run(self):
        return True

    # pylint: enable=no-self-use

    def _run(self, *args, **kwargs):
        log.info(f"[RUN] Task: {self.task.namespace}")
        if not self._should_run():
            self.task.result = results.SKIP
        self.__execute_task_and_save_result()
        self._run_child_tasks()

    def __init_task(self, task):
        checks = AssertionsChecks()
        task.inject_checks(checks)
        task.inject_context(self.context)
        return task

    # pylint: disable=broad-except
    def __invoke_task_run(self):
        try:
            self.task.invoke()
        except RequireFailedError as ex:
            log.warning(f"[REQUIRE] Failed: {ex}")
        except Exception as ex:
            log.error(f"[ERROR] Task: {ex}")
            if self.context.devel:
                raise ex
            return results.ERROR
        if self.task.asserts.passed:
            return results.PASS
        return results.FAIL

    # pylint: enable=broad-except

    def __execute_task_and_save_result(self):
        result = self.__invoke_task_run()
        self.task.result.set(result=result)
        self.executed_tasks.add_task(self.task)

    def __halt_test_if_required(self, result):
        if not result.passed and self.task.required:
            raise RequiredTaskFailed(self.task)
        return result

    def _run_child_tasks(self, *args, **kwargs):
        for child in self.task.tasks:
            self._run_child_subtask(child=child, *args, **kwargs)

    def _run_child_subtask(self, child, *args, **kwargs):
        clone = self.context.clone()
        child_runner = child.runner.get_instance(
            context=clone,
            executed_tasks=self.executed_tasks
            )
        child_runner.invoke(*args, **kwargs)
        return child.result
