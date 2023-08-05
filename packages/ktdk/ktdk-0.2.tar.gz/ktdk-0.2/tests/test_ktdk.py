from ktdk import KTDK
from ktdk.runtime.runners import Runner

import pytest


@pytest.fixture()
def runner(mocker):
    runner = mocker.Mock(spec=Runner)
    return runner


def test_instance():
    assert KTDK.instance is None
    assert KTDK.get_instance() is not None
    assert KTDK.instance is not None


def test_config():
    ktdk = KTDK.get_instance()
    assert (ktdk.config['test_files'] == 'test_files')
    assert (ktdk.config['workspace'] == 'workspace')
    assert (ktdk.config['submission'] == 'submission')


