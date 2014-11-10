import os
import shutil
import datetime
import time
import thread

class LocalBackup:
    def __init__(self):
        self.prevDate = None
        self.nowDate  = "{0}-{1}-{2}"
        self.backupDir = raw_input("Backup Directory: ")
        self.startDir = raw_input("Start Directory: ")
        self.on = False
        self.threads = 0
        self.maxThreads = 25

    def main(self):
        thread.start_new_thread(self.interaction, ())
        while True:
            now = datetime.datetime.now()
            self.nowDate = self.nowDate.format(now.year, now.month, now.day)
            if self.nowDate != self.prevDate:
                self.prevDate = self.nowDate
                if not os.path.exists(self.backupDir + "/" + self.nowDate):
                    os.mkdir(self.backupDir + "/" + self.nowDate)
                self.backup()
                print "Done" 

            time.sleep(60 * 60)



    def backup(self):
        for dire, _, files in os.walk(self.startDir):
            dire = dire.replace(self.startDir, '')
            self.on = self.backupDir + "/" + self.nowDate + "/" + dire
            if not os.path.exists(self.backupDir + "/" + self.nowDate + "/" + dire):
                try:
                    os.mkdir(self.backupDir + "/" + self.nowDate + "/" + dire)
                    print self.backupDir + "/" + self.nowDate + "/" + dire
                except Exception, e:
                    print dire + " Can't be made"
                    print e
            
            for files in files:
                while self.threads == self.maxThreads:
                    pass
                self.threads += 1
                thread.start_new_thread(self.copy, (dire, files))

         
    
    def copy(self, directory, file):
        origin = "/home/frankie/{0}/{1}".format(directory, file)
        destination = "{0}/{1}/{2}/{3}".format(self.backupDir, self.nowDate, directory, file)
        if os.path.exists(destination):
            obj1 = open(origin)
            c1 = obj1.read()
            obj1.close()
            obj2 = open(destination)
            c2 = obj2.read()
            obj2.close()

            if hash(c1) == hash(c2):
                print "{0} Hasn't changed".format(destination)
                self.threads -= 1
                return
        self.on = destination
        try:
            shutil.copy2(origin, destination)
            print destination

        except Exception, e:
            print "Can't Copy {0}".format(origin)
            print e

        self.threads -= 1

    def interaction(self):
        while True:
            raw_input()
            print self.on

if __name__ == "__main__":
    LocalBackup().main()
