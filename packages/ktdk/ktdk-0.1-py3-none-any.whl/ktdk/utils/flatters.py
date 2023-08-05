from typing import List


def flatten_collection(obj, collection: str, include_self=True):
    """Flattens any collection (tree) to list
    Args:
        include_self: Whether to include the root
        obj: Root element
        collection(str): Collection name (example: tests, tasks)
    Returns(List): List of all elements in the tree
    """
    if obj is None:
        return []
    result = [obj] if include_self else []
    for t in getattr(obj, collection):
        result.extend(flatten_collection(t, collection))
    return result


def flatten_tests(test, include_self: bool = True) -> List:
    """Flattens all the tests
    Args:
        include_self(bool): Whether to include root test
        test(Test): Root test
    Returns(List[Test]): List of all tests
    """
    if test is None:
        return []
    result = [test] if include_self else []
    for t in test.tests:
        result.extend(flatten_tests(t))
    return flatten_collection(test, 'tests', include_self=include_self)


def flatten_tasks(test) -> List:
    """Flatten all the tasks in the tests
    Args:
        test(Test): Root test
    Returns(List[Task]): Tasks
    """
    result = []
    for task in test.tasks:
        result.extend(flatten_collection(task, 'tasks'))
    return result


def flatten_all_tasks(test) -> List:
    """Flatten all the tasks in all the tests
    Args:
        test(Test): Root test
    Returns(List[Task]): Tasks
    """
    result = []
    all_tests = flatten_tests(test=test)
    for selected_test in all_tests:
        result.extend(flatten_tasks(selected_test))
    return result
