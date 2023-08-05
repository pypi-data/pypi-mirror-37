from ktdk.core.tasks import Task
from ktdk.core.tests import Test as Instance, TestRunnerConfig
from ktdk.runtime.runners import TestRunner, Runner
from tests.utils import TestUtils, TaskUtils


def assert_test(test, **params):
    params = {**TestUtils.EMPTY, **params}
    assert params['name'] == test.name
    assert params['desc'] == test.desc
    assert set(params['tags']) == test.tags
    assert params['tests'] == test.tests
    assert params['before'] == test.before
    assert params['after'] == test.after


def test_empty_constructor():
    test = Instance()
    assert_test(test)


def test_with_name_and_desc():
    test = Instance(name='Test01', desc='Test desc')
    assert_test(test, name='test01', desc='Test desc')


def test_with_all_constructor_params():
    params = TestUtils.get_params()
    test = TestUtils.construct_test(**params)
    assert_test(test, **params)


def test_set_all_params_without_tasks_and_tests():
    params = TestUtils.get_params()
    test = TestUtils.create_test(**params)
    assert_test(test, **params)


def test_test_has_default_instance_of_runner():
    test = TestUtils.create_test()
    assert test.runner.runner == TestRunner


def test_updated_tags():
    params = TestUtils.get_params()
    test = TestUtils.create_test(**params)
    test.add_tags('new_tag')
    tags = {
        'tags': {'naostro', 'generic', 'stylecheck', 'new_tag'}
    }
    params = {**params, **tags}
    assert_test(test, **params)


def test_add_one_child_test():
    child_test = TestUtils.create_test()
    test = TestUtils.create_test(tests=[child_test])
    assert test.tests
    assert child_test in test.tests
    assert child_test.parent == test


def test_add_multiple_child_tests():
    ch_tests = [TestUtils.create_test() for _ in range(5)]
    test = TestUtils.create_test(tests=[*ch_tests])
    assert len(test.tests) == 5
    for child in ch_tests:
        assert child.parent == test
        assert child in test.tests


def test_add_tasks():
    tasks = [TaskUtils.create_task() for _ in range(5)]
    test = TestUtils.create_test(tasks=[*tasks])
    assert len(test.tasks) == 5
    for task in tasks:
        assert task.test == test
        assert task in test.tasks


def test_namespace_for_test_without_children():
    test = TestUtils.create_test(name="Test")
    assert test.namespace == "test"


def test_namespace_for_test_with_children():
    test = TestUtils.create_test(name='Test')
    child = TestUtils.create_test(name='Child')
    test.add_test(child)
    assert test.namespace == 'test'
    assert child.namespace == 'test::child'


def test_test_config_get_runner():
    test = TestUtils.create_test()
    runner = test.runner.get_instance()
    assert isinstance(runner, TestRunner)


def test_effective_tags():
    test = Instance(name='test', tags=['test'])
    naostro = Instance(name='naostro', tags=['naostro'])
    nanecisto = Instance(name='nanecisto', tags=['nanecisto'])
    test.add_test(naostro)
    test.add_test(nanecisto)
    assert 'test' in test.effective_tags
    assert 'naostro' in test.effective_tags
    assert 'nanecisto' in test.effective_tags
    assert 'nanecisto' not in naostro.effective_tags
    assert 'naostro' not in nanecisto.effective_tags
    assert 'test' in naostro.effective_tags
    assert 'test' in nanecisto.effective_tags
