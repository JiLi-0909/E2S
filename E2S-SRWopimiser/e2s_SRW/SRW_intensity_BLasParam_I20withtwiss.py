# -*- coding: utf-8 -*-
#############################################################################
# SRWLIB Example#8: Simulating partially-coherent UR focusing with a CRL
# v 0.07
#############################################################################

from __future__ import print_function #Python 2.7 compatibility
import os
import sys

import datetime

# FBT Warning: the absolute path should be changed to  relative path in a future version, for better portability and decrease the chance of cloning failure
SRWLIB      = '/dls/physics/xph53246/source_to_beamline/SRWLIB/' # MA 12/03/2018 - repository created for pure SRWlib files 
sys.path.insert(0, SRWLIB)

e2s_Elegant_Lattices_Directory = '/E2S_JL/E2S-SRWopimiser/e2s_LATTICES/'
sys.path.insert(0, e2s_Elegant_Lattices_Directory)
e2s_Elegant_Scripts='/E2S_JL/E2S-SRWopimiser/e2s_ELEGANT/'
sys.path.insert(0, e2s_Elegant_Scripts)
from srwlib import *
from uti_plot import *

#sys.path.insert(0, '/dls/physics/xph53246/source_to_beamline/E2S/e2s_BLOPTICS')
sys.path.insert(0, '/E2S_JL/E2S-SRWopimiser/e2s_BLOPTICS/')
from fct_get_BLoptics  import DefineBLOptics
from fct_get_beam_param_from_twiss     import GetBeamParam
from fct_get_twiss_param_at_s_location import GetTwissList
from fct_get_rf_param                  import GetRF
from fct_get_SR_param                  import GetCirc
from fct_get_SR_param                  import DisplayCirc
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

def print_table():
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('!     ELEGANT (twiss file name)                       !!!!!!!!!!!!!!!           ELEGANT (Command bunched_beam)        !!!!!!!!!!    SRW.input          ')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('!ex0 ($gp$rm) =           2.704576e-09                [from *.twi  ]     /////  here:  emit_x here    [emittance]       ////         emi_x              ')
    print('!Sdelta0 =                9.59657e-04                [from *.twi  ]     /////  here:  sigma_dp here  [energy spread]   ////          dE                ')
    print('!Sz0 (calcule from RF)    sigma_z(0) : 0.003177228    [from *.fin??]     /////  here:  sigma_s        [bunch length]    ////         sig_z              ')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')




def Update_Accelerator_Optics(LATTICE, IDpos, bx,ax,by,ay,ex,exp, ex0,Sdelta0,Cou,Sz0,Circ):
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('%%%%%%%%%%%%                                                            %%%%%%%%%%%%%%%%%%%%%')
    print('%%%%%%%%%%%%  NOW STARTING THE ACCELERATOR OPTICS NEW PARAMETRIZATION   %%%%%%%%%%%%%%%%%%%%%')
    print('%%%%%%%%%%%%                                                            %%%%%%%%%%%%%%%%%%%%%')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('                                               ')
    print('                                               ')
    print('The targets optics variables are:')
    print('-----------------------------------------------')
    print(' beta-x       = '+str(bx))
    print(' alpha-x      = '+str(ax))
    print(' beta-y       = '+str(by))
    print(' alpha-y      = '+str(ay))
    print(' eta-x        = '+str(ex))
    print(' eta-x prime  = '+str(exp))
    print('                                               ')
    print('                                               ')
    print(' with the following baseline values :          ')
    print(' ex0          = '+str(ex0))
    print(' Sdelta0      = '+str(Sdelta0))
    print(' Cou          = '+str(Cou))
    print(' Sz0          = '+str(Sz0))
    print(' Circ          = '+str(Circ))

   
	
	
	
	
    eTWI   = LATTICE+'.twi'
    eRF    = LATTICE+'.rf'
    eMAG   = LATTICE+'.mag'
    

    # I reload the baseline config because ex0 and Sdelta0 are not in the SRW.input but are needed to call GetBeamParam
    os.chdir("/E2S_JL/E2S-SRWopimiser/e2s_LATTICES/")
    MickeyMouse=os.getcwd()
    print("we are now in:")
    print(MickeyMouse)
    
    # s,sIndex,betax,alphax,betay,alphay,etax,etaxp,ex0,Sdelta0 = GetTwissList(eTWI,IDpos)
    #print("VERIFICATION:")
    #print("s     : "+str(s))
    #print("betax : "+str(betax))
    #print("alphax : "+str(alphax))
    #print("betay : "+str(betay))
    #print("alphay : "+str(alphay))
    #print("eta_x : "+str(etax))
    #print("etax_p : "+str(etaxp))

    #Sz0  = GetRF(eRF)  
    #Circ = GetCirc(LATTICE)
    #cou  = 0.01
    os.chdir("/E2S_JL/E2S-SRWopimiser/e2s_SRW")
    MickeyMouse2=os.getcwd()
    print("\n\nwe have now returned to the directory:")
    print(MickeyMouse2)

    print("\n\nRecalculating the new beam parameters from the new accelerator optics...") 
    #Cou=0.1 #0.0507
    #print("FBT: We set the Coupling parameter Cou at 0.0507 \n(instead of 0.1 of the previous D-II versions) . You might want to check with \nthe fertical emittance. The Coupling is hardcoded at the root input \nfile used as argument for the original E2S.py script")
    beam, mom = GetBeamParam([bx,ax,by,ay,ex,exp,ex0,Sdelta0,Cou,Sz0])
    

    print("                                   ")
    print(" ***UPDATED*** Twiss parameters at that location:")
    print(" ------------------------------------------------")
    print(" betax     :", bx, " (m)")
    print(" alphax    :", ax)
    print(" betay     :", by, " (m)")
    print(" alphay    :", ay)
    print(" etax      :", ex, " (m)")
    print(" etaxp     :", exp)
    print(" ***UPDATED***  Beam/moments parameters :")
    print("-----------------------------------------")
    print(" sx        :", beam[0], " (m)")
    print(" sy        :", beam[1], " (m)")
    print(" sxp       :", beam[2], " (m)")
    print(" syp       :", beam[3], " (m)")
    print(" sigXX     :",mom[0])
    print(" sigXXp    :",mom[1])
    print(" sigXpXp   :",mom[2])
    print(" sigYY     :",mom[3])
    print(" sigYYp    :",mom[4])
    print(" sigYpYp   :",mom[5])


	

    
    print("                  ")
    print(" Global parameters at 3 GeV:")
    print(" ----------------------------")
   #print(" Eb         :", Ee, " (GeV)" )
   #print(" Ib         :", Ib, " (A)")
    print(" emix       :", ex0, " (m)")
    print(" dE/E       :", Sdelta0)
    print(" Circ       :", Circ, " (m)")
    print("                  ")
    print(" sigma_z(0) :", Sz0)
    
    print("                  ")
    #print(" ID:")
    #print(" ------------------")
    #print(" ID name       :", IDname)
    #print(" Np_und        :", Np_und)
    
    
  

  
	
	
	
	
	

    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('%%%%%%%%%%%%                                                            %%%%%%%%%%%%%%%%%%%%%')
    print('%%%%%%%%%%%%      NEW ACCELERATOR OPTICS PARAMETRIZATION COMPLETED      %%%%%%%%%%%%%%%%%%%%%')
    print('%%%%%%%%%%%%                                                            %%%%%%%%%%%%%%%%%%%%%')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    beamNew=beam
    momNew=mom	
    return beamNew,momNew






def CalcIntensity(currentOptBL,bx,ax,by,ay,ex,exp, SRWInputFile,rootnumber): #JL:modified to calculate with I20 beamline 

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
    
    #
    #***********Undulator
    By_und  = float(dict['By_und'])
    lam_und = float(dict['lam_und'])
    Np_und  = float(dict['Np_und'])
    K_und   = 0.9338 * By_und * lam_und * 100
    #***********Beam Parameters
    sig_x    = float(dict['sig_x'])   # 40e-6  # SIREPO TEST "God's eye @ 8088eV"
    sig_y    = float(dict['sig_y'])   # 40e-6 #
    sig_xp   = float(dict['sig_xp'])  # 0.1e-6 #
    sig_yp   = float(dict['sig_yp'])  # 0.1e-6 #
    sigXX    = float(dict['sigXX'])   # (40e-6)**2 #
    sigXXp   = float(dict['sigXXp'])  # 0 #
    sigXpXp  = float(dict['sigXpXp']) # (1e-7)**2 #
    sigYY    = float(dict['sigYY'])   # (40e-6)**2 #
    sigYYp   = float(dict['sigYYp'])  # 0 #
    sigYpYp  = float(dict['sigYpYp']) # (1e-7)**2 #
    Ee       = float(dict['Ee'])
    Ib       = float(dict['Ib'])
    sigEperE = float(dict['dE']) # 0.001 # 
    #*********** BeamLine Parameters
    slitZ   = float(dict['slitZ'])
    slitDX  = float(dict['slitDX'])
    slitDY  = float(dict['slitDY'])
    Ephot_ini = float(dict['Ephot_ini'])
    Ephot_end = float(dict['Ephot_end'])
    BLname    = dict['IDname']
    #********** Machine Parameters
    meshXsta  = float(dict['meshXsta'])
    meshXfin  = float(dict['meshXfin'])
    meshYsta  = float(dict['meshYsta'])
    meshYfin  = float(dict['meshYfin'])
    meshEsta  = float(dict['meshEsta'])
    meshEfin  = float(dict['meshEfin'])
    Nelectr   = float(dict['Nelectr'])
    calc_meth = int(dict['calc_meth'])
    Ncores    = float(dict['Ncores'])   # only meaningful for multi-e individual cluster calculations 
    outfil    = dict['outfil']
    lattice   = dict['LATTICE']
    #***********Extra Undulator Defs for Flux calculation
    harmB = SRWLMagFldH() #magnetic field harmonic 
    harmB.n = 1        # harmonic number
    harmB.h_or_v = 'v' # magnetic field plane: horzontal ('h') or vertical ('v')
    harmB.B = By_und   # 0.687566  #magnetic field amplitude [T]
    und = SRWLMagFldU([harmB])
    und.per = lam_und # 0.025 #period length [m]
    und.nPer = Np_und # number of periods (will be rounded to integer)
    magFldCnt = SRWLMagFldC([und], array('d', [0]), array('d', [0]), array('d', [0])) #Container of all magnetic field elements
    
    print('+ ----------------------------------------------------------- ')
    #print('| OUTPUT FILE: '+strExDataFolderName+'/'+strFluxOutFileName )
    print('+ ----------------------------------------------------------- ')
    print('| UNDULATOR PARAMETERS')
    print('| By (T)           = '+str(By_und))
    print('| lambda_u (m)     = '+str(lam_und))
    print('| Np_u             = '+str(Np_und))
    print('| K_max            = '+str(K_und))
    print('+ ----------------------------------------------------------- ')
    print('| BEAMLINE PARAMETERS')
    print('| Z_slit (m)       = '+str(slitZ))
    print('| DX (um)          = '+str(dict['slitDX']))
    print('| DY (um)          = '+str(dict['slitDY']))
    print('| Ephot_ini (eV)   = '+str(dict['Ephot_ini']))
    print('| Ephot_end (eV)   = '+str(dict['Ephot_end']))
    print('+ ----------------------------------------------------------- ')
    print('| BEAM PARAMETERS @ centre of undulator [FBT: BEFORE Accelerator Optics update]')
    print('| Ee       (GeV)   = '+str(Ee))
    print('| sigma_x  (um)    = '+str(sig_x*1e6))
    print('| sigma_xp (urad)  = '+str(sig_xp*1e6))
    print('| sigma_y  (um)    = '+str(sig_y*1e6))
    print('| sigma_yp (urad)  = '+str(sig_yp*1e6))
    print('| dp/p             = '+str(sigEperE))
    print('+ ----------------------------------------------------------- ')
    print('| MOMENTS @ centre of undulator [FBT: BEFORE Accelerator Optics update]')
    print('| sigXX     = '+str(sigXX))
    print('| sigXXp    = '+str(sigXXp))
    print('| sigXpXp   = '+str(sigXpXp))
    print('| sigYY     = '+str(sigYY))
    print('| sigYYp    = '+str(sigYYp))
    print('| sigYpYp   = '+str(sigYpYp))
    print('+ ----------------------------------------------------------- ')
    print('| MACHINE PARAMETERS')
    print('| Ib       (mA)   = '+str(Ib*1000))
    print('+ ----------------------------------------------------------- ')
    print('| COMPUTATION PARAMETERS')
    print('| Nelectr                   = '+str(Nelectr))
    print('| Ncores                    = '+str(Ncores))
    print('| mesh X start       (um)   = '+str(meshXsta))
    print('| mesh X fin         (um)   = '+str(meshXfin))
    print('| mesh Y start       (um)   = '+str(meshYsta))
    print('| mesh Y fin         (um)   = '+str(meshYfin))
    print('| mesh E start       (eV)   = '+str(meshEsta))
    print('| mesh E fin         (eV)   = '+str(meshEfin))
    print('| outfil                    = '+outfil)
    print('+ ----------------------------------------------------------- ')


    update_accelerator_optics=1
    if update_accelerator_optics==1:
	
        print('leaving the function CalcIntensity, entering in the function Update_Accelerator_Optics...')
	
        IDpos  = float(dict['IDpos']) # FBT: required to update the moments...

        ex0     = 2.704576e-09
        Sdelta0 =  0.000959657
        Cou     = 0.003
        Sz0     = 0.003177228
        Circ    = 561.571
        beamNew,momNew=Update_Accelerator_Optics(lattice, IDpos, bx,ax,by,ay,ex,exp, ex0,Sdelta0,Cou,Sz0,Circ)
        print('now back to the function CalcIntensity after having left Update_Accelerator_Optics...')
	
        sig_x    = beamNew[0]   # 40e-6  # SIREPO TEST "God's eye @ 8088eV"
        sig_y    = beamNew[1]   # 40e-6 #
        sig_xp   = beamNew[2]  # 0.1e-6 #
        sig_yp   = beamNew[3]  # 0.1e-6 #
        sigXX    = momNew[0]   # (40e-6)**2 #
        sigXXp   = momNew[1]  # 0 #
        sigXpXp  = momNew[2] # (1e-7)**2 #
        sigYY    = momNew[3]   # (40e-6)**2 #
        sigYYp   = momNew[4]  # 0 #
        sigYpYp  = momNew[5] # (1e-7)**2 #
        print("VERIFICATION POST-FUNCTION")
        print("sig_x    = "+str(sig_x))
        print("sig_y    = "+str(sig_y))
        print("sig_xp   = "+str(sig_xp))
        print("sig_yp   = "+str(sig_yp))
        print("sigXX   = "+str(sigXX))
        print("sigXXp  = "+str(sigXXp))
        print("sigXpXp = "+str(sigXpXp))
        print("sigYY   = "+str(sigYY))
        print("sigYYp  = "+str(sigYYp))
        print("sigYpYp = "+str(sigYpYp))




	
	
	
	
	
	
	
    
    #****************************Input Parameters:
    strExDataFolderName = outfil # 'data_example_08' #example data sub-folder name
    os.system('[ -d '+outfil+' ] && echo "output directory exists ..." || mkdir '+outfil)
    timestamp = "{:%Y-%b-%d_%H:%M:%S}".format(datetime.datetime.now())
    strIntOutFileName2 =  'single-e__'+outfil+'__'+lattice+'_'+timestamp+'.dat' 
    #the old 'ex08_res_int2.dat' #file name for output SR intensity data
    strIntOutFileName3 = 'multi-e__'+rootnumber+'-'+outfil+'__'+lattice+'_'+timestamp+'.dat' #FBT: added rootnumber
    #the old 'ex08_res_int3.dat' #file name for output SR intensity data
    
    #***********Undulator
    numPer = Np_und # 73 #Number of ID Periods (without counting for terminations
    undPer = lam_und # 0.033  # lam_und #Period Length [m]
    Bx = 0 #Peak Horizontal field [T]
    By = By_und # 0.3545 #Peak Vertical field [T]
    phBx = 0 #Initial Phase of the Horizontal field component
    phBy = 0 #Initial Phase of the Vertical field component
    sBx = 1 #Symmetry of the Horizontal field component vs Longitudinal position
    sBy = 1 #Symmetry of the Vertical field component vs Longitudinal position
    xcID = 0 #Transverse Coordinates of Undulator Center [m]
    ycID = 0
    zcID = 0 #-lam_und*Np_und/2-0.05 #-lam_und*Np_und/2*1.055 
    # Longitudinal Coordinate of Undulator Center wit hrespect to Straight Section Center [m]
    # my understanding: you need to calculate from a point outside the undulator
    # e.g. SIREPO fixes a -1.2705m offset for an undulator of 2.409m which 
    # hence: 2.409/2*1.055 = 1.2707
    
    und = SRWLMagFldU([SRWLMagFldH(1, 'v', By, phBy, sBy, 1), SRWLMagFldH(1, 'h', Bx, phBx, sBx, 1)], undPer, numPer) #Ellipsoidal Undulator
    magFldCnt = SRWLMagFldC([und], array('d', [xcID]), array('d', [ycID]), array('d', [zcID])) #Container of all Field Elements
    
    #***********Electron Beam
    elecBeam = SRWLPartBeam()
    elecBeam.Iavg = Ib # 0.1 #Average Current [A]
    elecBeam.partStatMom1.x = 0.00 #Initial Transverse Coordinates (initial Longitudinal Coordinate will be defined later on) [m]
    elecBeam.partStatMom1.y = 0.00
    elecBeam.partStatMom1.z = 0. #-0.5*undPer*(numPer + 4) #Initial Longitudinal Coordinate (set before the ID)
    elecBeam.partStatMom1.xp = 0 #Initial Relative Transverse Velocities
    elecBeam.partStatMom1.yp = 0
    elecBeam.partStatMom1.gamma = Ee/0.51099890221e-03 #Relative Energy
    #2nd order statistical moments
    elecBeam.arStatMom2[0]  = sigXX    # (sig_x)**2 # (5*118.027e-06)**2 #<(x-x0)^2> 
    elecBeam.arStatMom2[1]  = sigXXp
    elecBeam.arStatMom2[2]  = sigXpXp  # (sig_xp)**2 #(27.3666e-06)**2 #<(x'-x'0)^2>
    elecBeam.arStatMom2[3]  = sigYY    #(sig_y)**2  # (15.4091e-06)**2 #<(y-y0)^2>
    elecBeam.arStatMom2[4]  = sigYYp
    elecBeam.arStatMom2[5]  = sigYpYp  #(sig_yp)**2 # (2.90738e-06)**2 #<(y'-y'0)^2>
    elecBeam.arStatMom2[10] = (sigEperE)**2 #<(E-E0)^2>/E0^2
    
    #***********Precision Parameters for SR calculation
    meth    = calc_meth  # 1 #SR calculation method: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"
    relPrec = 0.01 #def = 0.01 relative precision
    zStartInteg = 0 #longitudinal position to start integration (effective if < zEndInteg)
    zEndInteg   = 0 #longitudinal position to finish integration (effective if > zStartInteg)
    npTraj  = 20000 #Number of points for trajectory calculation 
    useTermin   = 0 #1 #Use "terminating terms" (i.e. asymptotic expansions at zStartInteg and zEndInteg) or not (1 or 0 respectively)
    sampFactNxNyForProp = 0  # 0.25*2 #sampling factor for adjusting nx, ny (effective if > 0)
    arPrecPar = [meth, relPrec, zStartInteg, zEndInteg, npTraj, useTermin, 0]
    
    #***********Initial Wavefront data placeholder
    wfr2 = SRWLWfr() #For intensity distribution at fixed photon energy
    wfr2.allocate(1, 601, 601) # from Ji
    #wfr2.mesh.zStart = 36.25 + 1.25 #Longitudinal Position [m] from Center of Straight Section at which SR has to be calculated
    #wfr2.mesh.zStart = 12.9 + 1.25 #Longitudinal Position [m] from Center of Straight Section at which SR has to be calculated
    
    wfr2.mesh.zStart =  slitZ #Longitudinal Position [m] from Center of Straight Section at which SR has to be calculated
    wfr2.mesh.eStart =  meshEsta # 8830 # Initial Photon Energy [eV] <<< 1st harm peak for a 7GeV machine
    wfr2.mesh.eFin   =  meshEfin # 8830 # Final Photon Energy [eV]
    wfr2.mesh.xStart =  meshXsta/1e6  # meshXsta*1e-6 # -0.00025  # -0.0015 #Initial Horizontal Position [m]
    wfr2.mesh.xFin   =  meshXfin/1e6  # meshXfin*1e-6 #0.00025  # 0.0015 #Final Horizontal Position [m]
    wfr2.mesh.yStart =  meshYsta/1e6  # meshYsta*1e-6 #  # -0.0006 #Initial Vertical Position [m]
    wfr2.mesh.yFin   =  meshYfin/1e6  # meshYfin*1e-6 #0.00025  # 0.0006 #Final Vertical Position [m]
    wfr2.mesh.nx     =  600   #from Ji's low resolution calculation
    wfr2.mesh.ny     =  600
    meshInitPartCoh  = deepcopy(wfr2.mesh)
    wfr2.partBeam = elecBeam
    #
    # define the optical beamline 
    #
    print(' chosen beamline from SRW.input  is  : '+BLname)
    print(' here we are in SRW_intensity_BLasparam.py')
    #optBL = DefineBLOptics(BLname,slitDX,slitDY)
    testSRWInput=0
    if testSRWInput==1.1:
        
        print(' Performing a check that the beamline defined in SRW.input exists in fct_get_BLoptics...')
        optBL555 = DefineBLOptics(BLname,300,120)
    ### optBL = DefineBLOptics('I13d_ENTRY',slitDX,slitDY) # test 

    print('NOW LOADING THE MODIFIED BEAMLINE FOR INTENSITY CALCULATION')
    print('THAT IS optBL=currenntOptBL')
    optBL=currentOptBL
    
    #****************************Calculation (SRWLIB function calls)
    if(srwl_uti_proc_is_master()):
    
        print('1) Performing Initial Electric Field calculation ... =============================================', end='')
        arPrecPar[6] = sampFactNxNyForProp #sampling factor for adjusting nx, ny (effective if > 0)
        srwl.CalcElecFieldSR(wfr2, 0, magFldCnt, arPrecPar)
        print('done')
        print('2) Extracting Intensity from the Calculated Initial Electric Field ... ', end='')
        arI2 = array('f', [0]*wfr2.mesh.nx*wfr2.mesh.ny) #"flat" array to take 2D intensity data
        srwl.CalcIntFromElecField(arI2, wfr2, 6, 1, 3, wfr2.mesh.eStart, 0, 0)
        print('done')
        print('3) Saving the Initial Electric Field into a file ... ', end='')
        #AuxSaveIntData(arI2, wfr2.mesh, os.path.join(os.getcwd(), strExDataFolderName, strIntOutFileName2))
        #srwl_uti_save_intens_ascii(arI2, wfr2.mesh, os.path.join(os.getcwd(), strExDataFolderName, strIntOutFileName2), 0)
        srwl_uti_save_intens_ascii(arI2, wfr2.mesh, os.path.join(os.getcwd(), strExDataFolderName, strIntOutFileName2), 0)#JL:double source test
        print('  done')
    
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





 
