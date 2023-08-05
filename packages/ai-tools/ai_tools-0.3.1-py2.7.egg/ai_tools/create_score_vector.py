import os
import random


def logw(fh,message):
    print(message)
    fh.write(message)
def create_score_vector(num):
    
    fh=open("score_vector.txt","w")
    for i in range(0,num):
        sample_type=-1
        if random.random()>0.5:
            sample_type=1
        
        score=random.random()
        logw(fh,"%d %f\n"%(sample_type,score))
        
    fh.close()
create_score_vector(100)
