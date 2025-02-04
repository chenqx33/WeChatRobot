from wcferry import Wcf, WxMsg
import logging
import traceback
from plugin.action_enum import ActionEnum
from plugin.plugin_context import PluginContext
from config.configuration import config

class PluginFather:
    def __init__(self, order: int, actions: list[ActionEnum], admin_plugin: bool):
        self.order = order
        self.actions = actions
        self.admin_plugin = admin_plugin

        self.admins = config.ADMINS

    def handle(self, plugin_context: PluginContext, wcf: Wcf) -> None:
        logging.info(f'{self.__class__.__name__} start')
        msg = plugin_context.msg
        if self.before(msg):
            plugin_context.action = ActionEnum.BREAK
            plugin_context.result = ""
            return
        try:
            self.do_handle(plugin_context, wcf)
        except Exception as e:
            logging.error(f"Receiving message error: {e}")
            traceback.print_exc()
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
