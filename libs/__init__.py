from libs.windows.DragonGateSpider import *
from libs.functions import *

def exit_app(title, text):
   QMessageBox.information(dragonGateSpider, title, text)
   dragonGateSpider.setVisible(False)
   app.quit()
