
from __future__ import print_function #Python 2.7 compatibility
import sys
import os
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np


FILIN = sys.argv[1]

f = open(FILIN, 'r')
    
header = {}

B = [] 
 
while True:
    linea     = f.readline().strip()
    if linea == '':
        break
    elif linea[0] == '#':
        print('skip header ...')
    else:
        B.append(float(linea.split()[1]))

f.close()

X  = np.arange(-3.5,3.5,3.0001714384e-04)
print(np.shape(X),np.shape(B))

np.savetxt(r'K18.txt', np.column_stack((X,B)),fmt='%.8f %.8f')
#np.savetxt('3PW_test.txt', (X,B))   



#Bx [T], By [T], Bz [T] on 3D mesh: inmost loop vs X (horizontal transverse position), outmost loop vs Z (longitudinal position)
#0. #initial X position [m]
#0. #step of X [m]
#1 #number of points vs X
#0. #initial Y position [m]
#0. #step of Y [m]
#1 #number of points vs Y
#-3.5 #initial Z position [m]
#3.0001714384e-04 #step of Z [m]
#23333 #number of points vs Z
