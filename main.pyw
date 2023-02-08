import sys
from libs import *

if __name__ == "__main__":
    import libs.functions
    import plugins
    dragonGateSpider.show()
    say_in_english("welcome, chairman")
    say_in_english("please login")
    errorlevel = app.exec()
    if logfile_:
        dragonGateSpider.logfile.close()
    sys.exit(errorlevel)
