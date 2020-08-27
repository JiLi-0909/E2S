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
from scipy import integrate

# Open file
# FILIN = 'ex08_res_int1.dat' 
   
FILIN = sys.argv[1]

f = open(FILIN, 'r')

header = {}
#for i in range(0, 100):
flag = 1
i    = 0
while flag > 0:
    linea     = f.readline()
    if linea[0] is '#':
        header[i] = linea
        if 'Initial Photon Energy' in header[i]:
            lin     = header[i].strip()
            col     = lin.split()
            Emin = col[0]
            Emin = Emin[1:]
            emin = float(Emin)
            #print(header[i],i)
           
        if 'Final Photon Energy' in header[i]:
            lin     = header[i].strip()
            col     = lin.split()
            Emax = col[0]
            Emax = Emax[1:]
            emax = float(Emax)
            #print(header[i],i)

        if 'Number of points vs Photon Energy' in header[i]:
            lin     = header[i].strip()
            col     = lin.split()
            Epoints = col[0]
            Epoints = Epoints[1:]
            epoints = int(Epoints)
            #print(header[i],i)

        if 'Initial' in header[i]:
            lin     = header[i].strip()
            col     = lin.split()
            Xmin = col[0]
            Xmin = Xmin[1:]
            xmin = float(Xmin)
            #print(header[i],i)

        if 'Final ' in header[i]:
            lin     = header[i].strip()
            col     = lin.split()
            Xmax = col[0]
            Xmax = Xmax[1:]
            xmax = float(Xmax)
            #print(header[i],i)

        if 'Initial ' in header[i]:
            lin     = header[i].strip()
            col     = lin.split()
            Ymin = col[0]
            Ymin = Ymin[1:]
            ymin = float(Ymin)
            #print(header[i],i)

        if 'Final ' in header[i]:
            lin     = header[i].strip()
            col     = lin.split()
            Ymax = col[0]
            Ymax = Ymax[1:]
            ymax = float(Ymax)
     	    #print(header[i],i)
        i = i + 1
        
    else:
        flag = -1 
  


# Loop over lines and extract variables of interest
cnt = 0
data = []
columns = linea.split()
data.append(float(columns[0]))  # the first data.append is on the linea 

for line in f:
    line = line.strip()
    columns = line.split()
    
    
    data.append(float(columns[0]))
    #print(data[cnt])
    cnt=cnt+1

f.close()

Z = data

F=np.array(Z)

E = []
for iE in range(0,epoints):
    E.append(emin + (emax-emin)/epoints*(iE-1))

#for i in range(len(F)):
#	if F[i] > 5e+12:
#           print (E[i])



fig, ax = plt.subplots(nrows=1, ncols=1)
#cpf = ax.plot(E,np.log(F))
cpf = ax.plot(E,F)
power=integrate.simps(F, E, axis=-1, even='avg')
eV2J=1e-19*1.602
power=power*1000*eV2J
print('P= '+str(power)+' (W)')
Dx = 0.3 #xmax-xmin
Dy = 0.12 # ymax-ymin
power_dens=power / Dx / Dy
print('P_dens= '+str(power_dens)+' (W/mm2)')


plt.show()


