import sys
from libs import *

if __name__ == "__main__":
    import plugins
    add_to_threads(SayEngine())
    dragonGateSpider.show()
    say_in_english("welcome, president")
    say_in_english("please login")
    try:
        errorlevel = app.exec()
        words_queue.put(None)
    except Exception as e:
        dragonGateSpider.print_error(e)
    if logfile:
        dragonGateSpider.logfile.close()
    sys.exit(errorlevel)
