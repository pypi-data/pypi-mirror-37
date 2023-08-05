import datetime
def print_time(message):
    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("%s:%s"%(nowTime,message))

