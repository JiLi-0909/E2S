
from math import exp, sqrt, sin
from random import random
import multiprocessing
import sys
from InGenNoMain import func_optBL
import time

# HERE !!


import sys, os, time, math
sys.path.append(os.path.dirname(os.path.abspath("__file__")))

import cluster  # This sets up imports for different platforms

import traceback, tempfile, subprocess


def kur(x,rootnumber):
    print('====================================================================================================')
    
    #Imax,sigx,sigy=func_optBL(k13,k15)
    print('---------------JL: now we are in I20 accelerator and beamline optimisation------------------------') 
    print("x vaut :",x)
    print("-------------------------------------BEAMLINE HARDWARE--------------------------------------------")
    print("x[0] vaut:")
    print(x[0])
    print("x[1] vaut:")
    print(x[1])
    print("x[2] vaut:")
    print(x[2])
    print("x[3] vaut:")
    print(x[3])
    print("x[4] vaut:")
    print(x[4])

    print("-------------------------------------ACCELERATOR OPTICS--------------------------------------------")
    print("x[5] vaut:")
    print(x[5])
    print("x[6] vaut:")
    print(x[6])
    print("x[7] vaut:")
    print(x[7])
    print("x[8] vaut:")
    print(x[8])
    print("x[9] vaut:")
    print(x[9])
    print("x[10] vaut:")
    print(x[10])
	
    print("(FBT: remember indexation commences at 0, not 1)")
    print("------------------------------------- End of parameters display --------------------------------------------")
    blob=func_optBL(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],rootnumber) # 7D  HERE
    #blob=func_optBL(x[0],x[1],rootnumber) # 2D
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('the output blob from func_optBL is printed here in kur_fct_for_qsub.py:')
    print(blob)
    print('blob printed, now leaving the function kur(x) in the kur_fct_for_qsub.py file, and returning to the caller file...')
    

    return blob#(Imax,sigx) #f0/f1


def kur99(x):
    print('====================================================================================================')

    print('standard MOEA test problem KUR')
    print('FBT: x vaut :')
    print(x)
    print('====================================================================================================')

    #FBT : f0 et f1 sont calcules a partir des "individules", qui sont les parents initiaux
    N = 3 #FBT 3
    f0 = 0
    for i in range(N-1):
        f0 = f0 + -10 * exp(-0.2 * sqrt(x[i] ** 2 + x[i+1] ** 2))
    f1 = 0
    for i in range(N):
        f1 = f1 + abs(x[i]) ** 0.8 + 5 * sin(x[i] ** 3)
    print('====================================================================================================')


    print("f0 vaut : "+str(f0)+ " et f1 vaut : "+str(f1))
    print('====================================================================================================')

    print(cluster.SUBMIT_COMMAND)
    print('@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@~@')
    return (f0, f1)





if __name__ == "__main__":  # For testing

    print('()()()()())))()(((((()()()()()()()()')
    # FBT: we get sys.argv[1], rootname to use...
    run_name=sys.argv[1] # en effet, sys.argv[0] est le fichier python appelant...
    print("the rootname for this calculation is:")
    print(run_name)

    variable_file=run_name + '.var'

    options = {}
    # load variables in file into options structure
    execfile(variable_file, options)
    # some checks (better find out about missing parameters now than later)
    schema = ("gene", "array")

    param=options["gene"]
    print(' le gene est :')
    print(param)
    print(' et la solution est: ')
    #print(kur(param))
    this_sol=kur(param,run_name)
    print(this_sol)


    solution_file_1=run_name+'.sol2'
    with open(solution_file_1,'w') as f111:
        f111.write('sol='+ str(this_sol)+'\n')
    #with open(solution_file_1,'w') as f111:
    #    f111.write('sol='+ str(kur(param))+'\n')
    f111.close()    # added FBT 13.11.2018 to correct the synchronization error





