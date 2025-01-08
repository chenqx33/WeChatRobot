from wcferry import Wcf, WxMsg
import logging

from plugin.action_enum import ActionEnum
from plugin.plugin_context import PluginContext


class PluginFather:
    def __init__(self, order: int, actions: list[ActionEnum], admin_plugin: bool):
        self.order = order
        self.actions = actions
        self.admin_plugin = admin_plugin
        self.admins = []

    def handle(self, plugin_context: PluginContext, wcf: Wcf) -> None:
        logging.info(f'{self.__class__.__name__} start')
        msg = plugin_context.msg
        if self.before(msg):
            plugin_context.action = ActionEnum.BREAK
            plugin_context.result = ""
            return
        self.do_handle(msg, wcf)
        # after()


    def do_handle(self, plugin_context: PluginContext, wcf: Wcf) -> None:
        raise NotImplementedError("This method has not been implemented yet.")

    def before(self, msg: WxMsg) -> bool:
        # 权限校验
        if not self.check_permission(msg):
            logging.info(f'{self.__class__.__name__} no permission')
            return False
        return False

    def check_permission(self, msg: WxMsg):
        if self.admin_plugin and msg.sender not in self.admins:
            return False
        return True
