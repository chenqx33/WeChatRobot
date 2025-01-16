from wcferry import WxMsg

from plugin.action_enum import ActionEnum
from model.func_base import BaseBot

class PluginContext(object):
    def __init__(self, msg: WxMsg, action: ActionEnum, result: str, chat: BaseBot):
        self.msg = msg
        self.action = action
        self.result = result
        self.chat = chat

    def is_end(self) -> bool:
        return self.action == ActionEnum.BREAK