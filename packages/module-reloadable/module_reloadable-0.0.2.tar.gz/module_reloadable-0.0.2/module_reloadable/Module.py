""" module_reloadable.Module 181016_2130
"""
import importlib
import re


class Module():

    def __init__(self, module_name, ignore_import_error=False):
        self.module_name = module_name
        self.m = None
        try:
            self.m = importlib.import_module(self.module_name)
        except ImportError:
            if not ignore_import_error: raise

    def __cleanup_module_attrs(self):
        for attr_ in dir(self.m):
            if not re.search("^__[^_]+__$", attr_):
                delattr(self.m, attr_)

    def reload(self):
        # cleanup module attributes
        self.__cleanup_module_attrs()
        # reload module
        self.m = importlib.reload(self.m)

    def run(self, function_name, *args, **kwargs):
        # get module function
        function_ = getattr(self.m, function_name)
        # run it
        function_(*args, **kwargs)

    def module(self):
        # get module object
        return self.m
