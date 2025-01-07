from wcferry import Wcf, WxMsg
import logging

from plugin.action_enum import ActionEnum
from plugin.plugin_context import PluginContext


class PluginFather:
    def __init__(self, order: int, actions: list[ActionEnum]):
        self.order = order
        self.actions = actions

    def handle(self, msg: WxMsg, context: PluginContext) -> PluginContext:
        raise NotImplementedError("This method has not been implemented yet.")
