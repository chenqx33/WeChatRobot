from wcferry import WxMsg, Wcf
import re
from plugin.base_plugin import PluginFather
from plugin.stage_enum import StageEnum
from plugin.action_enum import ActionEnum

from plugin.plugin_context import PluginContext

import logging
class AuthPlugin(PluginFather):
    def __init__(self):
        super().__init__(-1, [StageEnum.PRE_PROCESS], False)

    def do_handle(self, plugin_context: PluginContext, wcf: Wcf) -> None:
        msg = plugin_context.msg
        if msg.content.startswith("/auth") and not msg.from_group():
            if msg.content.endswith("1818"):
                self.admins.append(msg.sender)
                logging.info(f' admins:{self.admins}')
                plugin_context.action = ActionEnum.BREAK
                plugin_context.result = "start success"
                return
            logging.info(f' admins:{self.admins}')
            plugin_context.action = ActionEnum.BREAK

