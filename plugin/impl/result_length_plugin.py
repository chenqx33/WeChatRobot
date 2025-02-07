from wcferry import WxMsg, Wcf
from plugin.base_plugin import PluginFather
from plugin.stage_enum import StageEnum
from plugin.action_enum import ActionEnum
from plugin.plugin_context import PluginContext

import logging

class ResultLengthPlugin(PluginFather):
    def __init__(self):
        # 设置为最后执行，在 POST_PROCESS 阶段
        super().__init__(999, [StageEnum.POST_PROCESS], False)
        self.max_length = 200

    def do_handle(self, plugin_context: PluginContext, wcf: Wcf) -> None:
        if plugin_context.result and isinstance(plugin_context.result, str):
            if len(plugin_context.result) > self.max_length:
                logging.info(f'Result too long ({len(plugin_context.result)} chars), truncating to {self.max_length} chars')
                plugin_context.result = plugin_context.result[:self.max_length] + '...'