import pytest

from ktdk import Context, Test
from ktdk.asserts.checks.general import TaskResultCheck
from ktdk.asserts.matchers import IsNone, IsNotNone, ResultPassed
from ktdk.core.tasks import Task


class FailingTask(Task):
    def _run(self, *args, **kwargs):
        self.asserts.check(None, IsNotNone())


class PassingTask(Task):
    def _run(self, *args, **kwargs):
        self.asserts.check(None, IsNone())


def get_failing_task():
    return FailingTask(name='failing_task')


def get_passing_task():
    return PassingTask(name='passing_task')


def get_failing_test(num: int = 0, points: float = 1):
    test = Test(name=f"test_{num}", desc=f"Failing test number {num}", points=points)
    fail = get_failing_task()
    test.add_task(fail)
    fail.check_that(TaskResultCheck(matcher=ResultPassed()))
    return test


def get_failing_reduce_test(num: int = 0, *reduces):
    test = Test(name=f"test_{num}", desc=f"Failing test number {num}", points=1)
    fail = get_failing_task()
    test.add_task(fail)
    for reduce in reduces:
        fail.check_that(TaskResultCheck(matcher=ResultPassed()), reduce)
    return test


def get_passing_test(num: int = 0, weight: float = 1):
    test = Test(name=f"test_{num}", desc=f"Passing test number {num}", points=weight)
    passing = get_passing_task()
    test.add_task(passing)
    passing.check_that(TaskResultCheck(matcher=ResultPassed()))
    return test


@pytest.fixture
def test():
    return Test(name='suite')


def test_should_have_full_points(test: Test):
    for i in range(10):
        test.add_test(get_passing_test(i + 1))
    runner = test.runner.get_instance(context=Context())
    runner.invoke()
    assert test.result.effective_points == 10


def test_should_have_half_points(test: Test):
    for i in range(10):
        test.add_test(get_passing_test(i + 1))
    for i in range(10):
        test.add_test(get_failing_test(i + 1))
    runner = test.runner.get_instance(context=Context())
    runner.invoke()
    assert test.result.effective_points == 10


def test_should_have_different_points_for_a_test(test: Test):
    test.add_test(get_passing_test(1))
    test.add_test(get_failing_test(1))
    test.add_test(get_failing_test(1, 4))
    test.add_test(get_passing_test(1, 2))

    runner = test.runner.get_instance(context=Context())
    runner.invoke()
    assert test.result.effective_points == 3


def test_should_have_multiple_layers(test: Test):
    naostro = get_passing_test(0, 5)
    nanecisto = get_passing_test(0, 3)

    naostro.add_test(get_passing_test(1))
    naostro.add_test(get_passing_test(3))
    naostro.add_test(get_failing_test(2))
    naostro.add_test(get_failing_test(4))

    nanecisto.add_test(get_passing_test(1))
    nanecisto.add_test(get_passing_test(3))
    nanecisto.add_test(get_failing_test(2))
    nanecisto.add_test(get_failing_test(4))

    test.add_test(naostro, nanecisto)

    runner = test.runner.get_instance(context=Context())
    runner.invoke()
    assert test.result.effective_points == 7 + 5
    assert naostro.result.effective_points == 7
    assert nanecisto.result.effective_points == 5


def test_should_have_multiple_passing_layers(test: Test):
    naostro = get_passing_test(0, 0.7)
    nanecisto = get_passing_test(0, 0.3)

    naostro.add_test(get_passing_test(1))
    naostro.add_test(get_passing_test(3))
    naostro.add_test(get_passing_test(2))
    naostro.add_test(get_passing_test(4))

    nanecisto.add_test(get_passing_test(1))
    nanecisto.add_test(get_passing_test(3))
    nanecisto.add_test(get_passing_test(2))
    nanecisto.add_test(get_passing_test(4))

    test.add_test(naostro, nanecisto)

    runner = test.runner.get_instance(context=Context())
    runner.invoke()
    assert test.result.effective_points == 9


def test_should_have_multiple_passing_layers_nanecisto_failing(test: Test):
    naostro = get_passing_test(0, 0.7)
    nanecisto = get_failing_test(0, 0.3)

    naostro.add_test(get_passing_test(1))

    nanecisto.add_test(get_passing_test(1))
    nanecisto.add_test(get_passing_test(3))
    nanecisto.add_test(get_passing_test(2))
    nanecisto.add_test(get_passing_test(4))

    test.add_test(naostro, nanecisto)

    runner = test.runner.get_instance(context=Context())
    runner.invoke()
    assert test.result.effective_points == 5.7


def test_should_reduce_points_if_test_fails(test: Test):
    test.add_test(get_failing_reduce_test(1, 0.3))
    runner = test.runner.get_instance(context=Context())
    runner.invoke()
    assert test.result.effective_points == 0.3


def test_should_reduce_multiple_points_if_test_fails(test: Test):
    test.add_test(get_failing_reduce_test(1, 0.5, 0.3))
    runner = test.runner.get_instance(context=Context())
    runner.invoke()
    assert test.result.effective_points == 0.3 * 0.5
