import logging

from ktdk.core.tests import Test
from ktdk.utils.flatters import flatten_all_tasks, flatten_tests

log = logging.getLogger(__name__)


def _get_tests_with_result(tests, result):
    return [t for t in tests if getattr(t.result.current, result)]


def _count_for_tasks(test):
    tasks = flatten_all_tasks(test)
    return _count_for_collection(tasks)


def _count_for_collection(coll):
    count = dict(all=len(coll))
    for res_type in ['passed', 'failed', 'skipped', 'errored']:
        filtered = _get_tests_with_result(coll, res_type)
        count[res_type] = len(filtered)
    return count


def _get_tests_names(tests):
    result = {}

    def __names(res_type):
        sel = _get_tests_with_result(tests, res_type)
        if sel:
            result[res_type] = [selected.namespace for selected in sel]

    for rtype in ['failed', 'errored', 'skipped']:
        __names(res_type=rtype)
    return result


def _get_test_info(test):
    return dict(
        name=test.name,
        namespace=test.namespace,
        description=test.desc,
        tags=list(test.tags),
        effective_tags=list(test.effective_tags),
        points=test.points,
        result=dict(
            effective=test.result.effective.state,
            current=test.result.current.state,
            reduced_points=test.result.reduced_points,
            effective_points=test.result.effective_points
        )
    )


def _get_tests_info(all_tests):
    return [_get_test_info(test) for test in all_tests]


def stat_test(test) -> dict:
    """Statistics of the tests
    Args:
        test(Test): Root test

    Returns(dict): computed statistics

    """
    all_tests = flatten_tests(test)
    result = dict(final_points=test.result.effective_points,
                  result=test.result.effective.state)
    result['tests_count'] = _count_for_collection(all_tests)
    result['tasks_count'] = _count_for_tasks(test)
    result['nok_tests'] = _get_tests_names(all_tests)
    result['all_tests'] = _get_tests_info(all_tests)
    return result
