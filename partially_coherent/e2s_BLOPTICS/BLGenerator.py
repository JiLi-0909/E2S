"""
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

import numpy as np


def BLGen(loelem,loval):   # loelem: list of optical elements,loval:list of (new) optical values


    #*********** we load the BL

    print('FBT : using I13 here...')
    optBL5 = DefineBLOptics('I13d_test',300,120)
    print('Bleamline loaded')

    #****************************Calculation (SRWLIB function calls)









