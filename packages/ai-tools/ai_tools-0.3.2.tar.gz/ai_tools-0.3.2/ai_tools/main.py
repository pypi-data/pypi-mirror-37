




# predict

# -*- coding: utf-8 -*-
import xml.dom.minidom
from vcvf import face_detector as fd
import cv2
import os
from roc import *


def predict(img_dir,reusltdir):

    fd1=fd.face_detector(1)
    files1 =os.listdir(img_dir)
    for xmlFile in files1:
        list1=[]
        name=xmlFile[:-4]
        imf=os.path.join(img_dir,xmlFile)
        print imf
        image=cv2.imread(imf)

        num,list1,time=fd1.detect_face(image)

        pathn=os.path.join(resultdir,xmlFile)
        pathn=pathn[:-4]+".xml"
        txtfile="tmp.txt"
        with open(txtfile, 'w') as fp:
            fp.write("%s %d " % (name, num))
            for i in range(num):
                list2=str(list1[i])
                list2=list2[1:-1]
                print list2
                fp.write("%s " % list2)
        xmlfilename=pathn
        txt2xml(txtfile,xmlfilename) 

def txt2xml(xmlfilename,txtfilename):
    with open(xmlfilename,'r') as fs:
            managerList=[]
            doc = xml.dom.minidom.Document()
            root = doc.createElement('Recognition')
            root.setAttribute('type', 'face')
            doc.appendChild(root)

            str=fs.read()
            line=str.split()
            print line
            for i in range(0,int(line[1])):
                managerList.append([{'xmin':line[2+i*4],'ymin':line[3+i*4],'xmax':line[4+i*4],'ymax':line[5+i*4]}])

            for i in managerList :
                for j in range(len(i)):
                    nodeManager = doc.createElement('bndbox')
                    nodeXmin = doc.createElement("xmin")
                    nodeXmin.appendChild(doc.createTextNode(i[j]['xmin']))
                    nodeYmin = doc.createElement("ymin")
                    nodeYmin.appendChild(doc.createTextNode(i[j]['ymin']))
                    nodeXmax = doc.createElement("xmax")
                    nodeXmax.appendChild(doc.createTextNode(i[j]['xmax']))
                    nodeYmax = doc.createElement("ymax")
                    nodeYmax.appendChild(doc.createTextNode(i[j]['ymax']))


                    nodeManager.appendChild(nodeXmin)
                    nodeManager.appendChild(nodeYmin)
                    nodeManager.appendChild(nodeXmax)
                    nodeManager.appendChild(nodeYmax)
                    root.appendChild(nodeManager)

            print line[0]
            #pathn=os.path.join(after_file,line[0])
            #pathn=os.path.join(pathn,".xml")
            #pathn+=".xml"
            #fp = open(pathn, 'w')
            fp = open(txtfilename, 'w')
            doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")

# caculate
if __name__ == '__main__':
    img_dir ="D:\zmm\moba\home\intern_mission\\bndbox_test2\\bndbox_test\\vcvf_txt\pre_file"
    resultdir="D:\zmm\moba\home\intern_mission\\bndbox_test2\caculate_roc\\predict_result1"
    gt_dir="D:\\zmm\\moba\\home\\intern_mission\\bndbox_test2\\caculate_roc\\gt"
    #predict(img_dir,resultdir)
    roc(gt_dir,resultdir,'result_roc.txt',"result_IOU.txt")
    
