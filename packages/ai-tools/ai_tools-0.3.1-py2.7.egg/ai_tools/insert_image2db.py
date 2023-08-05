# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 18:34:07 2018

@author: wuhongrui
"""

import sys
import MySQLdb
import os
from PIL import Image

def image2db():

    #本地图片所在路径
    localpath = "D:/file/try/try_png"
    projectName = 'name'
    #建立一个MySQL连接
    db = MySQLdb.connect(host="localhost", user="root", passwd="123456", charset='utf8')

    # 创建游标
    cursor = db.cursor()
    #创建项目数据库
    cursor.execute("CREATE DATABASE if not exists %s DEFAULT CHARACTER SET utf8" % projectName)
    cursor.execute("USE %s" % projectName)

    #创建保存图片数据的表格
    imgTbName = projectName+'img'
    sql = "Create table if not exists %s (id int(10) unsigned primary key auto_increment, image_name varchar(200), raw_data longblob, is_marking char(20) default 'no', if_verify char(20) default 'no') default character set utf8"% imgTbName
    cursor.execute(sql)

    #从本地读取图片文件存入数据库
    for imagefile in os.listdir(localpath):
        with open(os.path.join(localpath, imagefile), "rb") as f:
            img_data = f.read()
            f.close()

        image_name = str(imagefile)[:-4]

        sql = "INSERT INTO %s (image_name, raw_data) VALUES ('%s', '%s')" % (imgTbName, image_name, MySQLdb.escape_string(img_data))
        cursor.execute(sql)
        db.commit()

    #创建储存标注数据的表格
    xmlTbName = projectName+'xml'
    sql = "Create table if not exists %s (id int(10) unsigned primary key auto_increment, image_name varchar(200), xml_content varchar(2000), marker_id char(20)) default character set utf8"%  xmlTbName
    cursor.execute(sql)

    db.commit()
    cursor.close()
    db.close()
def insert2db(image_name,projectName,dbindex=0):

    #建立一个MySQL连
    if dbindex==0:
        db = MySQLdb.connect(host="172.23.250.51", user="root", passwd="20180712", charset='utf8')
    if dbindex==1:
        db = MySQLdb.connect(host="10.106.5.9", user="oco", passwd="MyNewPass4!", charset='utf8')
    # 创建游标
    cursor = db.cursor()
    #创建项目数据库
    cursor.execute("CREATE DATABASE if not exists %s DEFAULT CHARACTER SET utf8" % projectName)
    cursor.execute("USE %s" % projectName)

    #创建保存图片数据的表格
    imgTbName = projectName+'img'
    sql = "Create table if not exists %s (id int(10) unsigned primary key auto_increment, image_name varchar(200), raw_data longblob, is_marking char(20) default 'no', if_verify char(20) default 'no') default character set utf8"% imgTbName
    cursor.execute(sql)

    #从本地读取图片文件存入数据库
    #for imagefile in os.listdir(localpath):
    if 1:
        with open(os.path.join(image_name), "rb") as f:
            img_data = f.read()
            f.close()

        #image_name = str(imagefile)[:-4]

        sql = "INSERT INTO %s (image_name, raw_data) VALUES ('%s', '%s')" % (imgTbName, image_name, MySQLdb.escape_string(img_data))
        print("insert %s into %s.%s"%(image_name,projectName,imgTbName))
        cursor.execute(sql)
        db.commit()

    #创建储存标注数据的表格
    xmlTbName = projectName+'xml'
    sql = "Create table if not exists %s (id int(10) unsigned primary key auto_increment, image_name varchar(200), xml_content varchar(2000), marker_id char(20)) default character set utf8"%  xmlTbName
    cursor.execute(sql)

    db.commit()
    cursor.close()
    db.close()

def create_db(projectName):

    #建立一个MySQL连
    db = MySQLdb.connect(host="172.23.250.51", user="root", passwd="20180712", charset='utf8')

    # 创建游标
    cursor = db.cursor()
    #创建项目数据库
    cursor.execute("CREATE DATABASE if not exists %s DEFAULT CHARACTER SET utf8" % projectName)
    cursor.execute("USE %s" % projectName)

    #创建保存图片数据的表格
    imgTbName = projectName+'img'
    sql = "Create table if not exists %s (id int(10) unsigned primary key auto_increment, image_name varchar(200), raw_data longblob, is_marking char(20) default 'no', if_verify char(20) default 'no') default character set utf8"% imgTbName
    cursor.execute(sql)


    #创建储存标注数据的表格
    xmlTbName = projectName+'xml'
    sql = "Create table if not exists %s (id int(10) unsigned primary key auto_increment, image_name varchar(200), xml_content varchar(2000), marker_id char(20)) default character set utf8"%  xmlTbName
    cursor.execute(sql)

    db.commit()
    cursor.close()
    db.close()


def jpg2png():

    #本地图片所在路径和png图片保存路径
    jpgpath = "D:/file/try/try_jpg"
    pngpath = "D:/file/try/try_png"
    for imagefile in os.listdir(jpgpath):
        f = Image.open(os.path.join(jpgpath, imagefile))
        imagefile = str(imagefile)[:-4]+'.png'
        f.save(os.path.join(pngpath, imagefile))

if __name__=="__main__":
    create_db("similar_students_010")
    create_db("similar_students_011")
    create_db("similar_students_012")
    create_db("similar_students_013")
    create_db("similar_students_014")
    #create_db("similar_students_002")
    #create_db("similar_students_003")
    #create_db("similar_students_004")
    #jpg2png()
    #image2db()
