
class Scheduler():
    def __init__(self,mySC):
        self.mySC = mySC
        self.loadSchedule()
        # schedule.every(10).seconds.do(self.schedule_message,msg="hola").tag("title")
        # schedule.clear('title')
        #exec("schedule.every(10).seconds.do(self.reminder1)")
        pass

    def launchSchedule(self,data):

        task= "schedule.every(" + data['time'] + ").seconds.do(self.schedule_task)"
        exec(task)

    def loadSchedule(self):
        task={'time':str(self.mySC.TIME_LAPSE) }
        self.launchSchedule(task)

    def schedule_task(self):
        self.mySC.take_picture()

"""
# After every 10mins geeks() is called. 
schedule.every(10).minutes.do(geeks)

# After every hour geeks() is called.
schedule.every().hour.do(geeks)

# Every day at 12am or 00:00 time bedtime() is called.
schedule.every().day.at("00:00").do(bedtime)

# After every 5 to 10mins in between run work()
schedule.every(5).to(10).minutes.do(work)

# Every monday good_luck() is called
schedule.every().monday.do(good_luck)

# Every tuesday at 18:00 sudo_placement() is called
schedule.every().tuesday.at("18:00").do(sudo_placement)

"""