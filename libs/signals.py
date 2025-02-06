"""
信号文件，负责定义信号类
"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class LogSignals(QObject):
    """日志器信号"""
    log_message = pyqtSignal(str, str) # 日志信息，日志级别
