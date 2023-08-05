from ktdk.core import results
from ktdk.core.results import Result


def test_construct_result():
    res = results.NONE
    assert res.state == Result.NONE
    assert res.nok
    assert not res.ok
    assert res.reason == 'NONE'


def test_pass_result():
    res = results.PASS
    assert res.ok
    assert not res.nok
    assert res.passed
    assert not res.errored
    assert not res.failed
    assert not res.skipped
    assert res.reason == 'PASS'


def test_fail_result():
    res = results.FAIL
    assert not res.ok
    assert res.nok
    assert not res.passed
    assert not res.errored
    assert res.failed
    assert not res.skipped
    assert res.reason == 'FAIL'


def test_skip_result():
    res = results.SKIP
    assert res.ok
    assert not res.nok
    assert not res.passed
    assert not res.errored
    assert not res.failed
    assert res.skipped
    assert res.reason == 'SKIP'


def test_error_result():
    res = results.ERROR
    assert not res.ok
    assert res.nok
    assert not res.passed
    assert res.errored
    assert not res.failed
    assert not res.skipped
    assert res.reason == 'ERROR'
