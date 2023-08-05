# -*- coding: utf-8 -*-
from vcvf import face_detector as fd
import cv2
import os




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
        pathn+=".txt"
        with open(pathn, 'w') as fp:
            fp.write("%s %d " % (name, num))
            for i in range(num):
                list2=str(list1[i])
                list2=list2[1:-1]
                print list2
                fp.write("%s " % list2)
    print 'vcvf_txt() is OK'

if __name__ == '__main__':
    img_dir="D:\zmm\moba\home\intern_mission\\bndbox_test2\\bndbox_test\\vcvf_txt\pre_file"
    resultdir="D:\zmm\moba\home\intern_mission\\bndbox_test2\caculate_roc\\predict_result"
    predict(img_dir,resultdir)
