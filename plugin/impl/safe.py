from wcferry import WxMsg, Wcf
import re
from plugin.base_plugin import PluginFather
from plugin.stage_enum import StageEnum
from plugin.action_enum import ActionEnum

from plugin.plugin_context import PluginContext
from config.configuration import set_global_flag
import time
import random

class SafePlugin(PluginFather):
    def __init__(self):
        super().__init__(-1, [StageEnum.POST_PROCESS], False)


    def do_handle(self, plugin_context: PluginContext, wcf: Wcf) -> None:
        time.sleep(random.uniform(2, 5))
