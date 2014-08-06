import landerdb
import os
import time
import shutil

class LocalBackup:
    def __init__(self):
        self.db = landerdb.Connect("localbackup.db")
        self.start_dir = str(self.db.find("startdirectory", "all")[0]['startdirectory'])
        self.hardDiskDirectory = str(self.db.find("harddisk", "all")[0]["harddisk"])
        self.lastBackup = self.db.find("lastbackup", "all")[0]['lastbackup']

    def main(self):
        while True:
            if time.time() - self.lastBackup >= 60 * 60 * 24:
                self.createDirs()
                self.writeFiles()
                self.db.update("lastbackup", {"lastbackup":self.lastBackup}, {"lastbackup":time.time()})
                self.db.save()
                print "Backed up"
            time.sleep(60*60)

    def createDirs(self):
        
        for dirs, _, _ in os.walk(self.start_dir):
            dirs = dirs.replace(self.start_dir, '/')
            if not os.path.exists(self.hardDiskDirectory+dirs):
                print self.hardDiskDirectory+dirs
                try:
                    os.mkdir(self.hardDiskDirectory+dirs)
                except OSError:
                    pass

    def writeFiles(self):
        for dirs, _, files in os.walk(self.start_dir):
            new_dirs = dirs.replace(self.start_dir, "/")
            for files in files: 
                try:
                    check = open(dirs+"/"+files, 'rb').read()
                    if os.path.exists(self.hardDiskDirectory+new_dirs+files):
                
                        if hash(check) != hash(open(self.hardDiskDirectory+new_dirs+files, 'rb').read()): # If the file has changed
                            print self.hardDiskDirectory+new_dirs+files
                            shutil.copy(dirs+"/"+files, self.hardDiskDirectory+new_dirs+files)

                    else:
                        print self.hardDiskDirectory+new_dirs+files
                        shutil.copy(dirs+"/"+files, self.hardDiskDirectory+new_dirs+files)

                except Exception, e:
                    print e



if __name__ == "__main__":
    if not os.path.exists("localbackup.db"):
        db = landerdb.Connect("localbackup.db")
        start_directory = raw_input("Enter your home directory: ")
        hardDiskDirectory = raw_input("Enter hardisk directory: ")
        db.insert("harddisk", {"harddisk":hardDiskDirectory})
        db.save()
        db.insert("startdirectory", {"startdirectory":start_directory})
        db.save()
        db.insert("lastbackup", {"lastbackup":0})
        db.save()

    LocalBackup().main()
