import json
import re
import requests
import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from plugins import *



@plugins.register(
    name="coze",
    desire_priority=99,
    hidden=True,
    desc="coze",
    version="1.1",
    author="masterke",
)
class coze(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[chajian] inited")
        self.config = super().load_config()

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type != ContextType.TEXT:
            return
        reply = None
        if os.path.exists('config.json'):
            config_path = os.path.join(os.path.dirname(__file__), "config.json")
            with open(config_path, 'r') as file:
                config_data = json.load(file)
            apiUrl = config_data['apiUrl']
            apiKey = config_data['apiKey']
            channelId = config_data['channelId']
            createImgPrefix = config_data['createImgPrefix']
        else:
            text = "请先配置config.json文件"
            reply = Reply(ReplyType.ERROR, text)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS

        query = e_context["context"].content.strip()
        if query.startswith(createImgPrefix):
            try:
                header = {
                    "Content-Type": "application/json",
                    "Authorization": apiKey
                    }
                data = {
                    "channelId": channelId,
                    "messages": [
                        {
                        "role":"user",
                        "content":query
                        }
                        ],
                    "stream": False
                    }
                json_data = json.dumps(data)
                if apiKey:
                    results = requests.post(apiUrl, data=json_data, headers=header)
                    if results.status_code == 200:
                        data_string = results.json()
                        print(data_string)
                        coze_reply = data_string["choices"][0]["message"]["content"]
                        def contains_img(text):
                            # 正则表达式匹配http或https开头的URL
                            pattern = re.compile(r'https?://\S+')
                            # 检查文本是否包含匹配的URL
                            return pattern.search(text) is not None
                        if contains_img(coze_reply):
                            url_pattern = re.compile(r'!\[.*?\]\((.*?)\)')
                            # 使用findall()函数查找所有匹配的URL
                            urls = url_pattern.findall(coze_reply)
                            img_url = urls[0] if urls else None
                            logger.info(img_url)
                            reply = Reply(ReplyType.IMAGE_URL, img_url)
                            e_context["reply"] = reply
                            e_context.action = EventAction.BREAK_PASS
                        else:
                            logger.info(coze_reply)
                            reply = Reply(ReplyType.TEXT, coze_reply)
                            e_context["reply"] = reply
                            e_context.action = EventAction.BREAK_PASS
                    else:
                        requests_error_reply = (f"创建画图任务失败😭\n状态码：{results.status_code}!")
                        reply = Reply(ReplyType.ERROR, requests_error_reply)
                        e_context["reply"] = reply
                        e_context.action = EventAction.BREAK_PASS
            except Exception as e:
                print(e)
                run_error_reply = (f"发生异常,等待修复哦...😭\n先玩游戏其他的功能吧")
                reply = Reply(ReplyType.ERROR, run_error_reply)
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS

    def get_help_text(self, **kwargs):
        help_text = "请先配置config.json文件，删除app.py中config.json中的画图前缀，或者修改不同的画图前缀"
        return help_text
