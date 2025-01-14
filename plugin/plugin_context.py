import logging
from wcferry import WxMsg

from plugin.stage_enum import StageEnum
from plugin.action_enum import ActionEnum
from func_chatgpt import ChatGPT

class PluginContext(object):
    def __init__(self, msg: WxMsg, action: ActionEnum, result: str, chat: ChatGPT):
        self.msg = msg
        self.action = action
        self.result = result
        self.chat = chat

    def is_end(self) -> bool:
        return self.action == ActionEnum.BREAK