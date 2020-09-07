# -*- coding: utf-8 -*-
#############################################################################
# SRWLIB Example#8: Simulating partially-coherent UR focusing with a CRL
# v 0.07
#############################################################################

from __future__ import print_function #Python 2.7 compatibility

import os
import sys
#import numpy as np
import datetime

###SRWLIB      = '/dls/physics/xph53246/source_to_beamline/SRW_Dev/env/work/SRW_PROJECT/MyBeamline/'
SRWLIB      = '/dls/physics/xph53246/source_to_beamline/SRWLIB/' # MA 12/03/2018 - repository created for pure SRWlib files 

sys.path.insert(0, SRWLIB)
from srwlib import *
from uti_plot import * 

sys.path.insert(0, '/dls/physics/xph53246/source_to_beamline/E2S/e2s_BLOPTICS')
from fct_get_BLoptics  import DefineBLOptics


print('SRWLIB Python Example # 8:')
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
print('')

INPUT_file = sys.argv[1]
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
sig_x   = float(dict['sig_x'])
sig_y   = float(dict['sig_y'])
sig_xp  = float(dict['sig_xp'])
sig_yp  = float(dict['sig_yp'])
sigXX    = float(dict['sigXX'])   # (40e-6)**2 #
sigXXp   = float(dict['sigXXp'])  # 0 #
sigXpXp  = float(dict['sigXpXp']) # (1e-7)**2 #
sigYY    = float(dict['sigYY'])   # (40e-6)**2 #
sigYYp   = float(dict['sigYYp'])  # 0 #
sigYpYp  = float(dict['sigYpYp']) # (1e-7)**2 #
Ee      = float(dict['Ee'])
Ib      = float(dict['Ib'])
sigEperE = float(dict['dE']) 
#***********BeamLine Parameters
slitZ   = float(dict['slitZ'])
slitDX  = float(dict['slitDX'])
slitDY  = float(dict['slitDY'])
Ephot_ini = float(dict['Ephot_ini'])
Ephot_end = float(dict['Ephot_end'])
BLname    = dict['IDname']
#**********Machine Parameters
meshXsta  = float(dict['meshXsta'])
meshXfin  = float(dict['meshXfin'])
meshYsta  = float(dict['meshYsta'])
meshYfin  = float(dict['meshYfin'])
meshEsta  = float(dict['meshEsta'])
meshEfin  = float(dict['meshEfin'])
meshnx    = int(dict['meshnx'])
meshny    = int(dict['meshny'])
sampfact  = float(dict['sampfact'])
Nelectr   = int(dict['Nelectr'])
calc_meth = int(dict['calc_meth'])
Ncores    = int(dict['Ncores'])   # only meaningful for multi-e individual cluster calculations 
outfil    = dict['outfil']
lattice   = dict['LATTICE']
#***********Extra Undulator Defs for Flux calculation
#harmB = SRWLMagFldH() #magnetic field harmonic 
#harmB.n = 1        # harmonic number
#harmB.h_or_v = 'v' # magnetic field plane: horzontal ('h') or vertical ('v')
#harmB.B = By_und   # 0.687566  #magnetic field amplitude [T]
#und = SRWLMagFldU([harmB])
#und.per = lam_und # 0.025 #period length [m]
#und.nPer = Np_und # number of periods (will be rounded to integer)
#magFldCnt = SRWLMagFldC([und], array('d', [0]), array('d', [0]), array('d', [0])) #Container of all magnetic field elements

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
print('| BEAM PARAMETERS @ centre of undulator')
print('| Ee       (GeV)   = '+str(Ee))
print('| sigma_x  (um)    = '+str(sig_x*1e6))
print('| sigma_xp (urad)  = '+str(sig_xp*1e6))
print('| sigma_y  (um)    = '+str(sig_y*1e6))
print('| sigma_yp (urad)  = '+str(sig_yp*1e6))
print('| dp/p             = '+str(sigEperE))
print('+ ----------------------------------------------------------- ')
print('| MOMENTS @ centre of undulator')
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
print('| mesh nx                   = '+str(meshnx))
print('| mesh ny                   = '+str(meshny))
print('| outfil                    = '+outfil)
print('+ ----------------------------------------------------------- ')

#****************************Input Parameters:
strExDataFolderName = outfil # 'data_example_08' #example data sub-folder name
os.system('[ -d '+outfil+' ] && echo "output directory exists ..." || mkdir '+outfil)
timestamp = "{:%Y-%b-%d_%H:%M:%S}".format(datetime.datetime.now())

strIntOutFileNamePartCoh = 'individual-e__'+outfil+'__'+lattice+'_'+timestamp+'.dat' 
strOpTrFileName = 'ex08_res_op_tr_crl.dat' #file name for output optical transmission data
strOpPathDifFileName = 'ex08_res_op_path_dif_crl.dat' #file name for optical path difference data

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
zcID =  -lam_und*Np_und/2-0.05 #-lam_und*Np_und/2*1.055
#Longitudinal Coordinate of Undulator Center wit hrespect to Straight Section Center [m]
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
meth = calc_meth #SR calculation method: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"
relPrec = 0.01 #relative precision
zStartInteg = 0 #longitudinal position to start integration (effective if < zEndInteg)
zEndInteg   = 0 #longitudinal position to finish integration (effective if > zStartInteg)
npTraj  = 20000 #Number of points for trajectory calculation 
useTermin   = 0 #1 #Use "terminating terms" (i.e. asymptotic expansions at zStartInteg and zEndInteg) or not (1 or 0 respectively)
sampFactNxNyForProp = sampfact # 0.25*2 #sampling factor for adjusting nx, ny (effective if > 0)
arPrecPar = [meth, relPrec, zStartInteg, zEndInteg, npTraj, useTermin, 0]

#***********Initial Wavefront data placeholder
nE = 1
wfr2 = SRWLWfr() #For intensity distribution at fixed photon energy
#wfr2.allocate(1, 101, 101) #Numbers of points vs Photon Energy, Horizontal and Vertical Positions
wfr2.allocate(nE, meshnx+1, meshny+1) #Numbers of points vs Photon Energy, Horizontal and Vertical Positions
#wfr2.mesh.zStart = 36.25 + 1.25 #Longitudinal Position [m] from Center of Straight Section at which SR has to be calculated
#wfr2.mesh.zStart = 12.9 + 1.25 #Longitudinal Position [m] from Center of Straight Section at which SR has to be calculated

wfr2.mesh.zStart =  slitZ #Longitudinal Position [m] from Center of Straight Section at which SR has to be calculated
wfr2.mesh.eStart =  meshEsta # 8830 # Initial Photon Energy [eV] <<< 1st harm peak for a 7GeV machine
wfr2.mesh.eFin   =  meshEfin # 8830 # Final Photon Energy [eV]
wfr2.mesh.xStart =  meshXsta/1e6  # meshXsta*1e-6 # -0.00025  # -0.0015 #Initial Horizontal Position [m]
wfr2.mesh.xFin   =  meshXfin/1e6  # meshXfin*1e-6 #0.00025  # 0.0015 #Final Horizontal Position [m]
wfr2.mesh.yStart =  meshYsta/1e6  # meshYsta*1e-6 #  # -0.0006 #Initial Vertical Position [m]
wfr2.mesh.yFin   =  meshYfin/1e6  # meshYfin*1e-6 #0.00025  # 0.0006 #Final Vertical Position [m]
meshInitPartCoh  = deepcopy(wfr2.mesh)
wfr2.partBeam = elecBeam

#
# define the optical beamline 
#
optBL = DefineBLOptics(BLname,slitDX,slitDY)

#optApert = SRWLOptA('r', 'a', 0.1e-3, 0.2e-3) #Aperture
#optDrift = SRWLOptD(2.0) #Drift space
#propagParApert = [0, 0, 1., 0, 0, 1.5, 1.0, 1.1, 6., 0, 0, 0]
#propagParDrift = [0, 0, 1., 1, 0, 1.0, 1.2, 1.0, 1., 0, 0, 0]

#optBL = SRWLOptC([optApert, optDrift], [propagParApert, propagParDrift])

print('Simulating Partially-Coherent Wavefront Propagation by summing-up contributions of SR from individual electrons (takes time)... ')
#nMacroElec = 50000 #total number of macro-electrons
nMacroElec = Nelectr ### 30 [TESTING secondo me era errore]
#total number of macro-electrons: (old mpiexec was 13m for 50e on 50cores)
# using openmpi as suggested by M.Furseman
# 50  cores  3min for 50e / 5:41(4:50) for 100e / 11:05 for 200                 50.5.10
# 100 cores                                     / 11:03 for 200 (the same?)    100.5.10 
# 100 cores                       4:40 for 100e / 08:55                       100.10.10
nMacroElecAvgPerProc = 5 # 5 #number of macro-electrons / wavefront to average on worker processes before sending data to master (for parallel calculation only)
nMacroElecSavePer = 5 # 5 intermediate data saving periodicity (in macro-electrons)
srCalcMeth = 1 #SR calculation method
srCalcPrec = 0.01 #SR calculation rel. accuracy
# ORIGINAL WORKING ON RH6: radStokesProp = srwl_wfr_emit_prop_multi_e(elecBeam, magFldCnt, meshInitPartCoh, srCalcMeth, srCalcPrec, nMacroElec, nMacroElecAvgPerProc, nMacroElecSavePer, os.path.join(os.getcwd(), strExDataFolderName, strIntOutFileNamePartCoh), sampFactNxNyForProp, optBL) # ,0,0,0.,0.,0,1,False)
radStokesProp = srwl_wfr_emit_prop_multi_e(elecBeam, magFldCnt, meshInitPartCoh, srCalcMeth, srCalcPrec, nMacroElec, nMacroElecAvgPerProc, nMacroElecSavePer, os.path.join(os.getcwd(), strExDataFolderName, strIntOutFileNamePartCoh), sampFactNxNyForProp, optBL, 0, 0, 0., 0., 0, 1, True)


print('done')
print('GRID MESH NX = ',meshInitPartCoh.nx,' NY= ',meshInitPartCoh.ny )
#plotMeshX = [1000*meshInitPartCoh.xStart, 1000*meshInitPartCoh.xFin, meshInitPartCoh.nx]
#plotMeshY = [1000*meshInitPartCoh.yStart, 1000*meshInitPartCoh.yFin, meshInitPartCoh.ny]
#uti_plot2d(radStokesProp.arS, plotMeshX, plotMeshY, ['Horizontal Position [mm]', 'Vertical Position [mm]', 'Power Density'])


#uti_plot_show() #show all graphs (blocks script execution; close all graph windows to proceed)
print('done')

 