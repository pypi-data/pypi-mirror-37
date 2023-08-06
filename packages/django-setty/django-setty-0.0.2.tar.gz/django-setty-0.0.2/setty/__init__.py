from django.utils.functional import LazyObject


class LazyConfig(LazyObject):
    def _setup(self):
        from .wrapper import SettySettings
        self._wrapped = SettySettings()


config = LazyConfig()
