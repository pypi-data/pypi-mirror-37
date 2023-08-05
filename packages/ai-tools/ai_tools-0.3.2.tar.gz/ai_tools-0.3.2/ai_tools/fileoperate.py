import os
import shutil
    


def rmdirfile(dirname):
    files = os.listdir(dirname)
    for file in files:
        if os.path.getsize(file) < minSize * 1000:
            os.remove(file)    #删除文件
            print(file + " deleted")
def rmdir(dirname):
    if os.path.isdir(dirname):
        shutil.rmtree(dirname)

