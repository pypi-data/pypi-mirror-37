import pytest

from ktdk.runtime.context import Context


@pytest.fixture()
def context():
    return Context(
        suite_config={'global': 0},
        test_config={'test': 10},
        task_config={'task': 100}
    )


def test_context_init():
    context = Context({})
    assert not context.config.all


def test_context_config(context):
    assert context.config['global'] == 0
    assert context.config['test'] == 10
    assert context.config['task'] == 100


def test_context_clone_no_test(context):
    context.config.set_suite('global', 1)
    context.config.set_test('test', 11)
    context.config.set_task('task', 101)

    assert context.config['global'] == 1
    assert context.config['test'] == 11
    assert context.config['task'] == 101
    clone = context.clone()
    assert id(context.config.test) == id(clone.config.test)
    assert clone.config['global'] == 1
    assert clone.config['test'] == 11
    assert clone.config['task'] == 101
    clone.config.set_task('task', 102)
    assert clone.config['task'] == 102
    clone.config.set_test('test', 12)
    assert context.config['task'] == 101
    assert context.config['test'] == 12


def test_context_clone_test(context):
    context.config.set_suite('global', 1)
    context.config.set_test('test', 11)
    context.config.set_task('task', 101)

    assert context.config['global'] == 1
    assert context.config['test'] == 11
    assert context.config['task'] == 101
    clone = context.clone(clone_test=True)
    assert clone.config['global'] == 1
    assert clone.config['test'] == 11
    assert clone.config['task'] == 101
    clone.config.set_task('task', 102)
    assert clone.config['task'] == 102
    clone.config.set_test('test', 12)
    assert context.config['task'] == 101
    assert context.config['test'] == 11


def test_context_clone_test2(context):
    task_clone = context.clone()
    task_clone.config.set_test('test', 1000)
    assert context.config['test'] == 1000
    clone = context.clone(clone_test=True)
    assert clone.config['test'] == 1000
    clone.config.set_test('test', 12)
    assert clone.config['test'] == 12
    clone2 = clone.clone(clone_test=True)
    assert context.config['test'] == 1000
    assert clone2.config['test'] == 12


def test_context_add_test_dict(context):
    context.config.set_task('comp', {'hello': 'world'})
    context.config.add_task('comp', {'hi': 'sky'})
    assert 'hello' in context.config['comp']
    assert 'hi' in context.config['comp']
    assert 'world' == context.config['comp']['hello']
    assert 'sky' == context.config['comp']['hi']


def test_context_add_test_list(context):
    context.config.set_task('comp', ['hello'])
    context.config.add_task('comp', ['hi'])
    assert 'hello' in context.config['comp']
    assert 'hi' in context.config['comp']
