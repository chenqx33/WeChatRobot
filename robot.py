# -*- coding: utf-8 -*-

import logging
import re
import time
from queue import Empty
from threading import Thread

from wcferry import Wcf, WxMsg

from config.configuration import Config
from config.configuration import get_global_flag
from config.configuration import set_global_flag
from func_chatgpt import ChatGPT
from plugin import plugin_manager
__version__ = "39.2.4.0"

from plugin.stage_enum import StageEnum
import traceback


class Robot():
    """个性化自己的机器人
    """

    def __init__(self, config: Config, wcf: Wcf) -> None:
        super().__init__()
        self.wcf = wcf
        self.config = config
        self.LOG = logging.getLogger("Robot")
        self.chat = ChatGPT(self.config.CHATGPT)



    def toChitchat(self, msg: WxMsg) -> str:
        """闲聊，接入 ChatGPT
        """
        q = self.convert_format(msg.content)
        rsp = self.chat.get_answer(q, (msg.roomid if msg.from_group() else msg.sender))
        return rsp

    def processMsg(self, msg: WxMsg, wcf: Wcf) -> None:
        """当接收到消息的时候，会调用本方法。如果不实现本方法，则打印原始消息。
        此处可进行自定义发送的内容,如通过 msg.content 关键字自动获取当前天气信息，并发送到对应的群组@发送者
        群号：msg.roomid  微信ID：msg.sender  消息内容：msg.content
        content = "xx天气信息为："
        receivers = msg.roomid
        self.sendTextMsg(content, receivers, msg.sender)
        """
        plugin_result = plugin_manager.handle(msg, StageEnum.PRE_PROCESS, wcf)
        if plugin_result.is_end():
            if plugin_result.result:
                self.sendTextMsg(plugin_result.result, msg.roomid, msg.sender)
            return

        # 群聊消息
        rsp = ''
        # 不在配置的响应的群列表里，忽略
        if msg.from_group() and (msg.roomid not in self.config.GROUPS or 'all_groups' not in self.config.GROUPS):
            return
        if msg.type == 0x01:  # 文本消息
            rsp = self.toChitchat(msg)  # 闲聊
        else:
            return
        if rsp:
            if msg.from_group():
                self.sendTextMsg(rsp, msg.roomid, msg.sender)
            else:
                self.sendTextMsg(rsp, msg.sender)

    def enableReceivingMsg(self) -> None:
        def innerProcessMsg(wcf: Wcf):
            while wcf.is_receiving_msg():
                try:
                    msg = wcf.get_msg()
                    if not get_global_flag() and not msg.content == '/start':
                        continue
                    self.LOG.info(msg)
                    self.processMsg(msg, wcf)
                except Empty:
                    continue  # Empty message
                except Exception as e:
                    self.LOG.error(f"Receiving message error: {e}")
                    traceback.print_exc()

        self.wcf.enable_receiving_msg()
        Thread(target=innerProcessMsg, name="GetMessage", args=(self.wcf,), daemon=True).start()

    def sendTextMsg(self, msg: str, receiver: str, at_list: str = "") -> None:
        """ 发送消息
        :param msg: 消息字符串
        :param receiver: 接收人wxid或者群id
        :param at_list: 要@的wxid, @所有人的wxid为：notify@all
        """
        self.LOG.info(f'mock send text: {msg}')
        if True:
            return
        # msg 中需要有 @ 名单中一样数量的 @
        ats = ""
        if at_list:
            if at_list == "notify@all":  # @所有人
                ats = " @所有人"
            else:
                wxids = at_list.split(",")
                for wxid in wxids:
                    # 根据 wxid 查找群昵称
                    ats += f" @{self.wcf.get_alias_in_chatroom(wxid, receiver)}"

        # {msg}{ats} 表示要发送的消息内容后面紧跟@，例如 北京天气情况为：xxx @张三
        if ats == "":
            self.LOG.info(f"To {receiver}: {msg}")
            self.wcf.send_text(f"{msg}", receiver, at_list)
        else:
            self.LOG.info(f"To {receiver}: {ats}\r{msg}")
            self.wcf.send_text(f"{ats}\n\n{msg}", receiver, at_list)



    def keepRunningAndBlockProcess(self) -> None:
        """
        保持机器人运行，不让进程退出
        """
        while True:
            time.sleep(1)

    def convert_format(self, input_str):
        if '\n- - - - - - - - - - - - - - -\n' not in input_str:
            return re.sub(r"@.*?[\u2005|\s]", "", input_str).strip()

        # 分割字符串为上下两部分
        parts = input_str.split('\n- - - - - - - - - - - - - - -\n')

        # 从第一部分提取xxx
        first_part = re.sub(r"@.*?[\u2005|\s]", "", parts[0]).strip()
        content = first_part.split('：')[1].strip()[:-1]

        # 获取第二部分的yyy
        second_part = re.sub(r"@.*?[\u2005|\s]", "", parts[1]).strip()

        if second_part:
            # 组合成新格式
            return f"{second_part} --> {content}"

        return content
