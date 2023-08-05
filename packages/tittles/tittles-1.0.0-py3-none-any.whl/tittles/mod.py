""" tittles.mod 171217_1800
"""
import importlib
import re


class Mod():
    """Module reloadable"""
    def __init__(self, module_name, ignore_import_error=False):
        self.module_name = module_name
        self.m = None
        try:
            self.m = importlib.import_module(self.module_name)
        except ImportError:
            if not ignore_import_error:
                raise

    def __cleanup_module_attrs(self):
        for a_ in dir(self.m):
            if not re.search("^__[^_]+__$", a_):
                delattr(self.m, a_)

    def reload(self):
        """Cleanup module attributes and reload module"""
        self.__cleanup_module_attrs()
        self.m = importlib.reload(self.m)

    def run(self, func_name, *args, **kwargs):
        """Run module function"""
        action_ = getattr(self.m, func_name)
        action_(*args, **kwargs)

    def module(self):
        """Returns module object"""
        return self.m
