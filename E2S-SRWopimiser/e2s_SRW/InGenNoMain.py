

# constructed from "fct_update_BLoptics_withloop.py"

"""

fct_update_BLoptics
Created on 03 oct 2018

@author: FBT

description: generates a BL of a known family, with a new set of parameters    
"""

import os
import sys
import subprocess
import glob
import time
#import interpol
from pprint import pprint


SRWLIB      = '/dls/physics/xph53246/source_to_beamline/SRWLIB/' # MA 12/03/2018 - repository created for pure SRWlib files 
sys.path.insert(0, SRWLIB)
from srwlib import *
from uti_plot import *

#sys.path.insert(0, '/dls/physics/mfc33124/NSGA_E2S_01_backup_ok_2param_d13_d15_copy/e2s_BLOPTICS/')
#sys.path.insert(0, '/dls/physics/mfc33124/NSGA_E2S_01_backup_ok_2param_d13_d15_copy/e2s_SRW/ANALYSIS/')
sys.path.insert(0, '/E2S_JL/E2S-SRWopimiser/e2s_BLOPTICS/')
sys.path.insert(0, '/E2S_JL/E2S-SRWopimiser/e2s_SRW/ANALYSIS/')

from fct_get_BLoptics  import DefineBLOptics
from BLGenerator  import BLGen
from SRW_intensity_BLasParam_I20withtwiss import CalcIntensity #JL:modified to calculate I20 with twiss parameters
from ana_intensity_new_BLasParam import GetSampleStruct

import numpy as np

## NOTE : In this version, we don't use the file e2s_BLOPTICS/fct_update_BLOPTIcs.py. Instead, we use a function within this file called update_BL. This works much better.







def GetLastFile(path):
    print('Now in the GetLastFile function...')
    list_of_files = glob.glob(path) 
    mostRecentFile = max(list_of_files, key=os.path.getctime) # FBT: check with your Operating System, in some OS, it's the mininimum instead of maximum
    print('here we are at the end of the GetLastFile function...')
    return mostRecentFile

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

# 6D:

def update_BL_I13(loelem,loval):
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
        if index < 2:
            item.L= loval[index]
        if index==2:
            item.p= loval[2]         
            item.q= loval[3]
        if index==3:
            item.p= loval[4]
            item.q= loval[5]
        if index==4:             #HERE and
            item.L= loval[6] #HERE

        new_oe=item
    print('end of the updating process. Quitting function...')


# this one here is to update I20: the indexation of elements will be different
def update_BL(loelem,loval):
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
        if index == 0:
            item.L= loval[0]

        if index==1:
            item.radSag= loval[1]         
        
        if index==2:
            item.L= loval[2]
 
        if index==3:             #HERE and
            item.q= loval[3] #HERE

        if index==4:             #HERE and
            item.L= loval[4] #HERE

        new_oe=item
    print('end of the updating process. Quitting function...')

 
    
    
testtt=0
if testtt==1:
    loelem= [oe0[0][13],oe0[0][15]]
    loval=[12,15]
    print('avant')
    print(oe0[0][13].L)
    print(oe0[0][15].L)
    oe0[0][13].L=oe0[0][13].L+.1
    oe0[0][15].L=oe0[0][15].L +.3
    print('apres:')
    print(oe0[0][13].L)
    print(oe0[0][15].L)


#optBL = SRWLOptC(oe0[0],oe0[1])

print('all okay')



def func_optBL(k13,k14,k15,k16,k17,bx,ax,by,ay,ex,exp, rootnumber):    # NOTE : ROOTNUMBER TAG HERE #HERE
    
    #print('FBT : Loading the beamline optBL_I13dMA.py through the function /e2s_BLOPTICS/fct_get_BLoptics.DefineBLOtics') 
    #print('(this message is from InGennoMain.py in func_optBL)')
    #print('FBT : beamline is I13d_MA (non-Test version) with 300x200 aperture...')

    print('JL:this is for I20 beamline optimisation')
    #for I13
    #optBL5,oe0 = DefineBLOptics('I13d_MA',800,800) # FBT: uncomment if you want I13
    #for I20
    optBL5,oe0 = DefineBLOptics('I20_scan',13574.4,2030.7) # Slitx et slity picked up from SRW.input 




    #print('FBT : using I13 here...')
    #optBL5,oe0 = DefineBLOptics('I13d_test',300,120)
    print('Bleamline I20-scan loaded...')
    #loelem= [oe0[0][9],oe0[0][11]] 2D from I13d_MA.py (without mono's)
    #loelem= [oe0[0][13],oe0[0][15],oe0[0][12],oe0[0][14],oe0[0][11]] # we list the drift first (13 and 15), then only the mirrors (12 and 14)... #6D I13d_test (with mono's)
    #loelem= [oe0[0][9],oe0[0][11],oe0[0][8],oe0[0][10],oe0[0][7]] # we list the drift first (9 and 11), then only the mirrors (8 and 10)... #6D I13d_MA (without mono's)
    loelem= [oe0[0][13],oe0[0][14],oe0[0][15],oe0[0][16],oe0[0][17]] #HERE is I20








    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    #print(' k9 vaut ', k13,'    et k11 vaut ',k15,' -- and k8.p is ', k12p,' k8.q is ', k12q,' -- k10p is ', k14p,' k10q is ',k14q,' and the pre-KB drift is ', k12)    #HERE
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    loval=[k13,k14,k15,k16,k17] #HERE

    print('Values before modification:')  # WITH MONO
    print(oe0[0][13].L)
    pprint(vars(oe0[0][14]))
    print(oe0[0][14].radSag)
    print(oe0[0][15].L)
    print(oe0[0][16].q)
    print(oe0[0][17].L)

    update_BL(loelem,loval)
    optBL = SRWLOptC(oe0[0],oe0[1])
    print('New Beamline created')
    print('Verification :values after modification:')
    print(oe0[0][13].L)
    print(oe0[0][14].radSag)
    print(oe0[0][15].L)
    print(oe0[0][16].q)
    print(oe0[0][17].L)


    #print('Values before modification:')   WITHOUT MONO
    #print(oe0[0][9].L)
    #print(oe0[0][11].L)
    #print(oe0[0][8].p)
    #print(oe0[0][8].q)
    #print(oe0[0][10].p)
    #print(oe0[0][10].q)  #HERE
    #print(oe0[0][7].L)
    #update_BL(loelem,loval)
    #optBL = SRWLOptC(oe0[0],oe0[1])
    #print('New Beamline created')
    #print('Verification :values after modification:')
    #print(oe0[0][9].L)
    #print(oe0[0][11].L)
    #print(oe0[0][8].p)
    #print(oe0[0][8].q)
    #print(oe0[0][10].p)
    #print(oe0[0][10].q)
    #print(oe0[0][7].L) #HERE
    

    print(' We are now going to calculate the intensity of the propagated wavefront. We will use the CalcIntensity function imported from SRW_intensity_BLasParam_I20withtwiss.py ')
    CalcIntensity(optBL,bx,ax,by,ay,ex,exp,'SRW.input',rootnumber) # NOTE : ROOTNUMBER TAG HERE
    #OutputFolder='/dls/physics/mfc33124/NSGA_E2S_01_backup_ok_2param_d13_d15_copy/e2s_SRW/SRW_I13d/multi-e__'+rootnumber+'*' #FBT: will not work if just the directory is given # NOTE : ROOTNUMBER TAG HERE
    OutputFolder='/E2S_JL/E2S-SRWopimiser/e2s_SRW/SRW_I20S/multi-e__'+rootnumber+'*' #FBT: will not work if just the directory is given # NOTE : ROOTNUMBER TAG HERE
    print('the new (rootname-tagged) file is:')
    lFile=GetLastFile(OutputFolder)
    print(lFile)
    print(' we just printed lfile... \n')
    
    
    Imax,sigx,sigy=GetSampleStruct(lFile)
    print('The structure of photons at sample is given by:')
    print('Imax vaut :', Imax)
    print('sigx vaut :', sigx)
    print('sigy vaut :', sigy)
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

    #return(-Imax,sigx)
    return(sigx,sigy)   


# =============================================================================
# haha=np.arange(1,3,0.26)
# print(haha)
# print(log_k13)
# print(log_k15)
# print(log_Imax)
# print(log_sigx)
# print(log_sigy)
# print(log_index)
# =============================================================================















