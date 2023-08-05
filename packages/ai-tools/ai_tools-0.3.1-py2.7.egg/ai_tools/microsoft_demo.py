import cognitive_face as CF
import json
import numpy as np
import sys
from zprint import *

def init():
    #KEY = 'subscription key'  # Replace with a valid Subscription Key here.
    #KEY = '74bc910571cd4785991d003b30c2a783'
    #KEY = '6a78402ab44140aba9e2014e0c7263ea'
    KEY = '8f7fbf07deb944258ff459ef22b1fac2'
    CF.Key.set(KEY)
    #https://eastasia.api.cognitive.microsoft.com/face/v1.0
    #BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
    BASE_URL = 'https://eastasia.api.cognitive.microsoft.com/face/v1.0'
    CF.BaseUrl.set(BASE_URL)
    #img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
    return CF
def detect(CF,img_url):
    #img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
    try:
        result = CF.face.detect(img_url)
        return result
    except Exception as e:
        eprint("%s"%(e))
        eprint("img_url:%s"%(img_url))
        #print(e)
        #return detect(CF,img_url)
        return []

def ms_face_detect(img_url):
    CF=init()
    result=detect(CF,img_url)
    #print(result)
    cc=0
    rects=[]
    faceids=[]
    for re in result:
        #{u'faceId': u'4076f1f6-3461-4c8b-9113-647e17230d85', u'faceRectangle': {u'width': 101, u'top': 67, u'height': 101, u'left': 137}}
        cc+=1
        #np.array((0,0,faces[0][0],faces[0][1])) 
        #print cc
        rer=re[u'faceRectangle']
        #print rer[u'width']
        #print rer[u'top']
        #print rer[u'height']
        #print rer[u'left']
        #dic=json.loads(re)
        #print dic
        rects.append(np.array((rer[u'left'],rer[u'top'],rer[u'width'],rer[u'height'])))
        faceids.append(re[u'faceId'])
    return rects

def ms_face_verify(CF,img_url1,img_url2):
     result1=detect(CF,img_url1)
     result2=detect(CF,img_url2)
     confidence_list=[]
     for re1 in result1:
         #print re1
         for re2 in result2:
             #print re2
             vr=CF.face.verify(re1[u'faceId'],re2[u'faceId'])
             confidence=vr[u'confidence']
             #print confidence
             confidence_list.append(confidence)
     return confidence_list


img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
img_url2 = '/data1/mingmingzhao/label/data_sets_teacher_1w/47017613_1510574400_out-video-jzc70f41fa6f7145b4b66738f81f082b65_f_1510574403268_t_1510575931221.flv_0001.jpg'
#print(ms_face_detect(img_url))
CF=init()
cl=ms_face_verify(CF,img_url,img_url2)
print cl

