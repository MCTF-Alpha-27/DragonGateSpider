"""
功能文件，爬虫的主要功能在此处实现
"""
from threading import Thread
from libs import *

# 监听聊天记录
listen_chat_action = QAction("监听聊天记录", dragonGateSpider.ui.functions_menu)

def _listen_chat_action():
    if dragonGateSpider.isrun:
        dragonGateSpider.log("收到监听请求，开始监听聊天记录", dragonGateSpider.INFO)
        say_in_english("listening request received")
        dragonGate_window = dragonGateSpider.wechat_window.child_window(title="拉比林斯迷宫", control_type="ListItem")
        early_text = []
        while True:
            try:
                for i in dragonGate_window.wrapper_object().descendants():
                    if i.window_text() not in early_text:
                        dragonGateSpider.log(i.window_text())
                        early_text.append(i.window_text())
                time.sleep(0.5)
            except Exception as e:
                dragonGateSpider.log(f"{e.__class__.__name__}: {str(e)}", dragonGateSpider.ERROR)
    else:
        dragonGateSpider.log("请先登录", dragonGateSpider.WARNING)
        say_in_english("please login")

listen_chat_action.triggered.connect(lambda: Thread(target=_listen_chat_action).start())
dragonGateSpider.ui.functions_menu.addAction(listen_chat_action)
