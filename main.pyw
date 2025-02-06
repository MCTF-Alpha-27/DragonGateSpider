from libs import *

if __name__ == "__main__":
    import plugins

    dragonGateSpider.show()
    
    add_to_threads(SayEngine())

    say_in_english("welcome, president")
    say_in_english("please login")

    try:
        errorlevel = app.exec()
        words_queue.put(None)
    except Exception as e:
        dragonGateSpider.print_error(e)
        
    dragonGateSpider.log(f"程序退出，退出码为{str(errorlevel)}", dragonGateSpider.INFO)
    if logfile:
        dragonGateSpider.logfile.close()
    sys.exit(errorlevel)
