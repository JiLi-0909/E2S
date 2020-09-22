




from __future__ import print_function #Python 2.7 compatibility
import os
import sys

import datetime
import pickle


SRWLIB      = '/dls/physics/xph53246/source_to_beamline/SRWLIB/' # MA 12/03/2018 - repository created for pure SRWlib files 
sys.path.insert(0, SRWLIB)
from srwlib import *
from uti_plot import *

#sys.path.insert(0, '/dls/physics/xph53246/source_to_beamline/E2S/e2s_BLOPTICS')
#sys.path.insert(0, '/dls/physics/mfc33124/SRW_DLS_06/E2S/e2s_BLOPTICS/')
sys.path.insert(0, '/dls/physics/students/sug89938/E2S/e2s_BLOPTICS')
from fct_get_BLoptics  import DefineBLOptics
import numpy as np3



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


from SRW_intensity_BLasParam import CalcIntensity

optBL5,oe0 = DefineBLOptics('I20_scan',13574.4,2030.7)
print("\n\n-------------------------------------------------")

print(oe0[0][13].L)
print(oe0[0][14].radSag)
print(oe0[0][15].L)
print(oe0[0][16].q)
print(oe0[0][17].L)
print("-------------------------------------------------\n\n")


test_Beamline=1

if test_Beamline==1:
    loelem= [oe0[0][13],oe0[0][14],oe0[0][15],oe0[0][16],oe0[0][17]] #HERE is I20
    print("\n\nJL reminder: the baseline values are : loval=[2.7, 0.087435897, 4.5, 23, 19.5]\n\n") #HERE
    loval=[2.7, 0.087435897, 4.5, 23, 19.5] #HERE 
    update_BL(loelem,loval)
    optBL = SRWLOptC(oe0[0],oe0[1])
    print('New Beamline created')
    print('Verification :values after modification:')
    print(oe0[0][13].L)
    print(oe0[0][14].radSag)
    print(oe0[0][15].L)
    print(oe0[0][16].q)
    print(oe0[0][17].L)





rootnumber=str(2019)
CalcIntensity(optBL5,'SRW.input',rootnumber)
