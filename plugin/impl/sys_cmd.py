from wcferry import WxMsg, Wcf
import re
from plugin.base_plugin import PluginFather
from plugin.stage_enum import StageEnum
from plugin.action_enum import ActionEnum

from plugin.plugin_context import PluginContext
from config.configuration import set_global_flag

class SystemPlugin(PluginFather):
    def __init__(self):
        super().__init__(-1, [StageEnum.PRE_PROCESS], True)


    def do_handle(self, plugin_context: PluginContext, wcf: Wcf) -> None:
        msg = plugin_context.msg
        if msg.content.startswith("/stop") and not msg.from_group():
            set_global_flag(False)
            plugin_context.action = ActionEnum.BREAK
            plugin_context.result = "stop success"
            return

        if msg.content.startswith("/start") and not msg.from_group():
            set_global_flag(True)
            plugin_context.action = ActionEnum.BREAK
            plugin_context.result = "start success"
            return
