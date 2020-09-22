#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu 16 Aug 2018

@author: MA

description: external file describing a BL    
"""

import os
import sys
import subprocess
import numpy as np
import interpol

SRWLIB      = '/dls/physics/xph53246/source_to_beamline/SRWLIB/' # MA 12/03/2018 - repository created for pure SRWlib files 

sys.path.insert(0, SRWLIB)
from srwlib import *
from uti_plot import *




def read_input(filin):
    INPUT_file = filin # e.g. 'E2S.input'
    infile     = open(INPUT_file,'r')


    variables =[]; values=[];
    for line in infile:
        variable, value = line.split('=')
        variable = variable.strip()  # remove leading/traling blanks
        value    = value.strip()
        variables.append(variable)
        values.append(value)

    infile.close()

    dict={}              # create a dictionary for easy access to variables 
 
    for i in range(0,len(variables)) :
        dict[variables[i]] = values[i]

    dict['INPUT_file'] = INPUT_file
    return dict


dict = read_input('SRW.input')

delta_x = float(dict['delta_x'])
delta_xp = float(dict['delta_xp'])

print('--------------------------------------delta_x=',delta_x)

def optBL(slitDX, slitDY, Ephot):

    print "+ ------------------------------------- + "
    print "| this is Beam Line I13d - coherence      "
    print "| rev. 16/8/2018,  M. Apollonio DLS       " 
    print "+ ------------------------------------- + "

    verba = 0
    # --------
    # lens
    # --------
    Fx = 21.573
    Fy = 21.573
    print('lens focal length = '+str(Fx)) 
    optlen = SRWLOptL(Fx,Fy)

    # --------
    # CRL lens
    # -------- CASE E = 11209 eV
    delta        = 2.711695e-6   #    @11.209keV (SIREPO)
    attenLen     = 12545e-6      #[m] @11.209keV (SIREPO) 
    geomApertH   = 2.0E-03       #[m] Geometrical aperture of 1D CRL in the H plane
    geomApertV   = 2.0E-03       #[m] Geometrical aperture of 1D CRL in the 
    
    rMin         = 351.0e-6
    nCRL         = 3
    wallThick    = 50E-06 #[m] wall thickness of CRL
    
    xc           = 0#-200e-6
    yc           = 0 
    ftheo        = rMin / 2 / delta / nCRL 
    print('theoretical CRL focal length = '+str(ftheo))       
    optCRL = srwl_opt_setup_CRL(3, delta, attenLen, 1, geomApertH, geomApertV, rMin, nCRL, wallThick, xc, yc)
    
    
    # -----------------------------------------
    # Si(111) Crystal Parameters: fn of energy!
    # -----------------------------------------
    if Ephot>0:
        print " MONO - Si111 crystal parameters set for Ephot = {}".format(Ephot)
        crpar       = interpol.CrPar(Ephot/1e3, 'Si111')           # Faissal's function (note: Ephot eV --> keV, unit used in Si111.csv)
        dSpSi111    = 3.1355713563754857                           # Crystal reflecting planes d-spacing for Si(111) crystal
        psi0rSi111  = crpar[0]; psi0iSi111 = crpar[1]              # Real and imaginary parts of 0-th Fourier component of crystal polarizability
        psihrSi111  = crpar[2]; psihiSi111 = crpar[3]              # Real and imaginary parts of h-th Fourier component of crystal polarizability
        psihbrSi111 = psihrSi111; psihbiSi111 = psihiSi111         # Real and imaginary parts of -h-th Fourier component of crystal polarizability
        thickCryst  = 10.e-03                                      # Thickness of each crystal [m]
        angAsCryst  = 0                                            # Asymmetry angle of each crystal [rad]
    else: 
        Ephot =np.abs(Ephot) # if Ephot < 0 use fixed params 
        dSpSi111    = 3.1355713563754857                             # Crystal reflecting planes d-spacing for Si(111) crystal
        psi0rSi111  = -7.757245827e-6; psi0iSi111 = 9.506848329e-8   # Real and imaginary parts of 0-th Fourier component of crystal polarizability
        psihrSi111  = -4.095903022e-6; psihiSi111 = 6.637430983e-8   # Real and imaginary parts of h-th Fourier component of crystal polarizability
        psihbrSi111 = psihrSi111; psihbiSi111 = psihiSi111           # Real and imaginary parts of -h-th Fourier component of crystal polarizability
        thickCryst  = 10.e-03                                        # Thickness of each crystal [m]
        angAsCryst  = 0                                              # Asymmetry angle of each crystal [rad]
        
        
    dE_error =  0.0 # energy error on the mono
    dthet = delta_x/21.573#delta_xp#
    #bragg_Ang = 0.177331266836
    verba_new = 6 #JL: choose 66 to add modification of crystals  
    print('JL: source tilt angle check-------,dthet =',dthet)        
    # 
    # MA: 15/1/2019, pi/2 pi+pi/2 pi/2 pi+pi/2 was corrected to   pi/2 pi+pi/2  pi+pi/2 pi/2
    #                in line with the sequence sx, dx, dx, sx 
    #
    # -----------------------------------------------------
    # monoC1 - 1st crystal of the I13(coh) monochromator -- for reference PI = 3.1415926535897932384626433832795 
    # -----------------------------------------------------
    optCr_1 = SRWLOptCryst(_d_sp=dSpSi111, _psi0r=psi0rSi111,
                          _psi0i=psi0iSi111, _psi_hr=psihrSi111, _psi_hi=psihiSi111, _psi_hbr=psihbrSi111, 
                          _psi_hbi=psihbiSi111,_tc=thickCryst, _ang_as=angAsCryst)
    ang_dif_pl = np.pi/2
    #defG_1 = dthet#+bragg_Ang
    #Find appropriate orientation of the 1st crystal and the corresponding output beam frame (in the incident beam frame):
    orientDataCr1 = optCr_1.find_orient(Ephot+dE_error, ang_dif_pl) # (GsnBm.avgPhotEn) # ,0): deflect in the v-plane (default) (GsnBm.avgPhotEn,pi/2): deflect in the h-plane 
    orientCr1 = orientDataCr1[0] #1st crystal orientation
    tCr1 = orientCr1[0]; nCr1 = orientCr1[2] # Tangential and Normal vectors to crystal surface
    verba=1
    if verba == 1:
        print('   1st crystal orientation:'); 
        print('   t=', tCr1, 's=', orientCr1[1], 'n=', nCr1)


    #Set crystal orientation:
    #-----------JL: dthet is used to modify the bragg angle-------------
    if verba_new == 66:
   	bragg_Ang = acos(-nCr1[0]/sin(ang_dif_pl))
    	nCr1[0]= -cos(dthet+bragg_Ang)
    	nCr1[1]= 0
    	nCr1[2]= -sin(dthet+bragg_Ang)
    	tCr1[0]= -sin(dthet+bragg_Ang)
    	tCr1[2]= cos(dthet+bragg_Ang)
        #print('@@@@@@@@@@@@bra=',bragg_Ang)
        print('   1st crystal new orientation:'); 
        print('   t=', tCr1, 's=', orientCr1[1], 'n=', nCr1)
    optCr_1.set_orient(nCr1[0], nCr1[1], nCr1[2], tCr1[0], tCr1[1])
    orientOutFrCr1 = orientDataCr1[1] #Orientation (coordinates of base vectors) of the output beam frame 
    rxCr1 = orientOutFrCr1[0]; ryCr1 = orientOutFrCr1[1]; rzCr1 = orientOutFrCr1[2] #Horizontal, Vertical and Longitudinal base vectors of the output beam frame
    if verba == 11:
        print('   1st crystal output beam frame:'); print('   ex=', rxCr1, 'ey=', ryCr1, 'ez=', rzCr1)
    TrM = [rxCr1, ryCr1, rzCr1] #Input/Output beam transformation matrix (for debugging)
    if verba == 1:
        uti_math.matr_print(TrM)
        print('   Beam frame transformation matrix (from the begining of opt. scheme to output of current element):')
        
    
    # -----------------------------------------------------
    # monoC2 - 2nd crystal of the I13(coh) monochromator
    # -----------------------------------------------------
    optCr_2 = SRWLOptCryst(_d_sp=dSpSi111, _psi0r=psi0rSi111,
                           _psi0i=psi0iSi111, _psi_hr=psihrSi111, _psi_hi=psihiSi111, _psi_hbr=psihbrSi111, _psi_hbi=psihbiSi111,_tc=thickCryst, _ang_as=angAsCryst)
    #Find appropriate orientation of the 2nd crystal and the corresponding output beam frame (in the incident beam frame):
    ang_dif_pl = np.pi + np.pi/2
    defG_2 =  dthet#+bragg_Ang
    orientDataCr2 = optCr_2.find_orient(Ephot+dE_error, ang_dif_pl) # (GsnBm.avgPhotEn) 
    orientCr2 = orientDataCr2[0] #2nd crystal orientation
    tCr2 = orientCr2[0]; nCr2 = orientCr2[2] # Tangential and Normal vectors to crystal surface
    verba=2
    if verba == 2:
        print('   2nd crystal orientation:'); print('   t=', tCr2, 's=', orientCr2[1], 'n=', nCr2)
    #Set crystal orientation:
    if verba_new == 66:
    	bragg_Ang = acos(-nCr2[0]/sin(ang_dif_pl))
    	nCr2[0]= cos(dthet+bragg_Ang)
    	nCr2[1]= 0
    	nCr2[2]= -sin(dthet+bragg_Ang)
    	tCr2[0]= sin(dthet+bragg_Ang)
    	tCr2[2]= cos(dthet+bragg_Ang)
        #print('@@@@@@@@@@@@bra=',bragg_Ang)
        print('   2nd crystal new orientation:'); print('   t=', tCr2, 's=', orientCr2[1], 'n=', nCr2)

    optCr_2.set_orient(nCr2[0], nCr2[1], nCr2[2], tCr2[0], tCr2[1])
    orientOutFrCr2 = orientDataCr2[1] #Orientation (coordinates of base vectors) of the output beam frame 
    rxCr2 = orientOutFrCr2[0]; ryCr2 = orientOutFrCr2[1]; rzCr2 = orientOutFrCr2[2] #Horizontal, Vertical and Longitudinal base vectors of the output beam frame
    if verba == 22:
        print('   2nd crystal output beam frame:'); print('   ex=', rxCr2, 'ey=', ryCr2, 'ez=', rzCr2)
    TrM = uti_math.matr_prod(TrM, [rxCr2, ryCr2, rzCr2]) #Input/Output beam transformation matrix (for debugging)
    verba=1
    if verba == 1:
        print('   Beam frame transformation matrix (from the begining of opt. scheme to output of current element):')
        uti_math.matr_print(TrM)
        print('   After the two crystals of DCM, the transformation matrix should be close to the unit matrix.')
    
    # -----------------------------------------------------
    # monoC3 - 3rd crystal of the I13(coh) monochromator
    # -----------------------------------------------------
    optCr_3 = SRWLOptCryst(_d_sp=dSpSi111, _psi0r=psi0rSi111,
                           _psi0i=psi0iSi111, _psi_hr=psihrSi111, _psi_hi=psihiSi111, _psi_hbr=psihbrSi111, _psi_hbi=psihbiSi111,_tc=thickCryst, _ang_as=angAsCryst)
    ang_dif_pl = np.pi + np.pi/2
    ##defG_3 = ang_dif_pl+dthet+bragg_Ang
    #Find appropriate orientation of the 3rd crystal and the corresponding output beam frame (in the incident beam frame):
    orientDataCr3 = optCr_3.find_orient(Ephot+dE_error, ang_dif_pl) # (GsnBm.avgPhotEn) 
    orientCr3 = orientDataCr3[0] #3rd crystal orientation
    tCr3 = orientCr3[0]; nCr3 = orientCr3[2] # Tangential and Normal vectors to crystal surface
    verba=3
    if verba == 3:
        print('   3rd crystal orientation:'); print('   t=', tCr3, 's=', orientCr3[1], 'n=', nCr3)
    #Set crystal orientation:
    if verba_new == 66:
    	bragg_Ang = acos(-nCr3[0]/sin(ang_dif_pl))
    	nCr3[0]= cos(dthet+bragg_Ang)
    	nCr3[1]= 0
    	nCr3[2]= -sin(dthet+bragg_Ang)
    	tCr3[0]= sin(dthet+bragg_Ang)
    	tCr3[2]= cos(dthet+bragg_Ang)
        #print('@@@@@@@@@@@@bra=',bragg_Ang)
        print('   3rd crystal new orientation:'); print('   t=', tCr3, 's=', orientCr3[1], 'n=', nCr3)

    optCr_3.set_orient(nCr3[0], nCr3[1], nCr3[2], tCr3[0], tCr3[1])
    orientOutFrCr3 = orientDataCr3[1] #Orientation (coordinates of base vectors) of the output beam frame 
    rxCr3 = orientOutFrCr3[0]; ryCr3 = orientOutFrCr3[1]; rzCr3 = orientOutFrCr3[2] #Horizontal, Vertical and Longitudinal base vectors of the output beam frame
    if verba == 33:
        print('   3rd crystal output beam frame:'); print('   ex=', rxCr3, 'ey=', ryCr3, 'ez=', rzCr3)
    TrM = uti_math.matr_prod(TrM, [rxCr3, ryCr3, rzCr3]) #Input/Output beam transformation matrix (for debugging)
    if verba == 1:
        print('   Beam frame transformation matrix (from the begining of opt. scheme to output of current element):')
        uti_math.matr_print(TrM)
    
    # -----------------------------------------------------
    # monoC4 - 4th crystal of the I13(coh) monochromator
    # -----------------------------------------------------
    optCr_4 = SRWLOptCryst(_d_sp=dSpSi111, _psi0r=psi0rSi111,
                           _psi0i=psi0iSi111, _psi_hr=psihrSi111, _psi_hi=psihiSi111, _psi_hbr=psihbrSi111, _psi_hbi=psihbiSi111,_tc=thickCryst, _ang_as=angAsCryst)
    ang_dif_pl = np.pi/2
    ##defG_4 = ang_dif_pl+dthet+bragg_Ang
    #Find appropriate orientation of the 4th crystal and the corresponding output beam frame (in the incident beam frame):
    orientDataCr4 = optCr_4.find_orient(Ephot+dE_error, ang_dif_pl) # (GsnBm.avgPhotEn) 
    orientCr4 = orientDataCr4[0] #4th crystal orientation
    tCr4 = orientCr4[0]; nCr4 = orientCr4[2] # Tangential and Normal vectors to crystal surface
    verba=4
    if verba == 4:
        print('   4th crystal orientation:'); print('   t=', tCr4, 's=', orientCr4[1], 'n=', nCr4)
    #Set crystal orientation:
    if verba_new == 66:
    	bragg_Ang = acos(-nCr4[0]/sin(ang_dif_pl))
    	nCr4[0]= -cos(dthet+bragg_Ang)
    	nCr4[1]= 0
    	nCr4[2]= -sin(dthet+bragg_Ang)
    	tCr4[0]= -sin(dthet+bragg_Ang)
    	tCr4[2]= cos(dthet+bragg_Ang)
        #print('@@@@@@@@@@@@bra=',bragg_Ang)
        print('   4th crystal new orientation:'); print('   t=', tCr4, 's=', orientCr4[1], 'n=', nCr4)

    optCr_4.set_orient(nCr4[0], nCr4[1], nCr4[2], tCr4[0], tCr4[1])
    orientOutFrCr4 = orientDataCr4[1] #Orientation (coordinates of base vectors) of the output beam frame 
    rxCr4 = orientOutFrCr4[0]; ryCr4 = orientOutFrCr4[1]; rzCr4 = orientOutFrCr4[2] #Horizontal, Vertical and Longitudinal base vectors of the output beam frame
    if verba == 44:
        print('   4th crystal output beam frame:'); print('   ex=', rxCr4, 'ey=', ryCr4, 'ez=', rzCr4)
    TrM = uti_math.matr_prod(TrM, [rxCr4, ryCr4, rzCr4]) #Input/Output beam transformation matrix (for debugging)
    verba=1
    if verba == 1:
        print('   Beam frame transformation matrix (from the begining of opt. scheme to output of current element):')
        uti_math.matr_print(TrM)
        print('   After the two crystals of DCM, the transformation matrix should be close to the unit matrix.')
    
    # -----------------------------------------------------
    # M1 - planar mirror deflecting in the Horizontal Plane
    # -----------------------------------------------------
    tG, sG  = 3, 3  
    grazG   = 3e-3  # 10mrad  
    optM_1  = SRWLOptMirPl(_size_tang=tG, _size_sag=sG, _ap_shape='r',
                           _nvx=cos(grazG), _nvy=0, _nvz=-sin(grazG), _tvx=sin(grazG), _tvy= 0)
    
    # --------------------------------------------------------
    # KB1 - elliptical mirror deflecting in the Vertical Plane
    # --------------------------------------------------------
    tG, sG  = 3, 3 
    grazG   = 3e-3 # 1. * np.pi / 180 
    optKB_1   = SRWLOptMirEl(_p=30.9, _q=9.1, _ang_graz=grazG, _r_sag=1.e+23,
                             _size_tang=3, _size_sag=3,
                             _nvx=0, _nvy=cos(grazG), _nvz=-sin(grazG), _tvx=0, _tvy=sin(grazG))
    
    # ----------------------------------------------------------
    # KB2 - elliptical mirror deflecting in the Horizontal Plane
    # ----------------------------------------------------------
    tG, sG  = 3, 3
    grazG   = 3e-3 # 1. * np.pi / 180; 
    optKB_2   = SRWLOptMirEl(_p=33.1, _q=6.9, _ang_graz=grazG, _r_sag=1.e+23,
                             _size_tang=3, _size_sag=3,
                             _nvx=cos(grazG), _nvy=0, _nvz=-sin(grazG), _tvx=sin(grazG), _tvy= 0)
    
    # ------
    # Drifts
    # ------
    
    D1            = 9.999
    optDrift_1    = SRWLOptD(D1)                              # 10m - 1mm drift 
    D2            = 4.7                                       # 4.7m drift
    optDrift_2    = SRWLOptD(D2)
    D3            = 182.4#25.75#77.751#     # an offset of DX=60um @ source --> DX = 190um just before cryst-1
    optDrift_3    = SRWLOptD(D3)                              # 182.5m drift from CRL (position of mono) 
    #D31           = 2.649 # 33.75+40 #23.75+10-28.45 # 194.05  # 16.3                                      # short drift for tests 
    #optDrift_31    = SRWLOptD(D31)                              # 182.5m drift from CRL (position of mono) 
    
    D4            = 1
    optDrift_4    = SRWLOptD(D4)
    dD5           = 0.65       # correction to KB1 ... 
    D5            = 10#+dD5
    optDrift_5    = SRWLOptD(D5)
    DKB           = 2.2#-dD5
    optDrift_KB   = SRWLOptD(DKB)
    DKBSam        = 6.9-.8     #  .1:46/40   0:42/38   -.1: 38/36   -.2:34/34     -.3:30/32 
                               # -.4:26/30 -.5:22/29   -.6:19/27    -.7:15/25     -.8:11/23 
                               # -.9:8/22  -1.:5.2/21 -1.1:4.9/19  -1.2:7.3/17.3 -1.3:10.6/16.6
                               # -1.4:   -2: 14.3/16.7 
                               # -0.8m selected, brute figures: sx=11um/sy=23.6um, however the central spot is ~10.5um/11.2um 
    optDrift_KB_Sam   = SRWLOptD(DKBSam)
    
    
    # ----------------------
    # Propagation Parameters 
    # ----------------------
#                      arb ara rpa  l/q  FFTr   hra   hres  vra   vres  
#    propagParApert =  [  0,  0,  1.,  0,    0, 1.04,  1.1,  1.04, 1.1,  0, 0, 0]   # BEST SO FAR (BSF)
#    propagParLens  =  [  0,  0,  1.,  0,    0, 1.04,  1.1,  1.04, 1.0,  0, 0, 0]
#    propagParDrift =  [  0,  0,  1.,  1,    0, 1.04,  1.1,  1.04, 1.1,  0, 0, 0]
#    propagParPM    =  [  0,  0,  1.,  1,    0, 1.04,  1.1,  1.04, 1.1,  0, 0, 0]
#    propagParCryst =  [  0,  0,  1.,  1,    0, 1.04,  1.1,  1.04, 1.0,  0, 0, 0]
#    propagParKB    =  [  0,  0,  1.,  0,    0, 1.04,  1.1,  1.04, 1.0,  0, 0, 0]


#    CASE-0              arb ara  rpa  l/q  FFTr   hra   hres  vra   vres  
    propagParApert =  [  0,  0,  1.,  0,    0,   1.0,  1.0,  1.0,  1.0,  0, 0, 0]
    propagParLens  =  [  0,  0,  1.,  0,    0,   1.0,  1.0,  1.0,  1.0,  0, 0, 0]
    propagParDrift =  [  0,  0,  1.,  1,    0,   1.0,  1.0,  1.0,  1.0,  0, 0, 0]
#    propagParPM    =  [  0,  0,  1.,  0,    0,   1.0,  1.0,  1.0,  1.0,  0, 0, 0]
#    propagParPM    =  [  1,  0,  1.,  0,    0,   1.0,  1.0,  1.0,  1.0,  0, 0, 0] # arb = 1 corrects the dx flip seen in SIREPO/E2S
    propagParPM    =  [  0,  0,  1.,  0,    0,   1.0,  1.0,  1.0,  1.0,  0, 0, 0] # arb = 1 corrects the dx flip seen in SIREPO/E2S
    propagParCryst_1 =  [  0,  0,  1.,  0,    0,   1.0,  1.0,  1.0,  1.0,  0, 0, 0]#,sin(defG_1),0, cos(defG_1), 1, 0
    propagParCryst_2 =  [  0,  0,  1.,  0,    0,   1.0,  1.0,  1.0,  1.0,  0, 0, 0]#,sin(defG_2),0, cos(defG_2), 1, 0
               #pG     = [  0,  0,  1.,  1,    0,   1.0,  1.0,  1.0,  1.0,  0, 0, 0,   0 ,sin(defG), cos(defG), 1, 0 ]
    propagParKB    =  [  0,  0,  1.,  0,    0,   1.0,  1.0,  1.0,  1.0,  0, 0, 0]
    postProp       =  [  0,  0,  1.,  0,    0,   1.0,  1.0,  1.0,  1.0,  0, 0, 0]

    

#                      arb ara rpa  l/q  FFTr   hra   hres  vra   vres  
    #propagParDrift1 = propagParDrift
    #propagParDrift2 = [  0,  0,  1.,  1,    0,   1.0,  1,  1.0,  1.0,  0, 0, 0]
    #propagParDrift3 = [  0,  0,  1.,  1,    0,   1.,  1,  1.0,  1.0,  0, 0, 0]
    #propagParDrift4 = propagParDrift
    #propagParDrift5 = [  0,  0,  1.,  1,    0,   1.0,  1.0,  1.0,  1.0,  0, 0, 0]
    #propagParDriftKB = [  0,  0,  1.,  1,    0,   1.0,  1.0,  1.0,  1.0,  0, 0, 0]
    #propagParDriftKBS = [  0,  0,  1.,  1,    0,   1 , 1.0,  1,  1.0,  0, 0, 0]

    propagParDrift1 = propagParDrift
    propagParDrift2 = [  0,  0,  1.,  1,    0,   1.08,  1,  1.0,  1.0,  0, 0, 0]
    propagParDrift3 = [  0,  0,  1.,  1,    0,   3.1,  1,  1.08,  1.0,  0, 0, 0]
    #propagParDrift31 = [  0,  0,  1.,  1,    0,   1.5,  1,  1.08,  1.0,  0, 0, 0]
    propagParDrift4 = propagParDrift
    propagParDrift5 = [  0,  0,  1.,  1,    0,   1.08,  1.0,  1.08,  1.0,  0, 0, 0]
    propagParDriftKB = [  0,  0,  1.,  1,    0,   1.1,  1.0,  1.0,  1.0,  0, 0, 0]
    propagParDriftKBS = [  0,  0,  1.,  1,    0,   0.7,  1.0,  1.08,  1.0,  0, 0, 0]

    propagParKB1    = propagParKB
    propagParKB2    = propagParKB

    #propagParDrift3 =  [  0,  0,  1.,  1,    0,   3.5,  1.,  1.0,  1.0,  0, 0, 0]
    #propagParDrift31 = [  0,  0,  1.,  1,    0,   3.1,  1.,  1.0,  1.0,  0, 0, 0]
    #propagParDrift6 = [  0,  0,  1.,  1,    0, 3.7,  1.,  1.7, 1.0,  0, 0, 0]
    #propagParCryst =  [  0,  0,  1.,  0,    0,   1.,  1.,  1.0,  1.0,  0, 0, 0]

    # 0/1 to inhibit/activate the element 
    
    D_1     = 1
    CRL     = 1    # def 1
    Lens    = 0
    D_2     = 1
    M1      = 1    # def 1

    D_3     = 1
    #slit2   = 0 
    #D_31    = 0   # def 0: add one slit before mono  
    MONOA   = 1  # def 1 first two crystals of the mono
    MONOB   = 1      
    D_4     = 1
    MONOC   = 1  # def 1second two crystals of the mono
    MONOD   = 1 
    D_5     = 1
    KB1     = 1    # def 1
    D_KB    = 1
    KB2     = 1    # def 1
    D_KBSam = 1

    # --------------------------------------------------------------------------
    # Lists of Optical Elements (oe) and Propagation Parameters (pp) are defined
    # --------------------------------------------------------------------------
    
    s = []  # position along the line from the entry aperture

    oe=[]; pp=[] 
    bl = []
    #bl.append("  -||-  ")                                                             
    ## the optical elements
    #oe.append( SRWLOptA('r', 'a', slitDX*1e-6, slitDY*1e-6) )                             
    ## oe(1):  aperture
    #pp.append(propagParApert)
    #s.append(0)

    if D_1 == 1:
        bl.append( "  ---  " )
        oe.append( optDrift_1 )                                                                    
    # oe(2):  drift
        pp.append(propagParDrift1)
        s.append(oe[-1].L)

    if  Lens == 1:
        bl.append(" () ")
        oe.append( optlen )                                                                            
    # oe(3):  CRL       
        pp.append(propagParLens)
        s.append(0)
    
    if CRL == 1:
        bl.append(" ()()() ")
        oe.append( optCRL )                                                                            
    # oe(3):  CRL       
        pp.append(propagParLens)
        s.append(0)

    if D_2 == 1:
        bl.append("  ---  ")
        oe.append( optDrift_2 )                                                                   
    # oe(4):  drift
        pp.append(propagParDrift2)
        s.append(oe[-1].L)

    if M1 == 1:
        bl.append("  -/-  ")
        oe.append( optM_1 )                                                                              
    # oe(5):  plane mirror
        pp.append(propagParPM)
        s.append(0)
        
      

    if D_3 == 1:
        bl.append("  ---  ")
        oe.append( optDrift_3 )                                                          
    # oe(6):  drift
        pp.append(propagParDrift3)
        s.append(oe[-1].L)
 

    #if slit2 ==1:
    	#bl.append("  -||-  ")                                                             
    	#oe.append( SRWLOptA('r', 'a', 2*1e-3, 2*1e-3,-2.48896*2.e-3,0 ) )  #2.673474*1e-3,0                           
    	#pp.append(propagParApert)
    	#s.append(0)

    #if D_31 == 1:
    #    bl.append("  ---  ")
    #    oe.append( optDrift_31 )                                                          
    #    pp.append(propagParDrift31)
    #    s.append(oe[-1].L)   

      
    if MONOA == 1:
    
        bl.append("  -#  ")
        oe.append( optCr_1 )                                                            
    # oe(7):  mono-element1
        pp.append(propagParCryst_1)
        s.append(0)

    if MONOB == 1:
        
        bl.append("  #-  ")
        oe.append( optCr_2 )                                                                                                             # oe(8):  mono-element2
        pp.append(propagParCryst_2)
        s.append(0)
        
    if D_4 == 1:
        bl.append("  ---  ")
        oe.append( optDrift_4 )                                                                                                          # oe(9):  drift
        pp.append(propagParDrift4)
        s.append(oe[-1].L)
        
    if MONOC == 1:
        bl.append("  -#  ")
        oe.append( optCr_3 )                                                                                                             # oe(10): mono-element3
        pp.append(propagParCryst_2)
        s.append(0)

    if MONOD == 1:
        
        bl.append("  #-  ")
        oe.append( optCr_4 )                                                                                                             # oe(11): mono-element4
        pp.append(propagParCryst_1)
        s.append(0)
        
    if D_5 == 1:
        bl.append("  ---  ")
        oe.append( optDrift_5 )                                                                                                          # oe(12): drift
        pp.append(propagParDrift5)
        s.append(oe[-1].L)
        
    if KB1 == 1:   
        bl.append( "  -)-  ")    
        oe.append( optKB_1 )                                                                                                             # oe(13): KB1 
        pp.append(propagParKB1)
        s.append(0)
        
    if D_KB == 1:
        bl.append("  ---  ")
        oe.append( optDrift_KB )                                                                                                         # oe(14): drift KB 
        pp.append(propagParDriftKB)
        s.append(oe[-1].L)
        
    if KB2 == 1:
        bl.append("  -(-  ")
        oe.append( optKB_2 )                                                                                                             # oe(15): KB2 
        pp.append(propagParKB2)
        s.append(0)
        
    if D_KBSam == 1:
        bl.append("  ---  ")
        oe.append( optDrift_KB_Sam )                                                                                                     # oe(16): drift KB-sample  
        pp.append(propagParDriftKBS)
        s.append(oe[-1].L)
        
    bl.append("  --|S  ")
    pp.append(postProp)

    bl = ''.join(bl)
    print "{}".format(bl)
    cs = np.cumsum(s)
#    print("  ".join(str(int(np.ceil(x))) for x in cs))
    print("  ".join(str(round(x+11.55,4)) for x in cs))

    oe_pp =[]; oe_pp.append(oe); oe_pp.append(pp)
        
    return oe_pp

