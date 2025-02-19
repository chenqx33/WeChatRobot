#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging.config
import os
import shutil

import yaml


class Config(object):
    def __init__(self) -> None:
        self.reload()

    def _load_config(self) -> dict:
        pwd = os.path.dirname(os.path.abspath(__file__))
        try:
            with open(f"{pwd}/config.yaml", "rb") as fp:
                yconfig = yaml.safe_load(fp)
        except FileNotFoundError:
            shutil.copyfile(f"{pwd}/config.yaml.template", f"{pwd}/config.yaml")
            with open(f"{pwd}/config.yaml", "rb") as fp:
                yconfig = yaml.safe_load(fp)

        return yconfig

    def reload(self) -> None:
        yconfig = self._load_config()
        logging.config.dictConfig(yconfig["logging"])
        self.GROUPS = yconfig["groups"]["enable"]

        self.CHATGPT = yconfig.get("chatgpt", {})
        self.COZE = yconfig.get("coze", {})
        self.ARK = yconfig.get("ark", {})
        self.ADMINS = yconfig.get("admins", [])

GLOBAL_FLAG = True

def get_global_flag():
    return GLOBAL_FLAG
def set_global_flag(flag):
    global GLOBAL_FLAG
    GLOBAL_FLAG = flag

config = Config()