#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from datetime import datetime

import httpx
from openai import APIConnectionError, APIError, AuthenticationError, OpenAI

from model.func_base import BaseBot


class ARKBot(BaseBot):
    def __init__(self, conf: dict) -> None:
        key = conf.get("key")
        api = conf.get("api")
        proxy = conf.get("proxy")
        prompt = conf.get("prompt")
        self.model = conf.get("model", "deepseek-r1-250120")
        self.LOG = logging.getLogger("ARK")
        if proxy:
            self.client = OpenAI(api_key=key, base_url=api, http_client=httpx.Client(proxy=proxy))
        else:
            self.client = OpenAI(api_key=key, base_url=api)
        self.conversation_list = {}
        self.system_content_msg = {"role": "system", "content": prompt}

    def __repr__(self):
        return 'ARK'

    @staticmethod
    def value_check(conf: dict) -> bool:
        if conf:
            if conf.get("key") and conf.get("api") and conf.get("prompt"):
                return True
        return False

    def get_answer(self, question: str, wxid: str) -> str:
        # wxid或者roomid,个人时为微信id，群消息时为群id
        self.updateMessage(wxid, question, "user")
        rsp = ""
        try:
            logging.info(f'model messages:{self.conversation_list[wxid]}')
            ret = self.client.chat.completions.create(model=self.model,
                                                      messages=self.conversation_list[wxid],
                                                      temperature=1.2)
            rsp = ret.choices[0].message.content
            rsp = rsp[2:] if rsp.startswith("\n\n") else rsp
            rsp = rsp.replace("\n\n", "\n")
            self.updateMessage(wxid, rsp, "assistant")
        except AuthenticationError:
            self.LOG.error("OpenAI API 认证失败，请检查 API 密钥是否正确")
        except APIConnectionError:
            self.LOG.error("无法连接到 OpenAI API，请检查网络连接")
        except APIError as e1:
            self.LOG.error(f"OpenAI API 返回了错误：{str(e1)}")
        except Exception as e0:
            self.LOG.error(f"发生未知错误：{str(e0)}")

        return rsp

    def updateMessage(self, wxid: str, question: str, role: str) -> None:
        now_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        time_mk = "当前时间:"
        # 初始化聊天记录,组装系统信息
        if wxid not in self.conversation_list.keys():
            question_ = [
                self.system_content_msg,
                {"role": "system", "content": "" + time_mk + now_time}
            ]
            self.conversation_list[wxid] = question_

        # 当前问题
        for query_item in question.split(" --> ")[::-1]:
            content_question_ = {"role": role, "content": query_item}
            self.conversation_list[wxid].append(content_question_)

        for cont in self.conversation_list[wxid]:
            if cont["role"] != "system":
                continue
            if cont["content"].startswith(time_mk):
                cont["content"] = time_mk + now_time

        # 只存储10条记录，超过滚动清除
        i = len(self.conversation_list[wxid])
        if i > 10:
            print("滚动清除微信记录：" + wxid)
            # 删除多余的记录，倒着删，且跳过第一个的系统消息
            del self.conversation_list[wxid][2]

    def clean_conversation(self, wxid: str) -> None:
        if wxid in self.conversation_list.keys():
            del self.conversation_list[wxid]
