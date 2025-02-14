#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from cozepy import COZE_CN_BASE_URL

from model.func_base import BaseBot

coze_api_base = COZE_CN_BASE_URL

from cozepy import Coze, TokenAuth, Message, ChatEventType

user_id = 'mock_user_id'


class CozeBot(BaseBot):
    def __init__(self, conf: dict) -> None:
        self.bot_id = conf.get("bot_id")
        self.coze_api_token = conf.get("coze_api_token")
        self.LOG = logging.getLogger("Code")
        self.conversation_list = {}
        self.coze = Coze(auth=TokenAuth(token=self.coze_api_token), base_url=coze_api_base)

    def get_answer(self, question: str, wxid: str) -> str:
        # wxid或者roomid,个人时为微信id，群消息时为群id
        self.updateMessage(wxid, question, "user")
        rsp = ""
        try:
            logging.info(f'model messages:{self.conversation_list[wxid]}')
            for event in self.coze.chat.stream(
                    bot_id=self.bot_id, user_id=user_id,
                    additional_messages=[Message.build_user_question_text(question)]
            ):
                if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                    message = event.message
                    rsp += message.content
            rsp = rsp.strip()
            self.updateMessage(wxid, rsp, "assistant")
        except Exception as e0:
            self.LOG.error(f"发生未知错误：{str(e0)}")

        return rsp

    def updateMessage(self, wxid: str, question: str, role: str) -> None:
        # 初始化聊天记录,组装系统信息
        if wxid not in self.conversation_list.keys():
            question_ = [
            ]
            self.conversation_list[wxid] = question_

        # 当前问题
        for query_item in question.split(" --> ")[::-1]:
            if role == "user":
                content_question_ = Message.build_user_question_text(query_item)
            else:
                content_question_ = Message.build_assistant_answer(query_item)
            self.conversation_list[wxid].append(content_question_)

        # 只存储10条记录，超过滚动清除
        i = len(self.conversation_list[wxid])
        if i > 10:
            print("滚动清除微信记录：" + wxid)
            # 删除多余的记录，倒着删，且跳过第一个的系统消息
            del self.conversation_list[wxid][0]

    def clean_conversation(self, wxid: str) -> None:
        if wxid in self.conversation_list.keys():
            del self.conversation_list[wxid]
