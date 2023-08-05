from ktdk.core.tasks import Task
from tests.utils import TaskUtils, TestUtils


def assert_task(task, **params):
    params = {**TaskUtils.EMPTY, **params}
    assert params['name'] == task.name
    assert params['desc'] == task.desc


def test_empty_constructor():
    task = Task()
    assert_task(task)


def test_task_with_name_desc():
    task = Task(name='task01', desc='task01 desc')
    assert_task(task, name='task01', desc='task01 desc')


def test_with_all_constructor_params():
    params = TaskUtils.get_params()
    task = TaskUtils.create_task(**params)
    assert_task(task, **params)


def test_add_one_child_task():
    child_task = TaskUtils.create_task()
    task = TaskUtils.create_task()
    task.add_task(child_task)
    assert task.tasks
    assert child_task in task.tasks
    assert child_task.parent == task


def test_add_multiple_children_tasks():
    ch_tasks = [TaskUtils.create_task() for _ in range(5)]
    task = TaskUtils.create_task()
    task.add_task(*ch_tasks)
    for child in ch_tasks:
        assert child.parent == task
        assert child in task.tasks

