import landerdb
import os
import time
import shutil
import thread

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
                old = os.path.join(dirs, files)
                new = os.path.join(self.hardDiskDirectory+new_dirs, files)
                self.new = new
                try:
                    size = os.path.getsize(old)
                    if size == 0: # Occationally it would get stuck
                        continue
                    check = os.stat(old).st_size
                
                    if os.path.exists(new):
                        c2 = os.stat(new).st_size
                        if check != c2: # If the file has changed
                            print new, "Changed"
                            
                            if size > 0  and size < 1024 * 1024 * 500: # 500mb
                                shutil.copy(old, new)
                            elif size > 0:
                                thread.start_new_thread(self.longCopy, (old,))
                    else:
                        print new
                
                        if size > 0  and size < 1024 * 1024 * 500: # 500mb 
                            shutil.copy(old, new)
                        elif size > 0:
                            thread.start_new_thread(self.longCopy, (old,))

                except Exception, e:
                    print e
                    break # Just skip the directory


    def longCopy(self, files):
        with open(self.new, 'wb') as file:
            with open(files, 'rb') as old:
                while True:
                    data = old.read(1024)
                    if not data:
                        break
                    else:
                        file.write(data)


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
