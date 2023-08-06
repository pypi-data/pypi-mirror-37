# -*- coding: utf-8 -*-
#  this file is intended to used in the debugger
# write a script that calls your function to debug it

import jscatter as js
import numpy as np
import sys
# some arrays
w=np.r_[-100:100]
q=np.r_[0.001:5:0.01]
x=np.r_[1:10]


R=3;NN=20;relError=50
grid= np.mgrid[-R:R:1j*NN, -R:R:1j*NN,-2*R:2*R:2j*NN].reshape(3,-1).T
p=1;p2=1*2 # p defines a superball with 1->sphere p=inf cuboid ....
inside=lambda xyz,R1,R2,R3:(np.abs(xyz[:,0])/R1)**p2+(np.abs(xyz[:,1])/R2)**p2+(np.abs(xyz[:,2])/R3)**p2<=1
insidegrid=grid[inside(grid,R,R,2*R)]
q=np.r_[0.1,0.4,0.6]
ffe=js.ff.cloudScattering(q,insidegrid,relError=0.1)

