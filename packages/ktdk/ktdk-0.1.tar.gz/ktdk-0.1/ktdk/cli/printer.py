from typing import List

from ktdk import Test
from ktdk.utils.flatters import flatten_tasks


def print_tests(tests: List[Test], **kwargs):
    for i, test in enumerate(tests):
        print(f"{i + 1}: ", end='')
        if kwargs.get('full', False):
            print(test)
        else:
            print(f"{test.namespace} (P: {test.points} "
                  f") (T: {test.effective_tags})")
        print_tasks(test, test_counter=i, **kwargs)


def print_tasks(test: Test, test_counter=0, **kwargs):
    tasks = flatten_tasks(test)

    for i, task in enumerate(tasks):
        print(f"\t [TASK] {test_counter + 1}.{i+1}: ", end='')
        if kwargs.get('full', False):
            print(task)
        else:
            print(f"{task.namespace}")
