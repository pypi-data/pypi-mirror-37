"""
Main cli module
"""
import json
import logging

import click

from ktdk.cli.manager import CliManager
from ktdk.cli.printer import print_tests
from ktdk.utils.flatters import flatten_tests

log = logging.getLogger(__name__)


@click.group(help='KTDK Cli tool')
@click.version_option('1.0')
def main_cli():
    pass


@main_cli.group('tests', help='Test management namespace')
def tests_cli():
    pass


@tests_cli.command('list', help='Lists all the tests')
@click.option('-f', '--full', default=False, is_flag=True, help='Show full test definition')
@click.option('-T', '--test-files', help='Test files location', required=False)
@click.option('-p', '--param', multiple=True,
              help="Override default parameters (format: name=value)")
def cli_tests_list(full, **kwargs):
    cli_manager = CliManager()
    ktdk = cli_manager.create_context(**kwargs)
    tests = flatten_tests(ktdk.suite)
    print("Number of tests: " + str(len(tests)))
    print_tests(tests, full=full)


@main_cli.command('execute', help='Executes the KTDK')
@click.option('--timeout', default=60, help='Timeout for each command to run')
@click.option('-D', '--devel', is_flag=True, default=False, help='Whether to run in devel mode')
@click.option('-T', '--test-files', help='Test files location', required=False)
@click.option('-S', '--submission', help='Submission files location', required=False)
@click.option('-W', '--workspace', help='Workspace location', required=False)
@click.option('-R', '--results', help='Results location', required=False)
@click.option('--clang-format-style', help='Clang format style default (pb161)', required=False)
@click.option('--clang-format-styles-dir', required=False,
              help='Clang format style templates dirs, (/tmp/style_check)')
@click.option('--dump-result', help='Dump result', required=False)
@click.option('-p', '--param', multiple=True,
              help="Override default parameters (format: name=value)")
def execute(param=None, **kwargs):
    params = {}
    if param:
        override = {item[0]: item[1] for item in param.split('=')}
        params.update(override)
    params.update({k: v for k, v in kwargs.items() if v is not None})
    log.info(f"[EXEC] Params: {params}")
    cli_manager = CliManager(**params)
    ktdk = cli_manager.create_context(**params)
    ktdk.invoke()
    stat = ktdk.stats
    print(json.dumps(stat, indent=2))


if __name__ == '__main__':
    main_cli()
