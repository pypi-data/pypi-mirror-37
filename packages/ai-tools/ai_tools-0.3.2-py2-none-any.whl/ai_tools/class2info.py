# -*- coding: utf-8 -*-
import os
import os.path
import xml.dom.minidom
import sys
import MySQLdb
from PIL import Image
import time
from zprint import *

reload(sys) 
sys.setdefaultencoding('utf-8')

def con_db1():
    hostName = "172.23.250.51"
    userName = "root"
    passWord = "20180712"
    #dataBase = "ground_truth"
    #dataBase = project_name
    charset = "utf8"
    db = MySQLdb.connect("%s"%(hostName), "%s"%(userName), "%s"%(passWord), charset='utf8' )

    return db

def insert_project2db(projectName,localpath):
    
    db = con_db1()
    cursor = db.cursor()

    cursor.execute("CREATE DATABASE if not exists %s DEFAULT CHARACTER SET utf8" % projectName)
    cursor.execute("USE %s" % projectName)
    #create xml table
    xmlTbName = projectName+'xml'
    sql = "Create table if not exists %s (id int(10) unsigned primary key auto_increment, image_name varchar(200), xml_content varchar(2000), marker_id char(20)) default character set utf8"%  xmlTbName
    cursor.execute(sql)
    db.commit()
    #create imagetable
    imgTbName = projectName+'img'
    sql = "Create table if not exists %s (id int(10) unsigned primary key auto_increment, image_name varchar(200), raw_data longblob, is_marking char(20) default 'no', if_verify char(20) default 'no') default character set utf8"% imgTbName
    cursor.execute(sql)

    cc=0
    for imagefile in os.listdir(localpath):
        cc+=1
        print "[%d,%s]"%(cc,os.path.join(localpath,imagefile))
        Image.open(os.path.join(localpath,imagefile)).save("tmp.png")
        #with open(os.path.join(localpath, imagefile), "rb") as f:
        with open("tmp.png", "rb") as f:
            img_data = f.read()
            f.close()
        image_name = str(imagefile)[:-4]
        sql = "INSERT INTO %s (image_name, raw_data) VALUES ('%s', '%s')" % (imgTbName, image_name, MySQLdb.escape_string(img_data))
        cursor.execute(sql)
        db.commit()

    cursor.close()
    db.close()

def con_db2():
    hostName = "172.23.250.28"
    userName = "root"
    passWord = "MyNewPass4!"
    dataBase = "labelImg_monitor_task"
    charset = "utf8"
    db = MySQLdb.connect("%s"%(hostName), "%s"%(userName), "%s"%(passWord), "%s"%(dataBase), charset='utf8' )

    return db

def get_class_info(class_id_str):
    info_list_l=[]
    db = con_db2()
    cursor = db.cursor()
    tbName = "labelImg_monitor_task"
    insert_status = 'insert'
    can_status = 'can_download'
    done_status = 'download_done'
    cannot_status = 'cannot_download'
    class_ids=class_id_str.split(',')
    for class_id in class_ids:
        sql = "INSERT INTO %s (online_class_id, status) VALUES (%d, '%s')" % (tbName, int(class_id), insert_status)
        cursor.execute(sql)
    print "%s is ok!"% sql
    db.commit()
    for class_id in class_ids:
        sql = "SELECT status FROM %s WHERE online_class_id = %d LIMIT 1"%(tbName, int(class_id))
        #the longgest query time is 20s
        for i in range(0,80):
            zprintr(sql)
            db.commit()
            cursor.execute(sql)
            curr_status = cursor.fetchone()[0]
            zprintr( "%d s: Query again.curr_status: %s"%((i*5), curr_status))
            if curr_status == can_status:
                zprint("%d s passed."%(i*5))
                zprint("Now the status of %s is %s."%(class_id, curr_status))
                break
            elif curr_status == cannot_status:
                zprint("Now the status of %s is %s."%(class_id, curr_status))
                return [False, curr_status]
            time.sleep(5)
            if i == 99 and curr_status != can_status:
                zprint("Now the status of %s is %s."%(class_id, curr_status))
                return [False, curr_status]
        #info: online_class_id,supplier_code,student_id, teacher_id,classroom, scheduled_date_time
        sql = "SELECT online_class_id, supplier_code, student_id,teacher_id, class_room, scheduled_date_time FROM %s WHERE online_class_id = %d LIMIT 1"%(tbName, int(class_id))
        cursor.execute(sql)
        info_tuple = cursor.fetchone()
        print info_tuple
        info_list = list(tuple(info_tuple))
        info_list[-1]=info_list[-1].strftime("%Y-%m-%d %H:%M:%S")
        print "info_list: ", info_list
        info_list_l.append(info_list)
    db.commit()
    db.close()
    return info_list_l
 
def updateDb(class_id, status):

    db = con_db2()
    cursor = db.cursor()
    tbName = "labelImg_monitor_task"

    sql = "UPDATE %s SET status = '%s' WHERE online_class_id  = %d" % (tbName, status, int(class_id))
    cursor.execute(sql)
    print "%s is ok."%sql
    db.commit()
    db.close()
#insert_project2db("download_try_123732774", "D:/file/try/try")
#insert_project2db("test0802wu","D:/file/try/try")
if __name__=="__main__":
    class_id=137946928
    class_id=137825379
    class_id=137243710
    class_id="137434266,137483549"
    class_id="136087333,135838281"
    class_id="136819472,137829699"
    class_id="136812550,136736262,135863774,137921226,137868755,137226610,135883148,137379131,136212977,137950702,137462084,135823448,137731053,135901211,137306710,135758923,137807125,136841142,135008263,136522226,136819218,136170925,137750547,137228421,135896205,135932609,137865776,123300682,137201733,136475716,136736570,137868931,135793858,135983779,137930552,137881030,137072776,135898487"
    info_list=get_class_info(class_id)
    print(info_list)
    
