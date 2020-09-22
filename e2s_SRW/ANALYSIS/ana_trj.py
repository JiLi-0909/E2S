# -*- coding: utf-8 -*-
#############################################################################
# reading output file and plot flux curve ... MA 11/1/2018
#
#  python ana_flux.py  ex08_res_int1.dat
#
#############################################################################

from __future__ import print_function #Python 2.7 compatibility
import sys
import os
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np


def read_data_file(FILIN):
    f = open(FILIN, 'r')
    
    header = f.readline()
    
    data = []
    
    for line in f:
        line = line.strip()
        columns = line.split()
        
        data.append(columns)
        
        
    return data,header


    
FILIN = sys.argv[1]

data,header = read_data_file(FILIN)
atad  = np.transpose(data)

x = atad[1][1:]
xp = atad[2][1:]
z = atad[5][1:]
by = atad[8][1:]

#----------JL modified to corect the type---------------------------
Xp = np.array(xp, dtype=np.float32)
X = np.array(x, dtype=np.float32)
Z = np.array(z, dtype=np.float32)
By = np.array(by, dtype=np.float32)

numpy.savetxt('/dls/physics/students/sug89938/E2S/e2s_SRW/3PW.txt',Z,fmt='%f',delimiter=' ',newline='\r\n')

#----------old ver.---------------------------
#Xp = xp.astype(np.float)
#X  = x.astype(np.float)
#Z  = z.astype(np.float)
#By = by.astype(np.float)

#-------------------------------------
#print(header)
#print(data[2])
#fig, ax = plt.subplots(nrows=1, ncols=1)
#cpf = ax.plot(E,np.log(F))
#plt.xscale('log')
#plt.yscale('log')

cpf1 = plt.plot(Z,X)
#cpf2 = plt.plot(Z,By)
#cpf2 = ax.plot(E2,F2)
cpf2 = plt.plot(Z,By)

plt.subplot(3,1,1)
plt.plot(Z,By)
plt.ylabel('By (T)')
#plt.title('B18 case - By=1.4T')
#plt.title('I22m case - By=0.2T')
#plt.title('3PW DII case - By=1.454T')
#plt.title('3PW DII case - I22m - By=0.2T')
#plt.title('3PW DII case - K22 - By=0.2T')
plt.xlim((-3.5,3.5))
plt.title('3PW M-H6BA - K18 - By=1.45T/0.04T')
plt.grid('true','which','both')
plt.grid(True,which="both",ls="-")

plt.subplot(3,1,2)
plt.plot(Z,X*1e6)
plt.xlim((-3.5,3.5))
#plt.ylim((-50,300))
plt.ylim((-5000,5000))
#plt.ylim((-1000,26000))
#plt.ylim((-200,3000))
plt.ylabel('X (um)')
plt.grid('true','which','both')
plt.grid(True,which="both",ls="-")

plt.subplot(3,1,3)
plt.plot(Z,Xp*1e3)
plt.xlim((-3.5,3.5))
#plt.ylim((-10,10))
plt.ylim((-4.,4.))
#plt.ylim((-10,30))
#plt.ylim((-100,100))
plt.ylabel('Xp (mrad)')
plt.xlabel('S (m)')
plt.grid('true','which','both')
plt.grid(True,which="both",ls="-")


plt.show()


