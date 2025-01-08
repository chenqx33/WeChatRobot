from .plugin_managment import PluginManager
from .base_plugin import PluginFather

import pkgutil
import importlib

def import_submodules(package, recursive=False):
    """Import all submodules of a package."""
    importlib.invalidate_caches()
    submodules = []
    for loader, name, is_pkg in pkgutil.iter_modules(package.__path__):
        full_name = package.__name__ + '.' + name
        submodule = importlib.import_module(full_name)
        submodules.append(submodule)
        if recursive and is_pkg:
            submodules.extend(import_submodules(submodule))
    return submodules

import_submodules(importlib.import_module('impl', package='.impl'))


# 其他插件模块...

plugin_manager = PluginManager()