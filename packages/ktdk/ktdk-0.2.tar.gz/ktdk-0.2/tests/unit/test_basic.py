import pytest

from ktdk.utils.basic import BasicObject


@pytest.fixture()
def basic():
    return BasicObject()


def test_basic_object_to_string(basic):
    assert 'BasicObject: ' in basic.__str__()


def test_basic_object_repr(basic):
    assert basic.__repr__() == basic.__str__()
