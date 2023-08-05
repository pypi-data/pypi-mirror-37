"""
Main KTDK module
"""
import json
import logging
from typing import Callable, List

import requests

from ktdk import log_config
from ktdk.core import Result, Task, Test
from ktdk.runtime import Context
from ktdk.runtime.stat import stat_test
from ktdk.utils import unique_name

log_config.load_config()

log = logging.getLogger(__name__)

DEFAULTS_CONFIG = {
    'test_files': 'test_files',
    'workspace': 'workspace',
    'submission': 'submission',
    'results': None,
    'timeout': 60,  # seconds
    'suite_timeout': 3600,  # seconds
    'tags': [],
    'webhook_url': None,
    'webhook_token': None,
    'safe_suffixes': False,
    'cpp_compiler': 'clang++',
    'cpp_compiler_flags': '-std=c++17 -Wall -Wextra -pedantic',
    'c_compiler': 'clang',
    'c_compiler_flags': '-std=c99 -Wall -Wextra -pedantic',
    'valgrind_penalization': 0.7,
    'dump_result': False,
    'clang_format_style': 'pb161',
    'clang_format_styles_dir': '/tmp/check_style'
}


def dump_to_file(context: Context, file_name: str, what):
    """Dumps content to the file
    Args:
        context(Context): Context instance
        file_name(str): File name
        what: What should be written to the file
    """
    file_name = unique_name(file_name, context=context) + ".json"
    context.paths.save_result(file_name, json.dumps(what))


class KTDK(object):
    """
    Main class of the KTDK, it holds configuration, the suite (root of the )
    """
    instance = None

    @staticmethod
    def get_instance(**config):
        if KTDK.instance is None:
            log.debug(f"[KTDK] Instance config: {config}")
            KTDK.instance = KTDK(**config)
        return KTDK.instance

    def __init__(self, **config):
        """Creates instance of the KTDK suite
        Args:
            **config:
        """
        self.suite = Test(name='suite', tags=['suite'])
        self._post_actions: List[Callable] = []
        defaults = self.__config_defaults()
        self.config = {**defaults, **config}
        if self.config.get('devel'):
            for key, val in self.config.items():
                log.debug(f"[KTDK] Config: {key}={val}")

    def register_tags(self, *tags):
        if 'registered_tags' not in self.config:
            self.config['registered_tags'] = []
        self.config['registered_tags'].extend(tags)

    @property
    def post_actions(self) -> List[Callable]:
        """Gets all the post actions
        Returns(List[Callable]): List of all post actions
        """
        return self._post_actions

    def add_post_action(self, post_action: Callable):
        """Adds post action - action that will be executed after suite has been executed
        Args:
            post_action(Callable): Function that takes KTDK instance as the 1st arg and
                                    the Context as the 2nd arg

        """
        self._post_actions.append(post_action)

    def post_action(self):
        """Decorator that defines the post action
        Returns(Callable): Decorated Callable
        """

        def __post_action(func):
            self.add_post_action(func)

        return __post_action

    def create_context(self) -> Context:
        """Creates context from the configuration
        Returns(Context): The context instance
        """
        context = Context(suite_config=self.config, test_config={})

        return context

    def invoke(self) -> Result:
        """Invokes the KTDK suite
        Returns(Result): Overall result of the suite
        """
        return self.run()

    def run(self) -> Result:
        """Runs whole KTDK suite adn saves result

        Returns(Result): Overall result of the suite
        """
        context = self.create_context()
        log.info(f"[CTX] Created: {context}")
        suite_runner = self.suite.runner.get_instance(context=context)
        suite_result = suite_runner.invoke()
        self.__dump_required_files(context)
        self.__invoke_post_actions(context)
        return suite_result

    @property
    def stats(self) -> dict:
        return stat_test(self.suite)

    @staticmethod
    def __config_defaults():
        return DEFAULTS_CONFIG

    def __invoke_post_actions(self, context: Context):
        for post_action in self.post_actions:
            post_action(self, context)

        self.__send_notification(context=context)

    def __dump_required_files(self, context):
        if context.config['dump_result']:
            dump_to_file(context, 'suite-result', self.suite.to_dict())
        dump_to_file(context, 'suite-stats', self.stats)
        dump_to_file(context, 'suite-files', context.config['work_files'])

    def __send_notification(self, context: Context):
        webhook_url = context.config['webhook_url']
        if webhook_url:
            params = dict(url=webhook_url, data=json.dumps(self.stats))
            if context.config['webhook_token']:
                params['headers'] = {'Authorization': 'Bearer ' + context.config['webhook_token']}
            requests.post(**params)
