from ktdk.asserts import AssertionsChecks, AssertionMixin
from ktdk.core.errors import RequireFailedError

import pytest


def test_assertion_support_assert_that():
    support = AssertionMixin()
    support.inject_checks(AssertionsChecks())
    assert support.asserts.check(1, lambda x: (True, x, 'must pass'))
    assert support.asserts.passed
    assert not support.asserts.check(2, lambda x: (False, x, 'must fail'))
    assert support.asserts.failed
    assert 1 in [i.obj for i in support.asserts.passed_results]
    assert 2 in [i.obj for i in support.asserts.failed_results]


def test_assertion_support_check_that():
    support = AssertionMixin()
    support.inject_checks(AssertionsChecks())

    assert support.asserts.check(1, lambda x: (True, x, 'must pass'))
    assert support.asserts.passed
    with pytest.raises(RequireFailedError):
        support.asserts.require(2, lambda x: (False, x, 'must fail'))
    assert support.asserts.failed
    assert 1 in [i.obj for i in support.asserts.passed_results]
    assert 2 in [i.obj for i in support.asserts.failed_results]


def test_assertion_support_require_that():
    support = AssertionMixin()
    support.inject_checks(AssertionsChecks())

    support.asserts.require(1, lambda x: (True, x, 'must pass'))
    assert support.asserts.passed
    assert not support.asserts.check(2, lambda x: (False, x, 'must fail'))
    assert support.asserts.failed
    assert 1 in [i.obj for i in support.asserts.passed_results]
    assert 2 in [i.obj for i in support.asserts.failed_results]

