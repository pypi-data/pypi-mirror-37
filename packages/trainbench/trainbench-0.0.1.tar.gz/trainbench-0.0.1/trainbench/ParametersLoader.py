import importlib


class ModuleLoader:
    """
    Dynamically handles "add-on" modules (readers and writers) loading.
    """

    def __init__(self):
        super().__init__()
        self.module = None

    @staticmethod
    def load_module(path, name):
        return getattr(importlib.import_module(path + name, __package__), name)

    def load_reader(self, name):
        self.module = self.load_module('', name)

    def params(self):
        return self.module.parameters
