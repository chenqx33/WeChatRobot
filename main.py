#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import signal

from wcferry import Wcf

from config.configuration import Config
from plugin import PluginManager
from robot import Robot, __version__


def main():
    config = Config()
    wcf = Wcf(debug=False)

    def handler(sig, frame):
        wcf.cleanup()  # 退出前清理环境
        exit(0)

    signal.signal(signal.SIGINT, handler)

    robot = Robot(config, wcf)
    logging.info(f"WeChatRobot【{__version__}】成功启动···")

    # 机器人启动发送测试消息
    robot.sendTextMsg("机器人启动成功！", "filehelper")

    # 接收消息
    robot.enableReceivingMsg()  # 加队列

    # 让机器人一直跑
    robot.keepRunningAndBlockProcess()

def main_test():
    plugin_manager = PluginManager()
    print(plugin_manager.get_plugins())
if __name__ == "__main__":
    main()
