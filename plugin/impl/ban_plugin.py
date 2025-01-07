from wcferry import WxMsg, Wcf
import re
from plugin.base_plugin import PluginFather
from plugin.stage_enum import StageEnum
from plugin.action_enum import ActionEnum

from plugin.plugin_context import PluginContext


class BanPlugin(PluginFather):
    def __init__(self):
        super().__init__(-1, [StageEnum.PRE_PROCESS])
        self.black_list = []

    def handle(self, msg: WxMsg, wcf: Wcf) -> PluginContext:
        if msg.content.startswith("/ban") and msg._is_group:
            need_ban_wxid = self.get_at_wxid_by_xml(msg.xml, wcf)
            self.black_list.extend(need_ban_wxid)
            return PluginContext(msg, ActionEnum.BREAK, "ban success")

        if msg.content.startswith("/unban") and msg._is_group:
            need_ban_wxid = self.get_at_wxid_by_xml(msg.xml, wcf)
            self.black_list = [x for x in self.black_list if x not in need_ban_wxid]
            return PluginContext(msg, ActionEnum.BREAK, "unban success")

        if self.black_list[msg.sender]:
            return PluginContext(msg, ActionEnum.BREAK, "")
        return PluginContext(msg, ActionEnum.CONTINUE, "")

    def get_at_wxid_by_xml(self, xml_str: str, wcf: Wcf) -> list:
        result = re.search(r"<atuserlist>(.*?)</atuserlist>", xml_str)

        if result:
            self_wxid = wcf.get_self_wxid()
            id_list = result.group(1).split(",")
            id_list = [wxid for wxid in id_list if wxid != self_wxid]
            return id_list
        return []
