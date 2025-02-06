"""
主窗口文件，负责创建主窗口
"""
import logging
import time
import os
import sys
import pyautogui
import configparser
import json
import traceback

from libs.signals import *
from libs.gui.ui_DragonGateSpider import Ui_DragonGateSpider
from libs.engines import *

from pywinauto.application import Application
from psutil import process_iter

cfg = configparser.ConfigParser()

if not os.path.exists("config.ini"):
    cfg_file = open("config.ini", "w", encoding="utf-8")
    cfg.add_section("logger")
    cfg.set("logger", "logfile", "1")
    cfg.set("logger", "voicelog", "1")
    cfg.add_section("spider")
    cfg.set("spider", "controller", "龙门☭九常")
    cfg.set("spider", "reply", "{}")
    cfg.write(cfg_file)
    cfg_file.flush()
    cfg_file.close()

cfg.read("config.ini", encoding="utf-8")
logfile = bool(int(cfg.get("logger", "logfile")))
voicelog = bool(int(cfg.get("logger", "voicelog")))
controller = cfg.get("spider", "controller")
reply = json.loads(cfg.get("spider", "reply"))

threads = []

def add_to_threads(thread: QThread):
    if thread.isRunning():
        dragonGateSpider.log(f"尝试添加已运行线程: {str(thread)}", dragonGateSpider.WARNING)
        return
    thread.finished.connect(lambda: threads.remove(thread))
    thread.finished.connect(thread.deleteLater)
    thread.finished.connect(lambda: dragonGateSpider.log(f"Thread end: {str(thread)}", dragonGateSpider.DEBUG))
    threads.append(thread)
    thread.start()

def say_in_english(word):
    if not voicelog:
        return
    try:
        words_queue.put(word)
    except Exception as e:
        dragonGateSpider.print_error(e)

class DragonGateSpider(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DragonGateSpider()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)
        self.setFixedSize(self.size())
        self.setWindowTitle("龙门爬虫 v1.1.0")

        self.NORMAL = "NORMAL"
        self.INFO = "INFO"
        self.WARNING = "WARNING"
        self.ERROR = "ERROR"
        self.DEBUG = "DEBUG"

        self.log_signals = LogSignals() # 该死的多线程，我现在用信号总行了吧
        self.log_signals.log_message.connect(self._log)

        if not os.path.exists("logs"):
            os.mkdir("logs")

        if logfile:
            self.logfile = open("logs/%s.log"%time.strftime(r"%Y-%m-%d-%H.%M.%S"), "a", encoding="utf-8")
            self.logfile.write(time.strftime(r"%Y-%m-%d") + "的运行日志\n\n")
            self.logfile.flush()

            logging.basicConfig(filename="logs/%s.log"%time.strftime(r"%Y-%m-%d-%H.%M.%S"), level=logging.DEBUG, format="[%(asctime)s] [%(levelname)s]: %(message)s", encoding="utf-8")

        self.log("欢迎，龙门主席，请登录您的账号", self.INFO)

        self.ui.login_button.disconnect()
        self.ui.login_button.clicked.connect(self.on_login_button_clicked)
        self.isrun = False

    def _log(self, text, level):
        """日志器"""
        if level == self.NORMAL:
            self.ui.logger.append("<font color='white'>%s</font>"%text)
            if logfile:
                self.logfile.write(text)
                self.logfile.flush()
                self.logfile.write("\n")
                self.logfile.flush()
        elif level == self.INFO:
            self.ui.logger.append("<font color='white'>[%s] [%s]: %s</font>"%(time.strftime(r"%Y-%m-%d %H:%M:%S"), level, text))
            if logfile:
                logging.info(text)
        elif level == self.WARNING:
            self.ui.logger.append("<font color='yellow'>[%s] [%s]: %s</font>"%(time.strftime(r"%Y-%m-%d %H:%M:%S"), level, text))
            if logfile:
                logging.warning(text)
        elif level == self.ERROR:
            self.ui.logger.append("<font color='red'>[%s] [%s]: %s</font>"%(time.strftime(r"%Y-%m-%d %H:%M:%S"), level, text))
            if logfile:
                logging.error(text)
        elif level == self.DEBUG:
            if logfile:
                logging.debug(text)
        else:
            self.ui.logger.append("<font color='white'>[%s] [%s]: %s</font>"%(time.strftime(r"%Y-%m-%d %H:%M:%S"), level, text))
            if logfile:
                logging.info(text)

    def log(self, text, level="NORMAL"):
        """写入日志"""
        self.log_signals.log_message.emit(text, level)

    def print_error(self, e: Exception):
        """错误处理器，负责打印错误"""
        self.log(f"运行时发生错误\n{"".join(traceback.format_tb(e.__traceback__))}\n{e.__class__.__name__}: {str(e)}", self.ERROR)

    def on_login_button_clicked(self):
        self.isrun = True
        pid = self.get_wechat_pid()
        if not pid:
            self.log("未检测到微信运行，请先登录微信", self.ERROR)
            self.isrun = False
            say_in_english("please login")
        else:
            try:
                self.log(f"连接到主窗口: {controller}", self.INFO)
                self.app = Application(backend="uia").connect(process=pid)
                self.wechat_window = self.app.window(class_name="WeChatMainWndForPC")
                pyautogui.hotkey("ctrl", "alt", "w")
                self.main_window = self.wechat_window.child_window(title=controller, control_type="ListItem")
                self.wechat_window.minimize()
            except Exception as e:
                self.print_error(e)
                return
            self.log("已尝试打开微信窗口并最小化，如果没有成功，请手动打开", self.INFO)
            self.log("注意: 程序运行时请不要关闭微信窗口", self.INFO)
            self.ui.login_button.setText("登出")
            self.ui.login_button.setStyleSheet("background-color: red")
            self.ui.login_button.disconnect()
            self.ui.login_button.clicked.connect(self.on_logout_button_clicked)
            say_in_english("login succeeded")

    def on_logout_button_clicked(self):
        self.log("收到登出请求", self.INFO)
        say_in_english("stop request received")
        self.isrun = False
        self.ui.login_button.setText("登录")
        self.ui.login_button.setStyleSheet("background-color: rgb(0, 255, 0)")
        self.ui.login_button.disconnect()
        self.ui.login_button.clicked.connect(self.on_login_button_clicked)
        self.log("已登出", self.INFO)
        self.log("爬虫所有任务已终止", self.INFO)
        say_in_english("successfully stopped")
        say_in_english("terminal monitoring task terminated")

    def get_wechat_pid(self):
        """获取微信的pid"""
        if not self.isrun:
            self.log("请先登录", self.INFO)
            say_in_english("please login")
            return
        for i in process_iter():
            pid_dic = i.as_dict(attrs=["pid", "name"])
            if pid_dic["name"] == "WeChat.exe":
                return pid_dic["pid"]

    def get_users(self):
        """获取微信好友"""
        if not self.isrun:
            self.log("请先登录", self.INFO)
            say_in_english("please login")
            return
        user_list = []
        try:
            self.log("正在获取好友列表", self.INFO)
            say_in_english("getting users list")
            users = self.wechat_window.child_window(title="会话", control_type="List").children()
            for i in users:
                user_list.append(i.window_text())
        except Exception as e:
            self.print_error(e)
            return
        return user_list

app = QApplication(sys.argv)
dragonGateSpider = DragonGateSpider()
