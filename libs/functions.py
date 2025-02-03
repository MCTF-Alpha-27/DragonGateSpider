"""
功能文件，爬虫的主要功能在此处实现
"""
from libs.windows.DragonGateSpider import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import pywinauto

# 监听聊天记录
listen_chat_action = QAction("监听聊天记录", dragonGateSpider.ui.functions_menu)

def _listen_chat_action():
    if dragonGateSpider.isrun:
        dragonGateSpider.log("收到监听请求，开始监听聊天记录", dragonGateSpider.INFO)
        dragonGateSpider.log(f"获取到以下关键词: {str(reply)}", dragonGateSpider.INFO)
        say_in_english("listening request received")
        executant_wrapper_object = dragonGateSpider.main_window.wrapper_object()
        early_text = []
        try:
            while True:
                if not dragonGateSpider.isrun:
                    dragonGateSpider.log("收到停止监听请求，停止监听", dragonGateSpider.INFO)
                    say_in_english("stop listening")
                    break
                for i in executant_wrapper_object.descendants():
                    if type(i) != pywinauto.controls.uia_controls.StaticWrapper:
                        continue
                    if i.window_text() not in early_text:
                        dragonGateSpider.log(i.window_text())
                        early_text.append(i.window_text())
                    for j in reply:
                        if j in i.window_text():
                            dragonGateSpider.log(f"检测到关键词: {j}，正在回复", dragonGateSpider.INFO)
                            pyautogui.hotkey("ctrl", "alt", "w")
                            dragonGateSpider.main_window.child_window(title=controller, control_type="Button").click_input()
                            executant_wrapper_object.type_keys(reply[j], with_spaces=True)
                            pyautogui.press("enter")
                            executant_wrapper_object.type_keys("回复完成", with_spaces=True)
                            pyautogui.press("enter")
                            dragonGateSpider.wechat_window.minimize()
                            dragonGateSpider.log(f"已回复", dragonGateSpider.INFO)
                            say_in_english("replied")
                time.sleep(0.1)
        except Exception as e:
            dragonGateSpider.print_error(e)
    else:
        dragonGateSpider.log("请先登录", dragonGateSpider.WARNING)
        say_in_english("please login")

class ListenChatThread(QThread):
    def run(self):
        _listen_chat_action()

listen_chat_action.triggered.connect(lambda: add_to_threads(ListenChatThread()))
dragonGateSpider.ui.functions_menu.addAction(listen_chat_action)
