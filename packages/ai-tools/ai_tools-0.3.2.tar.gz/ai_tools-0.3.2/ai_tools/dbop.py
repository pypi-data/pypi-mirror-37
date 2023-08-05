# -*- coding: UTF-8 -*-
import fileinput
from scipy import misc
import sys
import os
import argparse
import numpy as np
import random
from time import sleep
import time
import datetime
import scipy.misc
import hashlib
import urllib2
import json
from DBUtils.PooledDB import PooledDB
import traceback
import cv2
from PIL import Image
import imageio
import shutil
from skimage import io
import os.path
import MySQLdb
import sys

class dbop:
    def __init__(self,hostName="127.0.0.1",usrName="root",passWord="123456",charset="utf8"):
        #pool = PooledDB(MySQLdb,1,host='10.106.5.9',user='oco',passwd='MyNewPass4!',db='task_zmm',port=3306,charset='utf8')
        #self.db = MySQLdb.connect("%s"%(hostName), "%s"%(userName), "%s"%(passWord), "%s"%(dataBase), charset='utf8' )
        #self.db = MySQLdb.connect("%s"%(hostName), "%s"%(usrName), "%s"%(passWord), "%s"%(dataBase), charset='utf8' )
        self.db = MySQLdb.connect("%s"%(hostName), "%s"%(usrName), "%s"%(passWord), charset='utf8' )
    def po(self,message):
        print(message)

    def turple2list(self,turple_val):
        rlist = lambda t, self=lambda t, self: [self (tt, self ) for tt in t] if isinstance (t, tuple ) else t: self (t, self )
        #rlist (((1,),(1,(1,2,3,(4,5 )))))
        rl=rlist (turple_val)
        return rl

    def run(self,sqlstr):
       
        cursor = self.db.cursor()
        content=None
        try:
            #sql = "SELECT xml_content FROM %sxml WHERE image_name = '%s'"%(project_name,image_name)
            #sql = "SELECT xml_content FROM %sxml WHERE image_name = '%s'"%(project_name,image_name)
            cursor.execute(sqlstr)
            content = cursor.fetchall()
        except Exception as e:
            self.po(sqlstr)
            self.po(e)
        self.db.commit()
        return self.turple2list(content)
    def help(self,name='sql'):
        if name=="sql":
            self.po("SELECT ziduan FROM %sxml WHERE image_name = '%s'")
            self.po("INSERT INTO %sxml (image_name, xml_content) VALUES ('%s','%s')")
            self.po("UPDATE %sxml SET xml_content = '%s' WHERE image_name = '%s'")
            self.po("select count(*) from %s_task  where status='finished' and teacher_id=%d")
            self.po("insert into  audio_flvs(online_class_id,info,created_at,updated_at) values(%d,'%s',now(),now())")
            self.po('delete from video_flvs where online_class_id=%d')
            self.po("insert into  video_flvs(online_class_id,info,created_at,updated_at) values(%d,'%s',now(),now())")

    def getnum(self,rr):
        num=0
        if rr is None:
            num+=0
        else:
            num+=rr[0][0]
        return num

    
    def get_task_num(projectname,host_id,status):
        #sqlstr="select online_class_id,info from %s_task  where status='%s' and host_id=%d order by id limit 1"%(projectname,status,host_id)
        sqlstr="select count(*) from %s_task  where status='%s' and host_id=%d"%(project_name,status,host_id)
        rr=self.run(sqlstr)
        return self.getnum(rr) 

    def get_finished_num_by_teacher_id(self,project_name,teacher_id,host_id):
        task_sql="select count(*) from %s_task  where status='finished' and teacher_id=%d"%(project_name,teacher_id)
        rr=self.run(sqlstr)
        return self.getnum(rr) 
    def get_task_list_from_db(self,project_name,host_id,pre_log_str):
        sqlstr="select online_class_id,supplier_code,student_id,teacher_id,class_room as classroom,scheduled_date_time,course_id,student_id,birthday,english_name,teacher_1_avatar_url,teacher_2_avatar_url,teacher_3_avatar_url,teacher_4_avatar_url from %s_task  where status in ('insert') and host_id=%d  order by id limit 1"%(project_name,host_id)
        rr=self.run(sqlstr)
        tl=self.tasklist2dict(rr) 
        return tl 
    def update_finished_num(self,project_name,teacher_id,finished_num):
        sqlstr="update %_task set finished_num=%d,updated_at=now() where teacher_id=%d "%(project_name,finished_num,teacher_id)
        rr=self.run(sqlstr)
        return self.getnum(rr) 
    def update_finished_teacher_id_status_as_repeate(self,project_name,teacher_id,pre_log_str):
        sqlstr="update %s_task set status='repeate',updated_at=now() where teacher_id=%d and status='new'"%(project_name,teacher_id)
        rr=self.run(sqlstr)
        return rr
    def connect(self,project_name):
        #pool = PooledDB(MySQLdb,1,host='10.106.5.9',user='oco',passwd='MyNewPass4!',db='task_zmm',port=3306,charset='utf8')
        #pool = PooledDB(MySQLdb,1,host='122.152.206.246',user='oco',passwd='MyNewPass4!',db='task_zmm',port=3306,charset='utf8')
        pool = PooledDB(MySQLdb,1,host='127.0.0.1',user='root',passwd='MyNewPass4!',db='%s_task'%(project_name),port=3306,charset='utf8')
        return pool
    
    def get_task_list_by_hand(pre_log_str):
        pre_log_str+=sys._getframe().f_code.co_name+':'
        log2(pre_log_str+'[start]')
        '''
        #distinct teacher_id,oc.id,scheduled_date_time,course_id,class_type,supplier_code,student_id,classroom 
        #4975    10024634        2017-01-12 21:30:00.0   5102    0       2       1873263 jz0e4ce371ad9643529c07d46fa2b473f6
        #9466032 2010-05-01      cindy   88908548        597816  jz50c2c134629f454da020f0da757a3fa0      2018-03-29 19:00:00.0   2       1792256,https://teacher-media.vipkid.com.cn/teacher/avatar/1792256/avatar_large/image_20161222190339_76221a2e558849d9a88e86e5962cd9b1.png|10085815,https://teacher-media.vipkid.com.cn/teacher/avatar/10085815/avatar_large/image_20171201235242_622f7edbf62c40a28fda623e2c716e34.png|8286866,https://teacher-media.vipkid.com.cn/teacher/avatar/8286866/avatar_large/image_20171015192213_df2997251d474eb588ccbd406898cefd.png|8613024,https://teacher-media.vipkid.com.cn/teacher/avatar/8613024/avatar_large/image_20171021131609_f0a47d44232a4472ba7180abeb16c3a0.png
        #1295483 2009-05-23      Kitty   94979870        597816  jz08c045b4d10a43d79a69f7df847874dc      2018-04-24 19:00:00.0   7       1076218,https://teacher-media.vipkid.com.cn/teacher/avatar/1076218/avatar_large/image_20161222185510_87385003166546b8a1b740b395f19626.png|2312087,https://teacher-media.vipkid.com.cn/teacher/avatar/2312087/avatar_large/image_20161222191249_eb124b8f82e140aebbbb5b8dda51e614.png|5675039,https://teacher-media.vipkid.com.cn/teacher/avatar/5675039/avatar_large/image_20171231002452_f6af238df0f44821acad7c6afe593591.png|2031380,https://teacher-media.vipkid.com.cn/teacher/avatar/2031380/avatar_large/image_20161222190714_8300ec7c9d784b15943413b2cd6e07be.png
        '''
        task_list=[]
        task_dict={}
        task_dict['online_class_id']=93363743
        task_dict['supplier_code']=8
        task_dict['student_id']=1896711
        task_dict['teacher_id']=7832201
        task_dict['classroom']='jz721ee6b1cff04559a597a6572d9f00d1'
        task_dict['scheduled_date_time']='2018-04-26 18:00:00'
        task_list.append(task_dict)
        log2(pre_log_str+'[  end]')
    
        return task_list
    def tasklist2dict(self,rr): 
        task_list=[]
        for rrr in rr:
           task=rrr
           online_class_id=task[0]
           #info=task[1]
           task_dict={}
           task_dict['online_class_id']=int(task[0])
           task_dict['supplier_code']=int(task[1])
           task_dict['student_id']=int(task[2])
           task_dict['teacher_id']=int(task[3])
           task_dict['course_id']=int(task[6])
           #task_dict['class_type']=int(task[7])
           task_dict['classroom']=str(task[4])
           task_dict['scheduled_date_time']=str(task[5])
           task_dict['student_id']=int(task[7])
           task_dict['birthday']=str(task[8])
           task_dict['english_name']=str(task[9])
           task_dict['teacher_1_avatar_url']=str(task[10])
           task_dict['teacher_2_avatar_url']=str(task[11])
           task_dict['teacher_3_avatar_url']=str(task[12])
           task_dict['teacher_4_avatar_url']=str(task[13])
           #task_dict = json.loads(info)
           task_list.append(task_dict)
        return task_list
    
if __name__=="__main__":
    #pool = PooledDB(MySQLdb,1,host='122.152.206.246',user='oco',passwd='MyNewPass4!',db='task_zmm',port=3306,charset='utf8')
    #dbb0=dbop("122.152.206.246","oco","MyNewPass4!")
    #db0l=dbb0.run("show databases;")
    #print(db0l)
    dbb=dbop("172.23.250.51","root","20180712")
    dbl=dbb.run("show databases;") 
    #print dbb.run("use test0720")
    #print dbb.run("desc test0720xml")
    xml_num=0
    jpg_num=0
    for dbname in dbl:
        if "fourgesture_detection_train" not in  dbname[0]:
            continue
        #print dbname
        sqlstr="use %s;"%(dbname[0])
        dbb.run(sqlstr) 
        sqlstr="select count(*) from %sxml;"%(dbname[0])
	rr=dbb.run(sqlstr) 
        xml_num+=dbb.getnum(rr)
        xml_numtmp=dbb.getnum(rr)
        sqlstr="select count(*) from %simg"%(dbname[0])
	rr=dbb.run(sqlstr) 
        jpg_num+=dbb.getnum(rr)
        jpg_numtmp=dbb.getnum(rr)
        if xml_numtmp>0:
            print dbname[0]
	    print "xmltmp:%d,jpgtmp:%s"%(xml_numtmp,jpg_numtmp)
	    print "xml:%d,jpg:%s"%(xml_num,jpg_num)
    print dbb.help("sql") 
    #print len(dbl)
    #print type(list(dbl))
    #for db in dbl:
    #    print list(db)
