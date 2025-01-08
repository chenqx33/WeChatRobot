from wcferry import WxMsg, Wcf
import re
from plugin.base_plugin import PluginFather
from plugin.stage_enum import StageEnum
from plugin.action_enum import ActionEnum

from plugin.plugin_context import PluginContext


class AuthPlugin(PluginFather):
    def __init__(self):
        super().__init__(-1, [StageEnum.PRE_PROCESS], False)

    def do_handle(self, msg: WxMsg, wcf: Wcf) -> PluginContext:
        if msg.content.startswith("/auth") and not not msg.from_group():
            if msg.content.endswith("/1818"):
                self.admins.append(msg.sender())
                return PluginContext(msg, ActionEnum.BREAK, "start success")
            return PluginContext(msg, ActionEnum.BREAK, "")

        return PluginContext(msg, ActionEnum.CONTINUE, "")
