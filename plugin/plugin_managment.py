from plugin.action_enum import ActionEnum
from plugin.base_plugin import PluginFather
import logging
from wcferry import Wcf, WxMsg
from plugin.plugin_context import PluginContext
from plugin.stage_enum import StageEnum


class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.get_plugins()

    def get_plugins(self):
        import plugin
        for subclass in PluginFather.__subclasses__():
            try:
                instance = subclass()
                for action_enum in instance.actions:
                    if self.plugins.get(action_enum) is None:
                        self.plugins[action_enum] = []
                    self.plugins[action_enum].append(instance)
            except Exception as e:
                logging.error(f"plugin {subclass} init failed: {e}")
        for value in self.plugins.values():
            value.sort(key=lambda x: x.order)
        return self.plugins

    def handle(self, msg, stage: StageEnum, wcf: Wcf) -> PluginContext:
        for plugin in self.plugins[stage]:
            plugin_result = plugin.handle(msg, wcf)
            if plugin_result.action == ActionEnum.CONTINUE:
                continue
            else:
                return plugin_result
        return plugin_result
