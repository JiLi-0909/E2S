



"""

fct_update_BLoptics
Created on 03 oct 2018

@author: FBT

description: generates a BL of a known family, with a new set of parameters    
"""

import os
import sys
import subprocess
import interpol

SRWLIB      = '/dls/physics/xph53246/source_to_beamline/SRWLIB/' # MA 12/03/2018 - repository created for pure SRWlib files 
sys.path.insert(0, SRWLIB)
from srwlib import *
from uti_plot import *

sys.path.insert(0, '/dls/physics/mfc33124/SRW_DLS_06/E2S/e2s_BLOPTICS/')
from fct_get_BLoptics  import DefineBLOptics
from BLGenerator  import BLGen

import numpy as np




"""
 print('FBT: example of access: oe_pp[0][15].L for the last drift')

 [0][0] SRWLOptA 
 [0][1] SRWLOptD       :L
 [0][2] SRWLOptT 
 [0][3] SRWLOptD       :L
 [0][4] SRWLOptMirPl 
 [0][5] SRWLOptD       :L 
 [0][6] SRWLOptCryst 
 [0][7] SRWLOptCryst 
 [0][8] SRWLOptD       :L 
 [0][9] SRWLOptCryst 
 [0][10] SRWLOptCryst 
 [0][11] SRWLOptD       :L 
 [0][12] SRWLOptMirEl 
 [0][13] SRWLOptD       :L 
 [0][14] SRWLOptMirEl 
 [0][15] SRWLOptD       :L 
"""


#def BLGen(loelem,loval):   # loelem: list of optical elements (that will be updated),loval:list of (new) optical values


    #*********** we load the BL

print('FBT : using I13 here...')
optBL5,oe0 = DefineBLOptics('I13d_test',300,120)
print('Bleamline loaded')

    #****************************Calculation (SRWLIB function calls)
print('fini...')
loelem= [oe0[0][13],oe0[0][15]]
loval=[12,15]
print('avant')
print(oe0[0][13].L)
print(oe0[0][15].L)
oe0[0][13].L=oe0[0][13].L+1
oe0[0][15].L=oe0[0][15].L +3
print('apres:')
print(oe0[0][13].L)
print(oe0[0][15].L)


optBL = SRWLOptC(oe0[0],oe0[1])

print('all okay')


for index, item in enumerate(loelem, start = 0):
    print index, item
    print loval[index]
    item.L=loval[index]*2
    print item.L







