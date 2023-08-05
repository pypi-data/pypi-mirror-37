
import numpy as np


thresh=0.4
ovr=np.array([0.3,0.4,0.5,0.3])
inds = np.where(ovr <= thresh)[0]
#inds = np.where(ovr <= thresh)
print inds
print inds+1
