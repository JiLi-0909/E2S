# -*- coding: utf-8 -*-
#############################################################################
# SRWLIB Example#8: Simulating partially-coherent UR focusing with a CRL
# v 0.07
#############################################################################

from __future__ import print_function #Python 2.7 compatibility
import os
import sys
import pickle
import datetime


SRWLIB      = '/dls/physics/xph53246/source_to_beamline/SRWLIB/' # MA 12/03/2018 - repository created for pure SRWlib files 
sys.path.insert(0, SRWLIB)
from srwlib import *
from uti_plot import *

#sys.path.insert(0, '/dls/physics/xph53246/source_to_beamline/E2S/e2s_BLOPTICS')
#sys.path.insert(0, '/dls/physics/mfc33124/SRW_DLS_06/E2S/e2s_BLOPTICS/')
sys.path.insert(0, '/E2S_JL/E2S-SRWopimiser/e2s_BLOPTICS')
from fct_get_BLoptics  import DefineBLOptics
import numpy as np3



print(' We are now in the file e2s_SRW/SRW_intensity_BLasParam.py, where you can find the function def CalcIntensity.')
print('This SRWLIB Python code is inspired from a modification of Example # 8:------------------------------------------------------------------------------------------------------------------------------')
print('Simulating emission and propagation of undulator radiation (UR) wavefront through a simple optical scheme including CRL')
print('')
print('First, single-electron UR (on-axis spectrum and a wavefront at a fixed photon energy) is calculated and propagated through the optical scheme. ', end='')
print('After this, calculation of partially-coherent UR from entire electron beam is started as a loop over "macro-electrons", using "srwl_wfr_emit_prop_multi_e" function. ', end='')
print('This function can run either in "normal" sequential mode, or in parallel mode under "mpi4py".', end='')
print('For this, an MPI2 package and the "mpi4py" Python package have to be installed and configured, and this example has to be started e.g. as:')
print('    mpiexec -n 5 python SRWLIB_Example08.py')
print('For more information on parallel calculations under "mpi4py" please see documentation to the "mpi4py" and MPI.')
print('Note that the long-lasting partially-coherent UR calculation saves from time to time instant average intensity to an ASCII file, ', end='')
print('so the execution of the long loop over "macro-electrons" can be aborted after some time without the danger that all results will be lost.')
print('---------------------------------------------------------------------------------------------------------------------------------------------------------')

def CalcIntensity(currentOptBL,SRWInputFile):

    INPUT_file = SRWInputFile #sys.argv[1]
    infile = open(INPUT_file, 'r')
    
    variables =[]; values=[];
    for line in infile:
        # Typical line: variable = value
        variable, value = line.split('=')
        variable = variable.strip()  # remove leading/traling blanks
        value    = value.strip()
        variables.append(variable)
        values.append(value)
    
    infile.close()
    
    dict={}              # create a dictionary for easy access to variables 
     
    for i in range(0,len(variables)) :
        dict[variables[i]] = values[i]
    

    #*********** BeamLine Parameters
    BLname    = dict['IDname']
    #********** Machine Parameters
    outfil    = dict['outfil']
    lattice   = dict['LATTICE']

    
    print('+ ----------------------------------------------------------- ')
    print('| outfil                    = '+outfil)
    print('+ ----------------------------------------------------------- ')
    
    #****************************Input Parameters:
    strExDataFolderName = outfil # 'data_example_08' #example data sub-folder name
    os.system('[ -d '+outfil+' ] && echo "output directory exists ..." || mkdir '+outfil)
    timestamp = "{:%Y-%b-%d_%H:%M:%S}".format(datetime.datetime.now())
    strIntOutFileName2 =  'single-e__'+outfil+'__'+lattice+'_'+timestamp+'.dat' 
    #the old 'ex08_res_int2.dat' #file name for output SR intensity data
    strIntOutFileName3 = 'multi-e__'+outfil+'__'+lattice+'_'+timestamp+'.dat' #FBT: added rootnumber
    #the old 'ex08_res_int3.dat' #file name for output SR intensity data
    

    #
    # define the optical beamline 
    #
    print(' chosen beamline from SRW.input  is  : '+BLname)
    print(' here we are in SRW_intensity_BLasparam.py')
    #optBL = DefineBLOptics(BLname,slitDX,slitDY)
    testSRWInput=0
    if testSRWInput==1.1:
        
        print(' Performing a check that the beamline defined in SRW.input exists in fct_get_BLoptics...')
        optBL555 = DefineBLOptics('I20_scan',13574.4,2030.7)
    ### optBL = DefineBLOptics('I13d_ENTRY',slitDX,slitDY) # test 

    print('NOW LOADING THE MODIFIED BEAMLINE FOR INTENSITY CALCULATION')
    optBL=currentOptBL
    print('THAT IS optBL:',currentOptBL)
   
    
    #****************************Calculation (SRWLIB function calls)
    if(srwl_uti_proc_is_master()):
   
        
        print('------JL: now it is going to extract wavefront from existing file------')

        def load_variable(filename):
            f=open(filename,'rb')
            wfr2=pickle.load(f)
            f.close()
            return wfr2
        
        wfr2 = load_variable('/dls/physics/students/sug89938/wfrnew.txt') #600x600
    
        print('4) Simulating Electric Field Wavefront Propagation ... ', end='')
        print(' FBT: the beamline is :')
        print(optBL)
        srwl.PropagElecField(wfr2,optBL)
        print(' 4) is now done')
        print('Extracting Intensity from the Propagated Electric Field  ... ', end='')
        arI3 = array('f', [0]*wfr2.mesh.nx*wfr2.mesh.ny) #"flat" 2D array to take intensity data
        # srwl.CalcIntFromElecField(arI3, wfr2, 6, 0, 3, wfr2.mesh.eStart, 0, 0)
        srwl.CalcIntFromElecField(arI3, wfr2, 6, 1, 3, wfr2.mesh.eStart, 0, 0)  # FBT 0 instead of 1
        print('  done')
        print('Saving the Propagated Wavefront Intensity data to a file ... ', strIntOutFileName3, end='')
        #AuxSaveIntData(arI3, wfr2.mesh, os.path.join(os.getcwd(), strExDataFolderName, strIntOutFileName3))
        srwl_uti_save_intens_ascii(arI3, wfr2.mesh, os.path.join(os.getcwd(), strExDataFolderName, strIntOutFileName3), 0)
        print('  done')
    
        test_numpy_FBT=0
        if test_numpy_FBT==1:
            print(' testing numpy, from SRW_intensity...')
            data = []
            for i in range(10):
                data.append(i)
        
            data = np3.array(data) # re-assign data after the loop
            print(data)





 
