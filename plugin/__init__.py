from .plugin_managment import PluginManager
from .base_plugin import PluginFather
from .impl.ban_plugin import BanPlugin
from .impl.auth_plugin import AuthPlugin
from .impl.sys_cmd import SystemPlugin
from .impl.safe import SafePlugin


# 其他插件模块...

plugin_manager = PluginManager()