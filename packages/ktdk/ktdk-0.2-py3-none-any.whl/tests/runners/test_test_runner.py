from ktdk.asserts.matchers import IsNotNone, Equals
from ktdk.core.tasks import Task
from ktdk.core.tests import Test
from ktdk.runtime.context import Context


class SimpleCounterLocalTask(Task):
    def _run(self, *args, **kwargs):
        self.context.config.set_test('lc', 1)
        self.asserts.check(self.context.config, IsNotNone())


class SimpleLocalLevelTask(Task):
    def _run(self, *args, **kwargs):
        self.asserts.check(self.context.config['lc'], Equals(1))
        self.context.config.set_test('lc', 2)
        self.asserts.check(self.context.config, IsNotNone())


class SimpleCounterGlobalTask(Task):
    def _run(self, *args, **kwargs):
        self.context.config.set_suite('gc', 1)
        self.asserts.check(self.context.config, IsNotNone())


class FailingTask(Task):
    def _run(self, *args, **kwargs):
        self.asserts.check(None, IsNotNone())


def test_test_runner_with_one_test():
    test = Test(name='test_name')
    runner = test.runner.get_instance(context=Context())
    runner.invoke()
    assert test.result.effective.passed


def test_test_runner_with_two_tests():
    test1 = Test(name='first')
    test2 = Test(name='second')
    test1.add_test(test2)
    runner = test1.runner.get_instance(context=Context())
    runner.invoke()
    assert test1.result.effective.passed


def test_test_runner_with_two_tests_and_task():
    test1 = Test(name='first')
    test2 = Test(name='second')
    task = SimpleCounterLocalTask('count task')
    test1.add_test(test2)
    test2.add_task(task)
    context = Context(suite_config={'gc': 0}, test_config={'lc': 0})
    runner = test1.runner.get_instance(context=context)
    result = runner.invoke()
    assert result
    assert 0 == context.config['lc']


def test_test_runner_with_two_tests_and_global_task():
    test1 = Test(name='first')
    test2 = Test(name='second')
    task = SimpleCounterGlobalTask('count task')
    test1.add_test(test2)
    test2.add_task(task)
    context = Context(suite_config={'gc': 0}, test_config={'lc': 0})
    runner = test1.runner.get_instance(context=context)
    result = runner.invoke()
    assert result
    assert 1 == context.config['gc']


def test_test_runner_with_two_tests_and_failing_task():
    test1 = Test(name='first')
    test2 = Test(name='second')
    task = FailingTask('count task')
    test1.add_test(test2)
    test2.add_task(task)
    context = Context(suite_config={'gc': 0}, test_config={'lc': 0})
    runner = test1.runner.get_instance(context=context)
    result = runner.invoke()
    assert result


def test_test_runner_with_two_tests_and_two_tasks():
    test1 = Test(name='first')
    test2 = Test(name='second')
    task = SimpleCounterLocalTask('count task')
    task2 = SimpleLocalLevelTask('count task2')
    test1.add_test(test2)
    test2.add_task(task)
    test2.add_task(task2)
    context = Context(suite_config={'gc': 0}, test_config={'lc': 0})
    runner = test1.runner.get_instance(context=context)
    result = runner.invoke()
    assert result
    assert 0 == context.config['lc']
