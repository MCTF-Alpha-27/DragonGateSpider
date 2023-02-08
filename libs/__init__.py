import pywinauto
import time
from libs.windows.DragonGateSpider import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

def exit_app(title, text):
   QMessageBox.information(dragonGateSpider, title, text)
   dragonGateSpider.setVisible(False)
   app.quit()
