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

#sys.path.insert(0, '/dls/physics/xph53246/source_to_beamline/E2S/e2s_BLOPTICS')
sys.path.insert(0, '/dls/physics/mfc33124/SRW_lab_OPT_DESIGN/MultiElectrons/e2s_BLOPTICS')

from fct_get_BLoptics  import DefineBLOptics


e2s_Elegant_Lattices_Directory = '/dls/physics/mfc33124/NSGA_E2S_01_backup_ok_2param_d13_d15_copy/e2s_LATTICES/'
sys.path.insert(0, e2s_Elegant_Lattices_Directory)
e2s_Elegant_Scripts='/dls/physics/mfc33124/NSGA_E2S_01_backup_ok_2param_d13_d15_copy/e2s_ELEGANT/'
sys.path.insert(0, e2s_Elegant_Scripts)
from srwlib import *
from uti_plot import *



from fct_get_beam_param_from_twiss     import GetBeamParam
from fct_get_twiss_param_at_s_location import GetTwissList
from fct_get_rf_param                  import GetRF
from fct_get_SR_param                  import GetCirc
from fct_get_SR_param                  import DisplayCirc
import numpy as np3


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
    print(" Global parameters at 3.5 GeV:")
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






def update_BL(loelem,loval):
# update_BL: create the new beamline
# loelem: list of optical elements (that will be updated)
# loval:list of (new) optical values
# No need to return anything, as the Beamline is transformed directly in this function

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

 
    
    



#optBL = SRWLOptC(oe0[0],oe0[1])

print('all okay')




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




update_accelerator_optics=1
if update_accelerator_optics==1:

	print('\n\n\n... entering in the function Update_Accelerator_Optics...')

	IDpos  = float(dict['IDpos']) # FBT: required to update the moments...
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(IDpos)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

	ex0     = float(dict['emi_x']) # previous: 1.155943e-10
	Sdelta0 = 6.649372e-04
	Cou     = 0.0507
	print('\n\n FBT : present coupling is set at 0.0507 - ATTENTION: if you change coupling,nyou must re-create a new SRW.input from the original E2S.py, i.e.  python E2S.py M-H6BA-14-1-1__I13d__SRW__source_shift.input \n\n')
	Sz0     = 0.001834378
	Circ    = 560.5704

	bx  = float(dict['beta_x'])
	ax  = float(dict['alpha_x'])
	by  = float(dict['beta_y'])
	ay  = float(dict['alpha_y'])
	ex  = float(dict['eta_x'])
	exp  = float(dict['eta_xp'])
        print("The baseline twiss parameters as read from SW.input are:")

        print("beta_x   : "+str(bx))
        print("alpha_x  : "+str(ax))
        print("beta_y   : "+str(by))
        print("alpha_y  : "+str(ay))
        print("eta_x    : "+str(ex))
        print("eta_xp   : "+str(exp))

        "FBT : BEACON - change twiss parameters here. Default are baseline values imported from SRW.input"
        [bx,ax,by,ay,ex,exp]=[bx,ax,by,ay,ex,exp]   
        [bx,ax,by,ay,ex,exp]=[8.842959,-0.2401737,5.319206,-0.4559996,3.162498e-09,3.653917e-16]#iniitial configuration
        [bx,ax,by,ay,ex,exp]=[8.24,-0.32,4.48,-0.36,0,0]#spoiled machine start
        [bx,ax,by,ay,ex,exp]=[9.8,-0.14,4.33,-0.36,0,0]#Twiss +BL end
        [bx,ax,by,ay,ex,exp]=[9.84,-0.14,4.30,-0.36,0,0]#spoiled machine end
        #-------------JL:midstraight beta optimisation result------------------------------------
        [bx,ax,by,ay,ex,exp]=[9.44791715888,-0.223114808177,5.0080469871,-0.501999403918,2.34597529474e-09,2.62496976189e-16]#twiss+BL,mid straight beta
        [bx,ax,by,ay,ex,exp]=[8.20176458183 ,-0.261578567933,6.01040450141,-0.383129517107,2.235727958e-09,2.83079625505e-16]#spoiled machine start,mid straight beta(try to run again with
        [bx,ax,by,ay,ex,exp]=[9.4448137584,-0.223195805442,5.00956264152,-0.501745279197,3.57446235585e-09,4.43689430526e-16]#spoiled machine end,mid straight beta




        Ji_Li_run=1
        if Ji_Li_run==1:
            [bx,ax,by,ay,ex,exp]=[9.4448137584,-0.223195805442,5.00956264152,-0.501745279197,3.57446235585e-09,4.43689430526e-16]

	beamNew,momNew=Update_Accelerator_Optics(lattice, IDpos, bx,ax,by,ay,ex,exp, ex0,Sdelta0,Cou,Sz0,Circ)
	print('\n\n...leaving the function left Update_Accelerator_Optics...')

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
################################################################################################optBL = DefineBLOptics(BLname,slitDX,slitDY)

optBL,oe0= DefineBLOptics('I13d_MA',800,800) # DefineBLOptics(BLname,2000,2000)
modify_beamline_with_mono=1
if modify_beamline_with_mono==1:
    loelem= [oe0[0][13],oe0[0][15],oe0[0][12],oe0[0][14],oe0[0][11]] # we list the drift first (9 and 11), then only the mirrors (8 and 10), then the ... #67 I13d_MA (with mono's) #HERE
    print('Values before modification:')  # WITH MONO
    print(oe0[0][13].L)
    print(oe0[0][15].L)
    print(oe0[0][12].p)
    print(oe0[0][12].q)
    print(oe0[0][14].p)
    print(oe0[0][14].q)  #HERE
    print(oe0[0][11].L)
    loval=[1.832582200286327, 6.289053559465659, 32.96614226771016, 10.563645243164029, 31.138241778555596, 7.818449617757608, 11.743278330287339]
    loval=[2.5208565114068406, 6.266457356448184, 31.271888421938566, 9.656129529326552, 32.40890852546115, 5.635012727808084, 10.609068300476318] # nsgaTest-007689
    loval=[2.5,5.7,32.8,11.32,32.98,6.71,12.77]
    loval=[2.534891443902258, 5.720047964538113, 32.80676130510688, 11.321701524434722, 32.984045863201544, 6.713463412078196, 12.771371548459268]
    loval=[2.5135157231176364, 5.720047964538113, 32.78477213047352, 11.321701524434722, 32.98404626209617, 6.713462497028317, 12.771371548459268]
    loval=[2.52450307371509, 6.1290917827782705, 32.81668677493878, 11.449787128345164, 32.984178589193064, 6.630792989276333, 12.771371548459268]
    loval=[2.5109758878780633, 6.004306002403229, 32.80367391585471, 11.565113851333258, 32.98352027244184, 6.720177541661552, 9.48965425562991]
    loval=[2.093942106615108, 5.586181271300679, 32.83948814330534, 11.654761807772585, 32.98404586522193, 6.713159639405772, 12.740889697239373]
    loval=[1.3037815894018434, 6.60635893855974, 31.68781742861342, 8.852103752840408, 30.920327628035274, 8.555584497644016, 12.857217454524404]
    loval=[2.8500032679278045, 5.004575531193836, 32.16425595149648, 10.53166639660344, 29.779991144454243, 5.876143915066686, 12.997855622809583]
    loval=[2.93091153716485, 5.004579538364016, 34.03878248740752, 10.636923976511639, 29.779820494380285, 5.876145656672525, 12.92555647306711] # front 400
    loval=[3.1559862293273273, 5.014980794491615, 33.959115643937274, 10.882134620169621, 30.141655523920267, 5.876153719571002, 12.09043197451079] # front 100
    loval=[3.156957671798139, 5.036054734746594, 33.127577418785414, 11.30395318512786, 29.782670452948885, 5.876149837102485, 12.077485253936604]
    #-------------JL:tiwss+BL optimisation result------------------------------------
    loval=[2.2, 5.5, 30.9, 9.1, 33.1, 6.9, 10]#initial configuration
    loval=[1.33, 5.00, 30.65, 7.93, 32.50, 5.74, 11.09]#best of BL optimisation
    loval=[3.71, 6.36, 32.2, 9.0, 31.6, 5.78, 12]#spoiled machine start
    loval=[1.46, 5.02, 30.7, 8.1, 29.3, 5.89, 12.9]#BL+twiss end
    loval=[1.00, 5.54, 32.0, 8.1, 29.9, 6.59, 12.9]#spoiled machine end
    #-------------JL:midstraight beta optimisation result------------------------------------
    loval=[1.24429103926, 5.41485803068, 29.3753006447, 8.5638077031, 31.6854436119, 6.33062082866, 12.9996600007]#twiss+BL,mid straight beta
    loval=[1.62353231107, 6.17425100939, 29.0533824923, 6.05716221705, 31.0004503282, 10.5273621125, 11.8739976911 ]#spoiled machine start,mid straight beta
    loval=[1.37714764477, 5.57642458713, 30.6243483504, 8.94674172969, 32.8636975392, 6.5032657802, 12.9753536011]#spoiled machine end,mid straight beta


    Ji_Li_run=1
    if Ji_Li_run==1:
        loval=[2.2, 5.5, 30.9, 9.1, 33.1, 6.9, 10]
    update_BL(loelem,loval)
    optBL = SRWLOptC(oe0[0],oe0[1])
    print('New Beamline created')
    print('Verification :values after modification:')
    print(oe0[0][13].L)
    print(oe0[0][15].L)
    print(oe0[0][12].p)
    print(oe0[0][12].q)
    print(oe0[0][14].p)
    print(oe0[0][14].q)  #HERE
    print(oe0[0][11].L)



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

 
