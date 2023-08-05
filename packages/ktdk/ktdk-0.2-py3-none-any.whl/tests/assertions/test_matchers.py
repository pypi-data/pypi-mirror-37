import pytest

from ktdk.asserts import AssertionsChecks
from ktdk.asserts.matchers import *
from ktdk.core import results
from ktdk.core.tasks import Task


@pytest.fixture
def task():
    task = Task('test_task')
    task.inject_checks(AssertionsChecks())
    return task


def test_general_matcher_invoke():
    matcher = GeneralMatcher('basic matcher')
    cond, obj, message = matcher.invoke("some string")
    assert cond
    assert obj == "some string"


def test_general_expected_matcher_invoke():
    matcher = GeneralExpectedMatcher('expected string')
    cond, obj, message = matcher.invoke('expected string')
    assert cond
    assert matcher.expected == "expected string"
    assert obj == "expected string"


def test_matchers_diff():
    expected = "Ahoj svet ako sa mas?\nJa sa mam dobre.\nSame"
    orig = "Ahoj svet ako sa mas?\nJa sa mam dobre.\nSame"
    matcher = Diff(expected)
    cond, obj, message = matcher(orig)
    assert cond
    assert matcher.expected == expected
    assert obj == orig


def test_matchers_not_same_diff():
    expected = "Ahoj svet ako sa mas?\nJa sa mam zle.\nSame\n"
    orig = "Ahoj svet ako sa mas?\nJa sa mam dobre.\nNot same\n"
    matcher = Diff(expected)
    cond, obj, message = matcher(orig)
    assert not cond
    assert matcher.expected == expected
    assert obj == orig


def test_matchers_equals():
    matcher = Equals('expected string')
    cond, obj, message = matcher.invoke('expected string')
    assert cond
    assert matcher.expected == "expected string"
    assert obj == "expected string"


def test_matchers_not_equals():
    matcher = NotEquals('expected string')
    cond, obj, message = matcher.invoke('expected string')
    assert not cond
    assert matcher.expected == "expected string"
    assert obj == "expected string"


def test_matchers_greater():
    matcher = Greater(2)
    cond, obj, message = matcher(1)
    assert not cond


def test_matchers_less():
    matcher = Less(2)
    cond, obj, message = matcher(1)
    assert cond


def test_matchers_less_equals():
    matcher = LessEquals(2)
    cond, obj, message = matcher(2)
    cond2, obj2, message2 = matcher(1)
    assert cond2
    assert cond


def test_matchers_greater_equals():
    matcher = GreaterEquals(2)
    cond, obj, message = matcher(2)
    cond2, obj2, message2 = matcher(3)
    assert cond2
    assert cond


def test_matchers_is_none():
    matcher = IsNone()
    cond, obj, message = matcher(None)
    assert cond
    cond, obj, message = matcher(1111)
    assert not cond


def test_matchers_is_not_none():
    matcher = IsNotNone()
    cond, obj, message = matcher(None)
    assert not cond
    cond, obj, message = matcher(1111)
    assert cond


def test_matchers_checks_passed(task):
    matcher = ChecksPassed()
    task.asserts.check(True)
    cond, obj, message = matcher(task)
    assert cond


def test_matchers_checks_failed(task):
    matcher = ChecksFailed()
    task.asserts.check(False)
    cond, obj, message = matcher(task)
    assert cond


def test_matchers_result_passed():
    matcher = ResultPassed()
    passed_result = results.PASS
    cond, obj, message = matcher(passed_result)
    assert cond


def test_matchers_result_failed():
    matcher = ResultFailed()
    cond, obj, message = matcher(results.FAIL)
    assert cond
