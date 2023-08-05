# -*- coding: utf-8 -*-
import xml.dom.minidom 
import os.path
from read import read
from IOU import IOU
import os


def Analyze_xml(standard_path,test_path):

    wrong,creat,pos=0,0,0
    ratio=0.
    list1=[]
    Reframe=GTframe=[]
    path1=standard_path
    path2=test_path
    files1 = os.listdir(path2)
    cc1=0
    cc2=0
    for xmlFile in files1:
        
        testpath_xml=os.path.join(path2,xmlFile)
        standpath_xml=testpath_xml.replace(path2,path1)
        print standpath_xml
        print testpath_xml
        if os.path.isfile(standpath_xml):
            dom_test=xml.dom.minidom.parse(testpath_xml)
            dom_stand=xml.dom.minidom.parse(standpath_xml)
            root1=dom_test.documentElement
            root2=dom_stand.documentElement
            #print root2
            #get_char()
            Reframe=read(root1)
            GTframe=read(root2)
            #print GTframe
            pos+=len(GTframe)
            cc1+=1
            if len(GTframe)>len(Reframe):
                for i in range(len(GTframe)-len(Reframe)):
                    list1.append([0,1,0])
                    
            for i in range(len(Reframe)):
                wrong=creat=0
                for j in range(len(GTframe)):
                    ratio=IOU(Reframe[i],GTframe[j])
                    score=Reframe[i][4]
                    if ratio>=0.5:
                        creat=1
                        list1.append([creat,wrong,ratio])
                        break
                if creat==0:
                    wrong=1
                    list1.append([creat,wrong,ratio])
                
        else:
            print "file not exist!"
            cc2+=1
            creat=wrong=0
            #print testpath_xml
            dom_test=xml.dom.minidom.parse(testpath_xml)
            root1=dom_test.documentElement
            Reframe=read(root1)
            for i in range(len(Reframe)):
                ratio=0
                wrong=1
                list1.append([creat,wrong,ratio])
        print cc1,cc2
    return list1,pos
            
        
