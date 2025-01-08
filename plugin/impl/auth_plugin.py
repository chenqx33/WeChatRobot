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

    def do_handle(self, msg: WxMsg, wcf: Wcf) -> PluginContext:
        if msg.content.startswith("/auth") and not msg.from_group():
            if msg.content.endswith("1818"):
                self.admins.append(msg.sender)
                logging.info(f' admins:{self.admins}')
                return PluginContext(msg, ActionEnum.BREAK, "start success")
            logging.info(f' admins:{self.admins}')
            return PluginContext(msg, ActionEnum.BREAK, "")

        return PluginContext(msg, ActionEnum.CONTINUE, "")
