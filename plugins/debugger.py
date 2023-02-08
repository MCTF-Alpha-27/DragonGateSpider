"""
一个用于开发者调试的插件
"""
from libs import *

__name__ = "调试器"
__author__ = "龙门主席"
__version__ = "1.0.0"

debug_menu = QMenu("调试选项", dragonGateSpider.ui.functions_menu)
dragonGateSpider.ui.functions_menu.addMenu(debug_menu)

# 调试群聊窗口句柄
def _debug_chat_window_action():
    if dragonGateSpider.isrun:
        dragonGateSpider.log(dragonGateSpider.wechat_window["龙门☭九常"].window_text(), dragonGateSpider.INFO)
    else:
        dragonGateSpider.log("请先登录", dragonGateSpider.WARNING)
        say_in_english("please login")

debug_chat_window_action = QAction("调试群聊窗口句柄", debug_menu)
debug_chat_window_action.triggered.connect(_debug_chat_window_action)
debug_menu.addAction(debug_chat_window_action)

# 调试好友获取功能
def _debug_get_users_action():
    if dragonGateSpider.isrun:
        for i in dragonGateSpider.get_users():
            dragonGateSpider.log(i)
    else:
        dragonGateSpider.log("请先登录", dragonGateSpider.WARNING)
        say_in_english("please login")

debug_get_users_action = QAction("调试好友获取功能", debug_menu)
debug_get_users_action.triggered.connect(_debug_get_users_action)
debug_menu.addAction(debug_get_users_action)
