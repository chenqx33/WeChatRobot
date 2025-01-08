from wcferry import WxMsg, Wcf
import re
from plugin.base_plugin import PluginFather
from plugin.stage_enum import StageEnum
from plugin.action_enum import ActionEnum

from plugin.plugin_context import PluginContext


class BanPlugin(PluginFather):
    def __init__(self):
        super().__init__(0, [StageEnum.PRE_PROCESS], True)
        self.black_list = []

    def do_handle(self, plugin_context: PluginContext, wcf: Wcf) -> None:
        msg = plugin_context.msg
        if msg.content.startswith("/ban") and msg.from_group():
            need_ban_wxid = self.get_at_wxid_by_xml(msg.xml, wcf)
            self.black_list.extend(need_ban_wxid)
            plugin_context.action = ActionEnum.BREAK
            plugin_context.result = "ban success"
            return

        if msg.content.startswith("/unban") and msg.from_group():
            need_ban_wxid = self.get_at_wxid_by_xml(msg.xml, wcf)
            self.black_list = [x for x in self.black_list if x not in need_ban_wxid]
            plugin_context.action = ActionEnum.BREAK
            plugin_context.result = "unban success"
            return

        if msg.sender in self.black_list:
            plugin_context.action = ActionEnum.BREAK
            plugin_context.result = ""
            return
        plugin_context.action = ActionEnum.CONTINUE

    def get_at_wxid_by_xml(self, xml_str: str, wcf: Wcf) -> list:
        result = re.search(r"<atuserlist>(.*?)</atuserlist>", xml_str)

        if result:
            self_wxid = wcf.get_self_wxid()
            id_list = result.group(1).split(",")
            id_list = [wxid for wxid in id_list if wxid != self_wxid]
            return id_list
        return []
