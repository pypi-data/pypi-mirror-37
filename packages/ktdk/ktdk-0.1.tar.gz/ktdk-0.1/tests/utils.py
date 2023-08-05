import string
from random import choice

from ktdk import Context
from ktdk.core.tasks import Task
from ktdk.core.tests import Test

ALPHABET = string.ascii_letters + string.digits


def get_test_context(**kwargs):
    params = {**kwargs}
    if params.get('suite_config'):
        params['suite_config']['devel'] = True
    return Context(**params)


def random_string(length=10, alpha=ALPHABET):
    return ''.join(choice(alpha) for i in range(length))


class TestUtils(object):
    EMPTY = {
        'name': 'test',
        'desc': None,
        'tags': set(),
        'tests': [],
        'before': [],
        'after': [],
    }

    @staticmethod
    def get_params(**params):
        defaults = {
            'name': random_string(alpha=string.ascii_lowercase),
            'desc': random_string(),
            'tags': ['naostro', 'generic', 'stylecheck'],
        }
        return {**TestUtils.EMPTY, **defaults, **params}

    @staticmethod
    def create_test(**params):
        params = TestUtils.get_params(**params)
        return Test(**params)

    @staticmethod
    def construct_test(**params):
        params = TestUtils.get_params(**params)
        return Test(**params)


class TaskUtils:
    EMPTY = dict(name='task', desc=None)

    @staticmethod
    def get_params(**params):
        defaults = {
            'name': random_string(alpha=string.ascii_lowercase),
            'desc': random_string(),
        }
        return {**TaskUtils.EMPTY, **defaults, **params}

    @staticmethod
    def create_task(**params):
        params = TaskUtils.get_params(**params)
        return Task(**params)
