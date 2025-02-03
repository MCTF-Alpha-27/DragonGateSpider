"""
引擎文件，负责创建引擎
一般来说，此文件中的引擎应当在main.pyw中实例化并加入到线程队列中
"""
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from queue import Queue
import pyttsx3

words_queue = Queue()

class SayEngine(QThread):
    """语音引擎"""
    def __init__(self):
        super().__init__()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", self.voices[1].id)
        self.engine.setProperty("rate", 150)

    def say(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()

    def run(self):
        while True:
            task = words_queue.get()
            if task is None:
                break
            self.say(task)
            words_queue.task_done()
