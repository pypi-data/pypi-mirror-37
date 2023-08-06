from importlib import import_module

from django.conf import settings

from .exceptions import InvalidConfigurationError


def _load_backend_class():
    backend = getattr(settings, 'SETTY_BACKEND', None)
    if backend is None:
        raise InvalidConfigurationError('The SETTY_BACKEND setting needs to be defined.')

    return getattr(getattr(import_module('setty'), 'backend'), backend)


class SettySettings:
    """
    Wrapper class used for accessing/updating setty settings
    """

    def __init__(self):
        super().__setattr__('__backend', _load_backend_class())

    def __getattr__(self, key):
        return super().__getattribute__('__backend').get(self, key)

    def __setattr__(self, key, value):
        super().__getattribute__('__backend').set(self, key, value)

    def __dir__(self):
        return [setting.name for setting in self.__getattribute__('__backend').get_all(self)]
