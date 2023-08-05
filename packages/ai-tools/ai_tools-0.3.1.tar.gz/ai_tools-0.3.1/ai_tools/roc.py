# -*- coding: utf-8 -*-
import pylab as pl
from Analyze_xml import Analyze_xml
import sys
def roc(standard_path="truth",test_path="test",result_roc='result_roc.txt'):

    db=[]
    print "analyze_xml:"
    db,pos=Analyze_xml(standard_path,test_path)
    db = sorted(db, key=lambda x:x[2], reverse=True)#sorted() 
    
    print pos 
    xy_arr = []
    tp,fp = 0., 0.			
    for i in range(len(db)):
        #print db
        tp += db[i][1]#wrong
        fp += db[i][0]#creat
        xy_arr.append([tp,fp/pos,db[i][2]])
   

    auc = 0.			
    prev_x = 0
    for x,y,t in xy_arr:
	    if x != prev_x:
		    auc += (x - prev_x) * y
		    prev_x = x
            
          
    x = [_a[0] for _a in xy_arr]
    y = [_a[1] for _a in xy_arr]
    pl.title("ROC (AUC = %.4f)" % (auc/float(x[-1])))
    pl.xlabel("False Count")
    pl.ylabel("True Positive Rate")
    pl.plot(x, y)
    pl.show()

    #with open(result_roc, 'w') as fp:
    #    for i in range(len(db)):
    #        fp.write("%d %f \n" % (x[i], y[i]))
    db=xy_arr
    with open(result_roc, 'w') as fp:
        for i in range(len(db)):
            fp.write("%d %d %f \n" % (db[i][0], db[i][1],db[i][2]))


def Analyze_score_vector(score_vector):
    '''
    score_vector
    1 0.8
    -1 0.3
    1 0.45
    ...
    -1 0.3

    '''
    db=[]
    pos=0
    with open(score_vector) as fh:
        for lines in fh.readlines():
            line=lines.strip('\n').split(' ')
            print line
            score=float(line[1])
            sample_type=float(line[0])
            if float(sample_type)==1:
                db.append([1,0,score])
                pos+=1
            else:
                db.append([0,1,score])
    return db,pos

def roc_score_matrix(score_vector="score_vector.txt",result_roc='result_roc.txt',result_IOU='result_IOU'):

    db=[]
    print "analyze_xml:"
    #db,pos=Analyze_xml(standard_path,test_path)
    db,pos=Analyze_score_vector(score_vector)
    db = sorted(db, key=lambda x:x[2], reverse=True)#sorted() 
    
    print pos 
    xy_arr = []
    tp,fp = 0., 0.			
    for i in range(len(db)):
        #print db
        tp += db[i][1]#wrong
        fp += db[i][0]#creat
        xy_arr.append([tp,fp/pos,db[i][2]])
   

    auc = 0.			
    prev_x = 0
    for x,y,t in xy_arr:
	    if x != prev_x:
		    auc += (x - prev_x) * y
		    prev_x = x
          
    x = [_a[0] for _a in xy_arr]
    y = [_a[1] for _a in xy_arr]
    pl.title("ROC (AUC = %.4f)" % (auc/float(x[-1])))
    pl.xlabel("False Count")
    pl.ylabel("True Positive Rate")
    pl.plot(x, y)
    pl.show()
    with open(result_roc, 'w') as fp:
        for i in range(len(db)):
            fp.write("%d %f \n" % (x[i], y[i]))
    db=xy_arr
    with open(result_IOU, 'w') as fp:
        for i in range(len(db)):
            fp.write("%d %d %f \n" % (db[i][0], db[i][1],db[i][2]))
    
def main_1(gt_dir,resultdir):
    #gt_dir=sys.argv[1]
    #resultdir=sys.argv[2]
    print gt_dir
    print resultdir
    roc(gt_dir,resultdir,'result_roc.txt')

def main_2():
    roc_score_matrix("score_vector.txt","result_roc.txt")


if __name__ == '__main__':
    gt_dir=sys.argv[1]
    resultdir=sys.argv[2]
    main_1(gt_dir,resultdir)
