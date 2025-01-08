from wcferry import WxMsg, Wcf
import re
from plugin.base_plugin import PluginFather
from plugin.stage_enum import StageEnum
from plugin.action_enum import ActionEnum

from plugin.plugin_context import PluginContext


class SystemPlugin(PluginFather):
    def __init__(self):
        super().__init__(-1, [StageEnum.PRE_PROCESS], True)
        self.is_open = True


    def do_handle(self, msg: WxMsg, wcf: Wcf) -> PluginContext:
        if msg.content.startswith("/stop") and not msg.from_group():
            self.is_open = False
            return PluginContext(msg, ActionEnum.BREAK, "stop success")

        if msg.content.startswith("/start") and not msg.from_group():
            self.is_open = True
            return PluginContext(msg, ActionEnum.BREAK, "start success")

        return PluginContext(msg, ActionEnum.CONTINUE, "")
