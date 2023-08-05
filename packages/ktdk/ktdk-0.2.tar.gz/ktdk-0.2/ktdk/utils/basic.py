"""
Basic object
"""
from json import JSONEncoder


class BasicObject(JSONEncoder):
    """ Base class from which all entities are going to inherit
    """

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return str(self.__class__.__name__) + ": " + str(self.default(o=self))

    def default(self, o):  # pylint: disable=method-hidden
        props = o.__dict__
        if hasattr(o, 'to_dict'):
            props = o.to_dict()
        return props
