from ktdk.asserts.matchers import IsNotNone
from ktdk.core.tasks import Task
from ktdk.runtime.context import Context
from ktdk.runtime.runners import TaskRunner


class SimpleCounterLocalTask(Task):
    def _run(self, *args, **kwargs):
        self.context.config.set_test('lc', 1)
        self.asserts.check(self.context.config, IsNotNone())


class SimpleCounterGlobalTask(Task):
    def _run(self, *args, **kwargs):
        gc = self.context.config['gc']
        self.context.config.set_suite('gc', gc + 1)
        self.asserts.check(self.context.config, IsNotNone())


class FailingTask(Task):
    def _run(self, *args, **kwargs):
        self.asserts.check(None, IsNotNone())


class FailingRequiredTask(Task):
    def _run(self, *args, **kwargs):
        self.asserts.check(None, IsNotNone())


class FailingRequireTask(Task):
    def _run(self, *args, **kwargs):
        self.asserts.require(None, IsNotNone())


class ExceptionThrowingTask(Task):
    def _run(self, *args, **kwargs):
        raise RuntimeError("Exception")


def test_task_runner_with_one_task():
    task = SimpleCounterLocalTask('counter_task')
    context = Context({'gc': 0}, {'lc': 0})
    runner = TaskRunner(task=task, config={}, context=context)
    runner.invoke()
    assert context.config['lc'] == 1
    assert context.config['gc'] == 0
    assert task.result.effective.passed
    assert task.result.current.passed


def test_task_runner_with_two_tasks():
    task = SimpleCounterLocalTask('counter_local')
    gtask = SimpleCounterGlobalTask('counter_global')
    task.add_task(gtask)
    context = Context({'gc': 0}, {'lc': 0})
    runner = TaskRunner(task=task, config={}, context=context)
    runner.invoke()
    assert task.result.effective.passed
    assert task.result.current.passed
    assert context.config['lc'] == 1
    assert context.config['gc'] == 1
    assert task.asserts.passed


def test_task_runner_with_failing_task():
    task = FailingTask('failing_task')
    context = Context({'gc': 0}, {'lc': 0})
    runner = TaskRunner(task=task, config={}, context=context)
    runner.invoke()
    assert task.result.effective.failed
    assert task.asserts.failed


def test_task_runner_with_tasks_one_failed():
    task = SimpleCounterLocalTask('counter_local')
    gtask = FailingTask('failing_task')
    task.add_task(gtask)
    context = Context({'gc': 0}, {'lc': 0})
    runner = TaskRunner(task=task, config={}, context=context)
    runner.invoke()
    assert gtask.result.effective.failed
    assert gtask.result.current.failed
    assert task.result.current.passed
    assert task.result.effective.passed


def test_task_runner_with_tasks_failed_require():
    task = SimpleCounterLocalTask('counter_local')
    gtask = FailingRequireTask('failing_require_task')
    task.require_that(gtask)
    context = Context({'gc': 0}, {'lc': 0})
    runner = TaskRunner(task=task, config={}, context=context)
    runner.invoke()
    assert gtask.result.effective.failed
    assert gtask.result.current.failed
    assert task.result.current.passed
    assert task.result.effective.failed


def test_task_runner_with_exception_task():
    task = ExceptionThrowingTask('exception_throwing')
    context = Context({'gc': 0, 'devel': False}, {'lc': 0})
    runner = TaskRunner(task=task, config={}, context=context)
    runner.invoke()
    assert task.result.effective.errored
    assert task.result.current.errored
