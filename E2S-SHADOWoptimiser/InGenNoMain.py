

# constructed from "fct_update_BLoptics_withloop.py"

"""

shadow optimisation
Created on 16 Jan 2018

@author: JL
   
"""

import os
import sys
import subprocess
import glob
import time
#import interpol
from pprint import pprint

#from fct_get_BLoptics  import DefineBLOptics
#from BLGenerator  import BLGen
from BL_optics_rays import BLoptics#JL:modified to build BL optics
from BL_optics_rays import Calcrays #JL:modified to simulate
from BL_optics_rays import update_BL #JL:modified to simulate

#from ana_intensity_new_BLasParam import GetSampleStruct

import numpy as np

## NOTE : In this version, we don't use the file e2s_BLOPTICS/fct_update_BLOPTIcs.py. Instead, we use a function within this file called update_BL. This works much better.







"""    
2D
def update_BL(loelem,loval):
# update_BL: create the new beamline
# loelem: list of optical elements (that will be updated)
# loval:list of (new) optical values
# No need to return anything, as the Beamline is transformed directly in this function    
    for index, item in enumerate(loelem, start = 0):
        print('-------------------------------')
        print index, item
        print('it must next be:')
        print loval[index]
        item.L= loval[index]
        print('it is now:')
        print item.L
        new_oe=item
"""


# this one here is to update I20: the indexation of elements will be different
def update_BL_old(loelem,loval):
# update_BL: create the new beamline
# loelem: list of optical elements (that will be updated)
# loval:list of (new) optical values
# No need to return anything, as the Beamline is transformed directly in this function
    print(' Now in InGenNoMain.update_BL')
    print('loelem is:')
    print(loelem)
    print('loval is')
    print(loval)   
    print('starting the enumeration on the list of optical elements (l.o.elem), note that this number is smaller or equal to the list of values to be modified (l.o.val.) so must be very careful here !!!!')
    for index, item in enumerate(loelem, start = 0): 
        #print('-------------------------------')
        #print index, item
        #print('it must next be:')
        #print loval[index]
        if index ==0:
            item=loval[0]

        if index==1:
            item=loval[1]         
        
        if index==2:
            item=loval[2]

        if index ==3:
            item=loval[3]

        if index==4:
            item=loval[4]         
        
        if index==5:
            item=loval[5]

        if index ==6:
            item=loval[6]       
        
        #if index==3:             #HERE and
        #    item.q= loval[3] #HERE

        #if index==4:             #HERE and
        #    item.L= loval[4] #HERE

        new_oe=item
    print('end of the updating process. Quitting function...new_oe',new_oe)
    return new_oe


def func_optBL(k1,k2,k3,k4,k5,k6,k7,rootnumber):    # NOTE : ROOTNUMBER TAG HERE #HERE


    print('JL:this is for beamline optimisation(raytracing)')#JL:put the targets parameters name
    par1= 'oe9.T_SOURCE'
    par2='oe10.T_SOURCE'
    par3='oe10.T_IMAGE'
    par4= 'oe9.SSOUR'
    par5='oe9.SIMAG'
    par6='oe10.SSOUR'
    par7='oe10.SIMAG'

    oe = BLoptics(par1,par2,par3,par4,par5,par6,par7)
    
    loelem= [oe[0],oe[1],oe[2],oe[3],oe[4],oe[5],oe[6]] #HERE is K18


    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    loval=[k1,k2,k3,k4,k5,k6,k7] #HERE

    print('Values before modification:')  # WITH MONO
    print(oe[0])
    print(oe[1])
    print(oe[2])
    print(oe[3])
    print(oe[4])
    print(oe[5])
    print(oe[6])




    #update_BL(par1,par2,par3,k1,k2,k3)
    #update_BL_old(loelem,loval)
    #optBL = SRWLOptC(oe0[0],oe0[1])



    

    print(' We are now going to raytracing. We will use the Calcrays function imported from python version of shadow beamline ')
    fwhmh,fwhmv=Calcrays(k1,k2,k3,k4,k5,k6,k7,rootnumber) # NOTE : ROOTNUMBER TAG HERE

    
    print('The structure of photons at sample is given by:')
    #print('Imax vaut :', Imax)
    print('fwhmh :', fwhmh)
    print('fwhmv :', fwhmv)
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    
    #return -Imax,sigx,sigy written like that, the plot.py function in nsga() will crash and say :
    #FBT: -------------------------------------
    #[[ -1.54747905e+18   1.31975865e+01]
    # [ -3.17705946e+17   1.21195044e+01]]
    # FBT: -------------------------------------
    #Traceback (most recent call last):
    #  File "plot.py", line 66, in <module>
    #    plot(directory, flip_axis)
    #  File "plot.py", line 41, in plot
    #    points = sorted(points)
    #ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
    # see: https://stackoverflow.com/questions/10062954/valueerror-the-truth-value-of-an-array-with-more-than-one-element-is-ambiguous

    ##return(-Imax,sigx)
    return (fwhmh,fwhmv)  
















