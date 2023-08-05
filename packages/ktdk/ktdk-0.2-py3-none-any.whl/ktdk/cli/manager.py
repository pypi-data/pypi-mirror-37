import importlib
import importlib.machinery
import importlib.util
import logging
import os
import sys
from pathlib import Path

from ktdk import KTDK

log = logging.getLogger(__name__)


class CliManager(object):
    def __init__(self, **kwargs):
        self.config = {**load_vars(), **kwargs}

    @property
    def workspace_dir(self) -> Path:
        return Path(self.config['workspace']).absolute()

    @property
    def test_files_dir(self) -> Path:
        return Path(self.config['test_files']).absolute()

    @property
    def submission_dir(self) -> Path:
        return Path(self.config['submission']).absolute()

    @property
    def results_dir(self) -> Path:
        return Path(self.config['results']).absolute()

    def load_project_files(self):
        module_path = self.test_files_dir / 'kontr_tests'
        sys.path.insert(0, str(module_path))
        path = module_path / self.config.get('entry_point')
        return _import_module_files('test_files', path)

    def get_ktdk(self, **kwargs):
        config = {**self.config, **kwargs}
        log.debug(f"[CFG] Config: {config}")
        ktdk = KTDK.get_instance(**config)
        return ktdk

    def create_context(self, **kwargs):
        ktdk = self.get_ktdk(**kwargs)
        self.load_project_files()
        return ktdk


def _load_var(dictionary: dict, name: str, default=None) -> dict:
    dictionary[name] = os.getenv(f'KTDK_{name.upper()}', default)
    return dictionary


def load_vars() -> dict:
    dictionary = {}
    _load_var(dictionary, 'workspace', '/tmp/workspace')
    _load_var(dictionary, 'test_files', '/tmp/test_files')
    _load_var(dictionary, 'submission', '/tmp/submission')
    _load_var(dictionary, 'results', '/tmp/results')
    _load_var(dictionary, 'entry_point', 'instructions.py')
    _load_var(dictionary, 'webhook_url')
    _load_var(dictionary, 'webhook_token')
    _load_var(dictionary, 'test_timeout', 60)
    _load_var(dictionary, 'suite_timeout', 3600)
    _load_var(dictionary, 'suite_id')
    return dictionary


def _import_module_files(module_name: str, path: Path):
    full_path = str(path)
    loader = importlib.machinery.SourceFileLoader(module_name, full_path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    log.info(f"[CLI] Loading module: {mod}")
    return mod
