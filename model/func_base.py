from wcferry import WxMsg


class BaseBot():
    def toChitchat(self, msg: WxMsg) -> str:
        """闲聊，接入 ChatGPT
        """
        return ""

    def get_answer(self, question: str, wxid: str) -> str:
        """获取答案
        """
        return ""

    def clean_conversation(self, wxid: str) -> None:
        """清理会话
        """
        pass
