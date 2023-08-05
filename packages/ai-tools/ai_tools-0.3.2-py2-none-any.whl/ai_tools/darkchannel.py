import cv2
import numpy as np
# zhaomingming
# 20180917
# the code for <<Single Image Haze Removal Using Dark Channel Prior>>


def get_Jc(img):
    print(img.shape)
    imgmin=img.min(2)
    Jc=imgmin.copy()
    print(imgmin.shape)
    #return img[:,:,0],img[:,:,1],img[:,:,2]
    return Jc 
def get_Jc_max(img):
    print(img.shape)
    imgmax=img.max(2)
    Jc=imgmax.copy()
    print(imgmax.shape)
    #return img[:,:,0],img[:,:,1],img[:,:,2]
    return Jc 
def get_Jdark_from_Jc(Jc,omiga_ridas=7):
    cols=Jc.shape[1]
    rows=Jc.shape[0]
    image=Jc 
    image_49channel=np.zeros((rows,cols,49))
    for i in range(0,7):
        for j in range(0,7):
            #affineShrinkTranslation = np.array([[0.5, 0, cols/4], [0, 0.5, rows/4]], np.float32)
            affineShrinkTranslation = np.array([[1, 0, i], [0, 1, j]], np.float32)
            shrinkTwoTimesTranslation = cv2.warpAffine(image, affineShrinkTranslation, (cols, rows), borderValue=255)
            image_49channel[:,:,i*7+j]=shrinkTwoTimesTranslation
    print(image_49channel.shape)
    Jdark=image_49channel.min(2)
    print(Jdark.shape) 
    return Jdark
def get_Jdark(img):
    Jc=get_Jc(img)
    return get_Jdark_from_Jc(Jc)
def get_Jdark_from_file(imgf):
    #img=cv2.imread("ai_tools/temp.jpg")
    img=cv2.imread(imgf)
    return get_Jdark(img)
def get_A_1(img,Jdark):
    # get the top 1% pix's position
    Jdarklist=np.zeros((3,Jdark.shape[0]*Jdark.shape[1]),dtype="int64")
    for i in range(0,Jdark.shape[0]):
        print(i,i*Jdark.shape[1])
        for j in range(0,Jdark.shape[1]):
            #Jdarklist[:,i*Jdark.shape[0]+j]=np.array((i,j,Jdark[i,j]))
            Jdarklist[0,i*Jdark.shape[1]+j]=i
            Jdarklist[1,i*Jdark.shape[1]+j]=j
            #Jdarklist[2,i*Jdark.shape[1]+j]=i*Jdark.shape[1]+j
            Jdarklist[2,i*Jdark.shape[1]+j]=Jdark[i,j]
            #print(np.array((i,j,i*Jdark.shape[0]+j),dtype="int64"))
    top_percent_one=int(round(Jdarklist[2,:].shape[0]*0.01))
    
    print(top_percent_one)
    sort_index=np.argsort(Jdarklist[2,:])
    print(sort_index)
    print(sort_index.shape)
    #print(Jdarklist[2,Jdark.shape[0]*Jdark.shape[1]-1-np.argsort(Jdarklist[2,:])])
    print(Jdarklist[2,np.argsort(Jdarklist[2,:])])
    top_x=Jdarklist[1,sort_index[-top_percent_one:-1]]
    top_y=(Jdarklist[0,sort_index[-top_percent_one:-1]])
    #print(Jdarklist[1,sort_index[-top_percent_one:-1]])
    #print(Jdarklist[0,sort_index[-top_percent_one:-1]])
     
    #print(Jdarklist[2,-10:-1])
    #print(Jdarklist[0,1:10])
def get_A(img,Jdark):
    # get the top 1% pix's position
    Jc_light=get_Jc_max(img)
    Jc_light_1=Jc_light.reshape((Jc_light.shape[0]*Jc_light.shape[1]))
    print(Jc_light_1)
    Jdark_1=Jdark.copy()
    Jdark_1=Jdark_1.reshape((Jdark_1.shape[0]*Jdark_1.shape[1]))
    top_num=int(round(Jdark_1.shape[0]*0.01))
    print(Jc_light_1[np.argsort(Jdark_1)])
    Jc_light_2=Jc_light_1[np.argsort(Jdark_1)]
    print("A=%s"%(Jc_light_2[-top_num:-1].max())) 
    A=Jc_light_2[-top_num:-1].max()
    A=float(A)
    print(type(A))
    A = 0.0001 if A == 0 else A
    print("A=%s"%(Jc_light_2[-top_num:-1].max())) 
    #return Jc_light_2[-top_num:-1].max()
    return A
def get_T(img,A):
    img1=img.astype(np.float64)
    
    A1=A
    #A1=A.astype(np.float64)
    print("A=%s,A1=%s"%(A,A1))
    T=1-0.5*get_Jdark(img1/A1)
    T[T<0.1]=0.1
    print("img1:")
    print(img1.shape)
    print(img1/A1)
    print(T.shape)
    return T
def c123(M):
    return np.stack([M,M,M],2)
def get_J_from_T(img,A,T):
    img1=img.astype(np.float64)
    #A1=A.astype(np.float64)
    A1=float(A)
    T1=T.astype(np.float64)
    J=(img1-A1)/T1+A1 
    return J

def get_J(img):
    Jdark = get_Jdark(img)
    cv2.imwrite("Jdark.png",Jdark)
    A = get_A(img,Jdark)
    T = get_T(img,A)
    J = get_J_from_T(img,A,c123(T))
    return J
def test():
    img=cv2.imread("ai_tools/temp.jpg")
    Jc=get_Jc(img)
    get_Jdark(Jc)
if __name__=="__main__":
    img=cv2.imread("ai_tools/temp.jpg")
    img=cv2.imread("haze_img1.png")
    get_Jdark(img)
    Jdark=get_Jdark_from_file("ai_tools/temp.jpg")
    cv2.imwrite("Jdark.jpg",Jdark)
    #get_A_1(img,Jdark)
    J=get_J(img)
    print(J)
    
    cv2.imwrite("haze_out.jpg",J)
