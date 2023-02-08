"""
主窗口文件，负责创建主窗口
"""
import logging
import time
import os
import pyautogui
import pyttsx3
import configparser

from PyQt6.QtWidgets import *
from libs.gui.ui_DragonGateSpider import Ui_DragonGateSpider

from pywinauto.application import Application
from psutil import process_iter

engine = pyttsx3.init()

if not os.path.exists("config.ini"):
    cfg = configparser.ConfigParser()
    cfg_file = open("config.ini", "w")
    cfg.add_section("logger")
    cfg.set("logger", "logfile", "1")
    cfg.set("logger", "voicelog", "1")
    cfg.write(cfg_file)
    cfg_file.flush()
    cfg_file.close()

cfg = configparser.ConfigParser()
cfg.read("config.ini")
logfile_ = bool(int(cfg.get("logger", "logfile")))
voicelog_ = bool(int(cfg.get("logger", "voicelog")))

def say_in_english(words):
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 150)
    engine.say(words)
    engine.runAndWait()

if not voicelog_:
    def disable(words):
        pass
    say_in_english = disable

class DragonGateSpider(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DragonGateSpider()
        self.ui.setupUi(self)
        self.setWindowTitle("龙门爬虫")

        self.NORMAL = "NORMAL"
        self.INFO = "INFO"
        self.WARNING = "WARNING"
        self.ERROR = "ERROR"

        if not os.path.exists("logs"):
            os.mkdir("logs")

        if logfile_:
            self.logfile = open("logs/%s.log"%time.strftime(r"%Y-%m-%d-%H.%M.%S"), "a")
            self.logfile.write(time.strftime(r"%Y-%m-%d") + "的运行日志\n\n")
            self.logfile.flush()

            logging.basicConfig(filename="logs/%s.log"%time.strftime(r"%Y-%m-%d-%H.%M.%S"), level=logging.INFO, format="[%(asctime)s] [%(levelname)s]: %(message)s")

        self.log("欢迎，龙门主席，请登录您的账号", self.INFO)

        self.ui.login_button.disconnect()
        self.ui.login_button.clicked.connect(self.on_login_button_clicked)
        self.isrun = False

    def log(self, text, level="NORMAL"):
        """日志器，负责写入日志"""
        if level == self.NORMAL:
            self.ui.logger.append("<font color='white'>%s</font>"%text)
            if logfile_:
                self.logfile.write(text)
                self.logfile.flush()
                self.logfile.write("\n")
                self.logfile.flush()
        elif level == self.INFO:
            self.ui.logger.append("<font color='white'>[%s] [%s]: %s</font>"%(time.strftime(r"%Y-%m-%d %H:%M:%S"), level, text))
            if logfile_:
                logging.info(text)
        elif level == self.WARNING:
            self.ui.logger.append("<font color='yellow'>[%s] [%s]: %s</font>"%(time.strftime(r"%Y-%m-%d %H:%M:%S"), level, text))
            if logfile_:
                logging.warning(text)
        elif level == self.ERROR:
            self.ui.logger.append("<font color='red'>[%s] [%s]: %s</font>"%(time.strftime(r"%Y-%m-%d %H:%M:%S"), level, text))
            if logfile_:
                logging.error(text)
        else:
            self.ui.logger.append("<font color='white'>[%s] [%s]: %s</font>"%(time.strftime(r"%Y-%m-%d %H:%M:%S"), level, text))
            if logfile_:
                logging.info(text)

    def on_login_button_clicked(self):
        self.isrun = True
        pid = self.get_wechat_pid()
        if not pid:
            self.log("未检测到微信运行，请先登录微信", self.ERROR)
            self.isrun = False
            say_in_english("please login")
        else:
            self.app = Application(backend="uia").connect(process=pid)
            self.wechat_window = self.app.window(class_name="WeChatMainWndForPC")
            pyautogui.hotkey("ctrl", "alt", "w")
            self.wechat_window.minimize()
            self.log("已尝试打开微信窗口并最小化，如果没有成功，请手动打开", self.INFO)
            self.log("注意：程序运行时请不要关闭微信窗口", self.INFO)
            self.ui.login_button.setText("登出")
            self.ui.login_button.setStyleSheet("background-color: red")
            self.ui.login_button.disconnect()
            self.ui.login_button.clicked.connect(self.on_logout_button_clicked)
            say_in_english("login succeeded")
            say_in_english("please stand by")

    def on_logout_button_clicked(self):
        self.log("收到停止请求", self.INFO)
        say_in_english("stop request received")
        self.isrun = False
        self.ui.login_button.setText("登录")
        self.ui.login_button.setStyleSheet("background-color: rgb(0, 255, 0)")
        self.ui.login_button.disconnect()
        self.ui.login_button.clicked.connect(self.on_login_button_clicked)
        self.log("成功停止", self.INFO)
        self.log("终端监听任务终止", self.INFO)
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
            self.log("获取好友列表失败！我们获取了以下错误信息", self.ERROR)
            self.log(str(e), self.ERROR)
            say_in_english(str(e))
            return
        return user_list

app = QApplication([])
dragonGateSpider = DragonGateSpider()
