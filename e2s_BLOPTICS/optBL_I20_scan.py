# -----------------------------------------
# JI created for I20 scanning branch
# add spherical mirror calculation
#-----------------------------------------

import os
import sys
import subprocess
import interpol

 # MA 12/03/2018 - repository created for pure SRWlib files 

SRWLIB      = '/dls/physics/xph53246/source_to_beamline/SRWLIB/'
sys.path.insert(0, SRWLIB)
from srwlib import *
from uti_plot import *
import numpy as np



Par_new1 = 2.788397789493215
Par_new2 = 0.050825039364912554
Par_new3 = 5.6606364476521955
Par_new4 = 21.670910223639105
Par_new5 = 19.94204210249081




def optBL(slitDX, slitDY, Ephot):

    print "+ ------------------------------------- + "
    print "| this is Beam Line I20 Scanning branch      "
    print "+ ------------------------------------- + "

    verba = 0

    # --------
    # lens
    # --------
    Fx = 8.5
    Fy = 8.5
    print('lens focal length = '+str(Fx)) 
    optlen = SRWLOptL(Fx,Fy)
    
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
        dSpSi111 = 3.1355713563754857                             # Crystal reflecting planes d-spacing for Si(111) crystal
        psi0rSi111 = -7.757245827e-6; psi0iSi111 = 9.506848329e-8 # Real and imaginary parts of 0-th Fourier component of crystal polarizability
        psihrSi111 = -4.095903022e-6; psihiSi111 = 6.637430983e-8 # Real and imaginary parts of h-th Fourier component of crystal polarizability
        psihbrSi111 = psihrSi111; psihbiSi111 = psihiSi111        # Real and imaginary parts of -h-th Fourier component of crystal polarizability
        thickCryst = 10.e-03                                      # Thickness of each crystal [m]
        angAsCryst = 0                                            # Asymmetry angle of each crystal [rad]
        
        
    dE_error =  0.0 # energy error on the mono
        
    # -----------------------------------------------------
    # monoC1 - 1st crystal of the I20 monochromator -- for reference PI = 3.1415926535897932384626433832795 
    # -----------------------------------------------------
    optCr_1 = SRWLOptCryst(_d_sp=dSpSi111, _psi0r=psi0rSi111,
                           _psi0i=psi0iSi111, _psi_hr=psihrSi111, _psi_hi=psihiSi111, _psi_hbr=psihbrSi111, 
                           _psi_hbi=psihbiSi111,_tc=thickCryst, _ang_as=angAsCryst)
    #Find appropriate orientation of the 1st crystal and the corresponding output beam frame (in the incident beam frame):
    orientDataCr1 = optCr_1.find_orient(Ephot+dE_error, np.pi+34.906585e-3 ) # (GsnBm.avgPhotEn) # ,0): deflect in the v-plane (default) / 3.1415926535897932384626433832795/2): deflect in the h-plane 
    orientCr1 = orientDataCr1[0] #1st crystal orientation
    tCr1 = orientCr1[0]; nCr1 = orientCr1[2] # Tangential and Normal vectors to crystal surface
    if verba == 1:
        print('   1st crystal orientation:'); 
        print('   t=', tCr1, 's=', orientCr1[1], 'n=', nCr1)

    #Set crystal orientation:
    optCr_1.set_orient(nCr1[0], nCr1[1], nCr1[2], tCr1[0], tCr1[1])
    orientOutFrCr1 = orientDataCr1[1] #Orientation (coordinates of base vectors) of the output beam frame 
    rxCr1 = orientOutFrCr1[0]; ryCr1 = orientOutFrCr1[1]; rzCr1 = orientOutFrCr1[2] #Horizontal, Vertical and Longitudinal base vectors of the output beam frame
    if verba == 1:
        print('   1st crystal output beam frame:'); print('   ex=', rxCr1, 'ey=', ryCr1, 'ez=', rzCr1)
    TrM = [rxCr1, ryCr1, rzCr1] #Input/Output beam transformation matrix (for debugging)
    if verba == 1:
        uti_math.matr_print(TrM)
        print('   Beam frame transformation matrix (from the begining of opt. scheme to output of current element):')
        
    
    # -----------------------------------------------------
    # monoC2 - 2nd crystal of the I20 monochromator
    # -----------------------------------------------------
    optCr_2 = SRWLOptCryst(_d_sp=dSpSi111, _psi0r=psi0rSi111,
                           _psi0i=psi0iSi111, _psi_hr=psihrSi111, _psi_hi=psihiSi111, _psi_hbr=psihbrSi111, _psi_hbi=psihbiSi111,_tc=thickCryst, _ang_as= angAsCryst)
    #Find appropriate orientation of the 2nd crystal and the corresponding output beam frame (in the incident beam frame):
    orientDataCr2 = optCr_2.find_orient(Ephot+dE_error, _ang_dif_pl= np.pi+3e-3 ) # (GsnBm.avgPhotEn) 
    orientCr2 = orientDataCr2[0] #2nd crystal orientation
    tCr2 = orientCr2[0]; nCr2 = orientCr2[2] # Tangential and Normal vectors to crystal surface
    if verba == 1:
        print('   2nd crystal orientation:'); print('   t=', tCr2, 's=', orientCr2[1], 'n=', nCr2)
    #Set crystal orientation:
    optCr_2.set_orient(nCr2[0], nCr2[1], nCr2[2], tCr2[0], tCr2[1])
    orientOutFrCr2 = orientDataCr2[1] #Orientation (coordinates of base vectors) of the output beam frame 
    rxCr2 = orientOutFrCr2[0]; ryCr2 = orientOutFrCr2[1]; rzCr2 = orientOutFrCr2[2] #Horizontal, Vertical and Longitudinal base vectors of the output beam frame
    if verba == 1:
        print('   2nd crystal output beam frame:'); print('   ex=', rxCr2, 'ey=', ryCr2, 'ez=', rzCr2)
    TrM = uti_math.matr_prod(TrM, [rxCr2, ryCr2, rzCr2]) #Input/Output beam transformation matrix (for debugging)
    if verba == 1:
        print('   Beam frame transformation matrix (from the begining of opt. scheme to output of current element):')
        uti_math.matr_print(TrM)
        print('   After the two crystals of DCM, the transformation matrix should be close to the unit matrix.')

    
    # -----------------------------------------------------
    # monoC3 - 3rd crystal of the I20 monochromator
    # -----------------------------------------------------
    optCr_3 = SRWLOptCryst(_d_sp=dSpSi111, _psi0r=psi0rSi111,
                           _psi0i=psi0iSi111, _psi_hr=psihrSi111, _psi_hi=psihiSi111, _psi_hbr=psihbrSi111, _psi_hbi=psihbiSi111,_tc=thickCryst, _ang_as= angAsCryst)
    #Find appropriate orientation of the 3rd crystal and the corresponding output beam frame (in the incident beam frame):
    orientDataCr3 = optCr_3.find_orient(Ephot+dE_error, _ang_dif_pl=3e-3) # (GsnBm.avgPhotEn) 
    orientCr3 = orientDataCr3[0] #3rd crystal orientation
    tCr3 = orientCr3[0]; nCr3 = orientCr3[2] # Tangential and Normal vectors to crystal surface
    if verba == 3:
        print('   3rd crystal orientation:'); print('   t=', tCr3, 's=', orientCr3[1], 'n=', nCr3)
    #Set crystal orientation:
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
    # monoC4 - 4th crystal of the I20 monochromator
    # -----------------------------------------------------
    optCr_4 = SRWLOptCryst(_d_sp=dSpSi111, _psi0r=psi0rSi111,
                           _psi0i=psi0iSi111, _psi_hr=psihrSi111, _psi_hi=psihiSi111, _psi_hbr=psihbrSi111, _psi_hbi=psihbiSi111,_tc=thickCryst, _ang_as=angAsCryst)
    #Find appropriate orientation of the 4th crystal and the corresponding output beam frame (in the incident beam frame):
    orientDataCr4 = optCr_4.find_orient(Ephot+dE_error, _ang_dif_pl= np.pi+3e-3 ) # (GsnBm.avgPhotEn) 
    orientCr4 = orientDataCr4[0] #4th crystal orientation
    tCr4 = orientCr4[0]; nCr4 = orientCr4[2] # Tangential and Normal vectors to crystal surface
    if verba == 4:
        print('   4th crystal orientation:'); print('   t=', tCr4, 's=', orientCr4[1], 'n=', nCr4)
    #Set crystal orientation:
    optCr_4.set_orient(nCr4[0], nCr4[1], nCr4[2], tCr4[0], tCr4[1])
    orientOutFrCr4 = orientDataCr4[1] #Orientation (coordinates of base vectors) of the output beam frame 
    rxCr4 = orientOutFrCr4[0]; ryCr4 = orientOutFrCr4[1]; rzCr4 = orientOutFrCr4[2] #Horizontal, Vertical and Longitudinal base vectors of the output beam frame
    if verba == 44:
        print('   4th crystal output beam frame:'); print('   ex=', rxCr4, 'ey=', ryCr4, 'ez=', rzCr4)
    TrM = uti_math.matr_prod(TrM, [rxCr4, ryCr4, rzCr4]) #Input/Output beam transformation matrix (for debugging)
    if verba == 1:
        print('   Beam frame transformation matrix (from the begining of opt. scheme to output of current element):')
        uti_math.matr_print(TrM)
        print('   After the two crystals of DCM, the transformation matrix should be close to the unit matrix.')


    # -----------------------------------------------------
    # Sph - Spherical mirror deflecting 
    # -----------------------------------------------------
    grazG = 3e-3
    optSph = SRWLOptMirSph(_size_tang= 2, _size_sag= 2, _r = 0.087435897,_ap_shape = 'r',
                           _nvx=0, _nvy=cos(grazG), _nvz=-sin(grazG), _tvx=0, _tvy= sin(grazG))

    # -----------------------------------------------------
    # Tor - Toroidal mirror deflecting 
    # -----------------------------------------------------
    tG,sG = 2,2
    grazG = 3e-3

    optTor = SRWLOptMirTor(_rt= 1.e+20, _rs=0.087435897,_size_tang=tG, _size_sag=sG, _x=0.0, _y=0.0,_ap_shape='r',
                            _nvx=0, _nvy= cos(grazG), _nvz=-sin(grazG), _tvx=0, _tvy=sin(grazG) )



    # -----------------------------------------------------
    # M1 - planar mirror deflecting in the Vertical Plane
    # -----------------------------------------------------
    tG, sG  = 2, 2
    grazG   = np.pi+3e-3  #  
    optM_1  = SRWLOptMirPl(_size_tang=tG, _size_sag=sG, _ap_shape='r',
                           _nvx=0, _nvy=cos(grazG), _nvz=-sin(grazG), _tvx=0, _tvy= sin(grazG))


    
    # --------------------------------------------------------
    # EM1 - elliptical mirror deflecting to collimate beam
    # --------------------------------------------------------
    tG, sG  = 2, 2
    grazG   = 3e-3# 1. * np.pi / 180 
    optEM_1   = SRWLOptMirEl(_p= 20.1755688, _q= 1.e+10, _ang_graz=grazG, _r_sag=1.e+23,
                             _size_tang=tG, _size_sag=sG,
                             _nvx=0, _nvy=-cos(grazG), _nvz=sin(grazG), _tvx=0, _tvy= -sin(grazG))
    
    # ----------------------------------------------------------
    # EM2 - elliptical mirror deflecting in the Vertical Plane
    # ----------------------------------------------------------
    tG, sG  = 2, 2
    grazG   = np.pi+3e-3 # 1. * np.pi / 180; 
    optEM_2   = SRWLOptMirEl(_p= 1.e+10, _q=23, _ang_graz=grazG, _r_sag=1.e+23,
                             _size_tang=tG, _size_sag=sG,
                             _nvx=0, _nvy= -cos(grazG), _nvz= sin(grazG), _tvx= 0, _tvy=-sin(grazG))

    # ------
    # Drifts
    # ------
    
    D1            = 6.532
    optDrift_1    = SRWLOptD(D1)                               
    D2            = 1.5                                      
    optDrift_2    = SRWLOptD(D2)
    D3            = 3 
    optDrift_3    = SRWLOptD(D3)                              
    D4            = 0.1
    optDrift_4    = SRWLOptD(D4)
    D5            = 0.1
    optDrift_5    = SRWLOptD(D5)
    D6            = 0.1
    optDrift_6    = SRWLOptD(D6)
    D7            = 3.81185#2.7
    optDrift_7    = SRWLOptD(D7)
    D8            = 4.5481#4.5
    optDrift_8    = SRWLOptD(D8) 
    D9            = 17.3477#19.5
    optDrift_9    = SRWLOptD(D9) 
    D10            = 0.1
    optDrift_10    = SRWLOptD(D10) 
    D11            = 3.4
    optDrift_11    = SRWLOptD(D11)   
    
    
    # ----------------------
    # Propagation Parameters 
    # ----------------------
    propagParApert =  [0, 0, 1., 0, 0, 1.0, 1.0, 1.0, 1., 0, 0, 0]
    propagParSph  =   [0, 0, 1., 0, 0, 1.0, 1.0, 1.0, 1., 0, 0, 0]
    propagParDrift =  [0, 0, 1., 1, 0, 1.0, 1, 1., 1, 0, 0, 0]
    propagParDrift_cr =  [0, 0, 1., 1, 0, 1., 1., 1, 1, 0, 0, 0]
    propagParPM    =  [0, 0, 1., 0, 0, 1.0, 1., 1.0, 1., 0, 0, 0]#JL:cannot change resolution
    propagParCryst =  [0, 0, 1., 0, 0, 1.0, 1.0, 1.0, 1., 0, 0, 0]
    propagParEM    =  [0, 0, 1., 0, 0, 1.0, 1.0, 1.0, 1., 0, 0, 0]#JL:cannot change resolution
    propagParTor   =  [0, 0, 1., 0, 0, 1.0, 1., 1.0, 1, 0, 0, 0]#JL:cannot change resolution
    propagParDrift_8 =  [0, 0, 1., 1, 0, 1.5, 1.5, 1.0, 1.5, 0, 0, 0]
    propagParDrift_9 =  [0, 0, 1., 1, 0, 1.5, 1.0, 1.0, 1.0, 0, 0, 0]
    propagParDrift_10 =  [0, 0, 1., 1, 0, 1.5, 1.0, 1.0, 1.0, 0, 0, 0]
    propagParDrift_11 =  [0, 0, 1., 1, 0, 1.5, 1.5, 1.0, 1.5, 0, 0, 0]
    print('+++++++++++++propagParDrift+++',propagParDrift)
    #propagParLens  =  [0, 0, 1., 0, 0, 1 ,4, 1.5, 0.3,  0, 0, 0]

    #----------------------------------
    #  Elements switch
    #----------------------------------
    Lens = 0
    Dr_1 = 1
    EM_1 = 1
    Dr_2 = 1
    PM_1 = 1
    Dr_3 = 1
    Mono_1 = 1
    Dr_4 = 1
    Mono_2 = 1
    Dr_5= 1
    Mono_3 = 1
    Dr_6 = 1
    Mono_4 = 1
    Dr_7 = 1
    Cy = 0
    Tor = 1
    Dr_8 = 1
    EM_2 = 1
    Dr_9 = 1
    PM_2 = 1
    Dr_10 = 1
    PM_3 = 1
    Dr_11 = 1



    
    # --------------------------------------------------------------------------
    # Lists of Optical Elements (oe) and Propagation Parameters (pp) are defined
    # --------------------------------------------------------------------------
    
    s = []  # position along the line from the entry aperture

    oe=[]; pp=[] 
    bl = []

 
    #bl.append("-||- ")                                                                                                                                                   # the optical elements
    #oe.append( SRWLOptA('r', 'a', slitDX*1e-6, slitDY*1e-6) )                                                                                                       # oe(1):  aperture
    #pp.append(propagParApert)
    #s.append(0)

    if  Lens == 1:
        bl.append(" () ")
        oe.append( optlen )                                                                            
    # oe(3):  CRL       
        pp.append(propagParLens)
        s.append(0)


    if Dr_1 == 1:
        bl.append(" --- ")
        oe.append( optDrift_1 )                                                                                                                                        # oe(4):  drift
        pp.append(propagParDrift)
        s.append(oe[-1].L)



	#bl.append( " --- " )
        #oe.append( SRWLOptD(8) ) #optDrift_1                                                                                                                                        # oe(2):  drift
        #pp.append(propagParDrift)
        #s.append(oe[-1].L)


	#bl.append( " --- " )
        #oe.append( SRWLOptD(9.41) )                                                                                                                                         # oe(2):  drift
        #pp.append(propagParDrift)
        #s.append(oe[-1].L)



    if EM_1 ==  1:
        bl.append( " -)- ")    
        oe.append( optEM_1 )                                                                                                                                            # oe(3): EM1 
        pp.append(propagParEM)
        s.append(0)


    if Dr_2 ==  1:
        bl.append(" --- ")
        oe.append( optDrift_2 )                                                                                                                                        # oe(4):  drift
        pp.append(propagParDrift)
        s.append(oe[-1].L)

    if PM_1 ==  1:
	bl.append(" -/- ")
	oe.append( optM_1 )                                                                                                                                             # oe(5):  plane mirror
	pp.append(propagParPM)
	s.append(0)

    if Dr_3 ==  1:    
	bl.append(" --- ")
	oe.append( optDrift_3 )                                                                                                                                         # oe(6):  drift
	pp.append(propagParDrift)
	s.append(oe[-1].L)

    if Mono_1 ==  1:
	bl.append(" -## ")
	oe.append( optCr_1 )                                                                                                                                            # oe(7):  mono-element1
	pp.append(propagParCryst)
	s.append(0)

    if Dr_4 ==  1: 
	bl.append(" --- ")
	oe.append( optDrift_4 )                                                                                                                                         # oe(8):  drift
	pp.append(propagParDrift)
	s.append(oe[-1].L)

    if Mono_2 ==  1:
	bl.append(" ##- ")
	oe.append( optCr_2 )                                                                                                                                            # oe(9):  mono-element2
	pp.append(propagParDrift)
	s.append(0)

    if Dr_5 ==  1:
	bl.append(" --- ")
	oe.append( optDrift_5 )                                                                                                                                         # oe(10): drift
	pp.append(propagParDrift)
	s.append(oe[-1].L)

    if Mono_3 ==  1:
	bl.append(" -## ")
	oe.append( optCr_3 )                                                                                                                                            # oe(11): mono-element3
	pp.append(propagParCryst)
	s.append(0)

    if Dr_6 ==  1:
	bl.append(" --- ")
	oe.append( optDrift_6 )                                                                                                                                         # oe(12): drift
	pp.append(propagParDrift)
	s.append(oe[-1].L)

    if Mono_4 ==  1:
	bl.append(" ##- ")
	oe.append( optCr_4 )                                                                                                                                            # oe(13): mono-element4
	pp.append(propagParCryst)
	s.append(0)

    if Dr_7 ==  1:
	bl.append(" --- ")
	oe.append( optDrift_7 )                                                                                                                                         # oe(14): drift
	pp.append(propagParDrift)
	s.append(oe[-1].L)

    if Cy ==  1:                                                                                                                                                      # oe(15): Cylinder
	bl.append(" -/)- ")
	oe.append( optSph )                                                                                                                                             
	pp.append(propagParSph)
	s.append(0)

    if Tor ==  1:
	bl.append(" -()- ")
	oe.append( optTor )                                                                                                                                             
	pp.append(propagParTor)
	s.append(0)

    if Dr_8 ==  1:                                                                                                                                                        # oe(16): drift
	bl.append(" --- ")
	oe.append( optDrift_8 )                                                                                                                                         
	pp.append(propagParDrift_8)
	s.append(oe[-1].L)

    if EM_2 ==  1:                                                                                                                                                        # oe(17): EM2
	bl.append( " -)- ")    
	oe.append( optEM_2 )                                                                                                                                            
	pp.append(propagParEM)
	s.append(0)

    if Dr_9 ==  1:                                                                                                                                                        # oe(18): drift
	bl.append(" --- ")
	oe.append( optDrift_9 )                                                                                                                                        
	pp.append(propagParDrift_9)
	s.append(oe[-1].L)

    if PM_2 ==  1:                                                                                                                                                        # oe(19): Plane mirror
	bl.append(" -/- ")
	oe.append( optM_1 )                                                                                                                                             
	pp.append(propagParPM)
	s.append(0)

    if Dr_10 ==  1:                                                                                                                                                        # oe(20): drift
	bl.append(" --- ")
	oe.append( optDrift_10 )                                                                                                                                      
	pp.append(propagParDrift_10)
	s.append(oe[-1].L)


    if PM_3 ==  1:                                                                                                                                                         # oe(21): Plane mirror
	bl.append(" -/- ")
	oe.append( optM_1 )                                                                                                                                             
	pp.append(propagParPM)
	s.append(0)

    if Dr_11 ==  1:                                                                                                                                                        # oe(22): drift
	bl.append(" --- ")
	oe.append( optDrift_11 )                                                                                                                                     
	pp.append(propagParDrift_11)
	s.append(oe[-1].L)


    bl.append(" --|S  ")
    bl = ''.join(bl)
    print "{}".format(bl)
    cs = np.cumsum(s)
    print("  ".join(str(round(x+16.968,4)) for x in cs))#x+16.968

    oe_pp =[]; oe_pp.append(oe); oe_pp.append(pp)
        
    return oe_pp


    
