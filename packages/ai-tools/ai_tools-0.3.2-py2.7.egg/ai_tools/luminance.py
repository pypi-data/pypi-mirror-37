import cv2
from zprint import *
import numpy as np    
import math
import pdb
from distutils.sysconfig import get_python_lib
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn import cross_validation, metrics
from sklearn.externals import joblib

data_dir="/data1/mingmingzhao/data_sets/luminance"
sppath=get_python_lib()
mpath=os.path.join(sppath,"ai_tools/data/clf.pkl")
print("%s exits: %s"%(mpath,os.path.exists(mpath)))
clf=joblib.load(mpath)
def splitimage(image,n_row,n_col):
    w=image.shape[0]
    h=image.shape[1]
    ws=w/n_col
    hs=h/n_row
    splits=[]
    for i in range(0,w,ws):
        for j in range(0,h,hs):
            tmp=image[j:j+hs,i:i+ws]
            #print tmp.shape,i,j,ws,hs
            tmp1=tmp.reshape((ws*hs))
            splits.append(tmp1)
            
    return splits 
def weights_sum(vallist,weights):
    #weights=[0.1,0.1.0.1,0.1,0.2,0.1,0.1,0.1,0.1]
    c=[]
    i=0
    v=0.0
    ws=0.0
    for iv in vallist:
        
        c.append(iv*weights[i])
        #print c
        v+=c[-1]
        #ws+=weights[i]
        i+=1
    #v=v/ws
    return v 

def analysys_luminance(image_list):
    c=[]
    weights=[0.1,0.1,0.1,0.1,0.2,0.1,0.1,0.1,0.1]
    i=0
    mean_i=[]
    val_i=[]
    min_i=[]
    max_i=[]
    for image in image_list:
        image=image/255.0
        #print image.mean(),image.var(),min(image),max(image)
        mean_i.append(image.mean())
        val_i.append(image.var())
        min_i.append(min(image))
        max_i.append(max(image)) 
        i+=1
    
    #print mean_i 
    mean_lumi=weights_sum(mean_i,[0.1,0.1,0.1,0.1,0.2,0.1,0.1,0.1,0.1])
    hori_lumi=weights_sum(mean_i,[  1,  1,  1,  0,  0,  0, -1, -1, -1])
    vert_lumi=weights_sum(mean_i,[  1,  0, -1,  1,  0, -1,  1,  0, -1])
    slop_lumi=weights_sum(mean_i,[  0, -1, -1,  1,  0, -1,  1,  1,  0])
    tl_lumi  =weights_sum(mean_i,[  1,  0,  0,  0,  0,  0,  0,  0,  0])
    tr_lumi  =weights_sum(mean_i,[  0,  0,  0,  0,  0,  0,  1,  0,  0])
    lumi={}
    lumi['mean']=mean_lumi
    lumi['hori']=hori_lumi
    lumi['vert']=vert_lumi
    lumi['slop']=slop_lumi
    lumi['tl']=tl_lumi
    lumi['tr']=tr_lumi
    lumi['max']=max(mean_i)
    lumi['min']=min(mean_i)


    return lumi 
def get_Y(image):
    xyz=cv2.cvtColor(image,cv2.COLOR_BGR2XYZ)
    #cv2.cvtColor(image,xyz,cv2.COLOR_BGR2GRAY)
    channels=cv2.split(xyz)
    Yt=channels[1]
    return Yt
def get_sp(image):
    Yt=get_Y(image)
    Y=cv2.resize(Yt,(300,300),interpolation=cv2.INTER_CUBIC)
    sp=splitimage(Y,3,3)
    return sp
def luminance(image):
    sp=get_sp(image)
    zprint("lensp=%s"%(len(sp)))
    luminance=analysys_luminance(sp)
    #print luminance 
    return luminance
def nhist(image,bins_num=256,is_Y=0):
    if is_Y==0:
        y=get_Y(image)
    else:
        y=image
    hist=np.zeros((256))
    #pdb.set_trace()
    hist_n=np.zeros((bins_num+1))
    hist_x=np.zeros((bins_num+1))
    for i in range(0,bins_num+1):
        hist_x[i]=i
    #for yc in y.reshape((y.shape[0]*y.shape[1])):
    for yc in y:
        hist[yc]+=1
    zprint(hist)
    for i in range(0,256):
        index=int(math.floor(float(i)/(256.0/float(bins_num))))
        #zprint("%s,%s"%(i,index))
        hist_n[index]+=hist[i]
    hist_n/=hist_n.sum()
    return hist_n,hist_x
def concat(a1,a2,direction=0):
    s1=a1.shape[0]
    s2=a2.shape[0]
    histo=np.zeros((s1+s2))
    histo[0:s1]=a1
    histo[s1:s1+s2]=a2
    return histo
    
def get_9hist(image):
    sp=get_sp(image)
    hist9=np.zeros((81))
    c=0
    for spc in sp:
        spc_hist,_=nhist(spc,9,1)
        hist9[c:c+9]=spc_hist[0:9]
        c+=9  
    #zprint(hist9)
    return hist9
def get_imglist_histfeature(imglist):
    if len(imglist)==0:
        return np.zeros((60,60))*-1
    histimg=np.zeros((len(imglist),117))
    for i in range(0,len(imglist)):
        zprint(i)
        img=imglist[i]
        hist36,_=nhist(img,36)
        hist81=get_9hist(img)
        print(hist36.shape)
        print(hist81.shape)

        hist117=concat(hist36,hist81)
        histimg[i,0:36]=hist36[0:36]*4
        histimg[i,36:36+81]=hist81[0:81]
    histimg=cv2.resize(histimg,(60,60),interpolation=cv2.INTER_CUBIC)
    return histimg
def lumi_classify_histimg(histimg):
    global clf 
    histimg*=255.0
    histimg.astype("uint8") 
    x=histimg.reshape((1,histimg.shape[0]*histimg.shape[1]))
    y_pred = clf.predict_proba(x)
    y_pred_sort_index=np.argsort(y_pred)
    y_pred_l=y_pred_sort_index[:,-1]
    ddict=["normal","darkest","darker","lighter","sun"]
    #ddict=["normal","darkest","darker","lighter","sun"]
    return ddict[y_pred_l[0]]
def lumi_classify(imglist):
    return lumi_classify_histimg(get_imglist_histfeature(imglist))
if __name__=="__main__":
    imgf="/root/jz9d701f00163d44ffa167d1e0455ea228_0_thumbnail.jpg"
    img=cv2.imread(imgf)
    #img=np.random.rand(60,60)
    histimg=get_imglist_histfeature([img])
    print(lumi_classify_histimg(histimg))
    #image=cv2.imread("roc.jpg")
    image=cv2.imread(imgf)
    lumi=luminance(image)
    print(lumi)
    print(lumi['mean'])
