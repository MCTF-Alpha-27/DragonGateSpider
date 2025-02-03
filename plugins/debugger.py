"""
一个用于开发者调试的插件
"""
from libs import *
from io import StringIO
import sys

__name__ = "调试器"
__author__ = "龙门主席"
__version__ = "1.1.0"

debug_menu = QMenu("调试选项", dragonGateSpider.ui.functions_menu)
dragonGateSpider.ui.functions_menu.addMenu(debug_menu)

# 调试群聊窗口标题
def _debug_chat_window_action():
    if dragonGateSpider.isrun:
        try:
            dragonGateSpider.log(f"输出群聊窗口标题\n{dragonGateSpider.wechat_window[controller].window_text()}", dragonGateSpider.DEBUG)
        except Exception as e:
            dragonGateSpider.print_error(e)
    else:
        dragonGateSpider.log("请先登录", dragonGateSpider.WARNING)
        say_in_english("please login")

debug_chat_window_action = QAction("调试群聊窗口句柄", debug_menu)
debug_chat_window_action.triggered.connect(_debug_chat_window_action)
debug_menu.addAction(debug_chat_window_action)

# 调试好友获取功能
def _debug_get_users_action():
    if dragonGateSpider.isrun:
        dragonGateSpider.log("获取好友列表", dragonGateSpider.DEBUG)
        try:
            for i in dragonGateSpider.get_users():
                dragonGateSpider.log(i)
        except Exception as e:
            dragonGateSpider.print_error(e)
    else:
        dragonGateSpider.log("请先登录", dragonGateSpider.WARNING)
        say_in_english("please login")

debug_get_users_action = QAction("调试好友获取功能", debug_menu)
debug_get_users_action.triggered.connect(_debug_get_users_action)
debug_menu.addAction(debug_get_users_action)

def print_control_identifiers(window):
    captured_output = StringIO()
    original_stdout = sys.stdout
    sys.stdout = captured_output
    window.print_control_identifiers()
    dragonGateSpider.log(f"输出窗口句柄{str(window)}\n{captured_output.getvalue()}", dragonGateSpider.DEBUG)
    sys.stdout = original_stdout

# 调试窗口句柄
def _debug_get_hwnd_action():
    if dragonGateSpider.isrun:
        try:
            print_control_identifiers(dragonGateSpider.wechat_window.child_window(title=controller, control_type="ListItem"))
            exec_wrapper = dragonGateSpider.wechat_window.child_window(title=controller, control_type="ListItem").wrapper_object()
            for i in exec_wrapper.descendants():
                dragonGateSpider.log(i.window_text(), dragonGateSpider.DEBUG)
        except Exception as e:
            dragonGateSpider.print_error(e)
    else:
        dragonGateSpider.log("请先登录", dragonGateSpider.WARNING)
        say_in_english("please login")

debug_get_hwnd_action = QAction("调试窗口句柄", debug_menu)
debug_get_hwnd_action.triggered.connect(_debug_get_hwnd_action)
debug_menu.addAction(debug_get_hwnd_action)

# 调试选择窗口
def _debug_select_window_action():
    if dragonGateSpider.isrun:
        try:
            dragonGateSpider.log(f"选择窗口: {controller}", dragonGateSpider.DEBUG)
            pyautogui.hotkey("ctrl", "alt", "w")
            dragonGateSpider.wechat_window.child_window(title=controller, control_type="ListItem").child_window(title=controller, control_type="Button").click_input()
            dragonGateSpider.wechat_window.minimize()
        except Exception as e:
            dragonGateSpider.print_error(e)
    else:
        dragonGateSpider.log("请先登录", dragonGateSpider.WARNING)
        say_in_english("please login")

debug_select_window_action = QAction("调试选择窗口", debug_menu)
debug_select_window_action.triggered.connect(_debug_select_window_action)
debug_menu.addAction(debug_select_window_action)
