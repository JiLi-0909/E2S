from math import exp, sqrt, sin
from random import random
import multiprocessing
import time
import glob
import subprocess




import sys, os, time, math,re
sys.path.append(os.path.dirname(os.path.abspath("__file__")))

import cluster  # This sets up imports for different platforms

import traceback, tempfile, subprocess

"nsga2 input file for KUR test problem"

#
# Run with:
# ./nsga.py INPUT_FILENAME
#

# probability of random mutation (increases the diversity of solutions)
# pmut_real = 0.1 / number of decision variables is recommended by the NSGA2 paper
pmut_real = 0.1 / 3

# probabilty of crossover between two individuals
# pcross_real = 0.9 is recommended in the NSGA2 paper
pcross_real = 0.9

# eta_m is the mutation distribution index for polynomial mutation
# see "Survey on multiobjective evolutionary and real coded genetic algorithms"
# http://www.complexity.org.au/conference/upload/raghuw01/raghuw01.pdf
# eta_m = 20 is recommended in the NSGA2 paper
eta_m = 20

# eta_c is the crossover distribution index
# (controls how close the children are to the parents)
# er number, closer to the parents
# see "Survey on multiobjective evolutionary and real coded genetic algorithms"
# http://www.complexity.org.au/conference/upload/raghuw01/raghuw01.pdf
# eta_c = 20 is recommended in the NSGA2 paper
eta_c = 20
root_number=1

# this is the function to optimize, see the comments for func=kur just below
def kur900(x):
    print('====================================================================================================')
    print('====================================================================================================')
    print('standard MOEA test problem KUR')
    print('FBT: x vaut :')
    print(x)
    print('====================================================================================================')
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
    print('====================================================================================================')

    print("f0 vaut : "+str(f0)+ " et f1 vaut : "+str(f1))
    print('====================================================================================================')
    print('====================================================================================================')
    print(cluster.SUBMIT_COMMAND)
    return (f0, f1)

# 'evaluate' is passed a list of individules, each individule is represented by
# a tuple of parameter values which should be evaulated then returned in an iterable
# with matching indicies.

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################


def get_nb_jobs():

    command = 'qstat -g d'
    output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0]
	    #output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0]	
    output2 = [line.split() for line in output.split('\n')[:-1]][2:]
    #output = [x for x in output if jobname == x[2]]
    return len(output2)

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################

def evaluate(population):  # original kur evaluate, works
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print('populations')
    print(len(population))
    print(population)
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print('/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/')

    print('/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/')
    print('Evaluating population of size : ',len(population))
    # Don't do anything if population is empty. It's probably caused
    # by all jobs failing and NSGA having no dominators for the next round.
    if not population:
        print 'Error: population was empty, did any jobs succeed?'
        sys.exit(-1)

    # Useful to have these combined
    root_path = os.path.join(TMP_DIR, ROOTNAME)

    # Work out unique task Job / Task IDs
    global root_number
    task_range = range(root_number, root_number + len(population))
    root_number = root_number + len(population) # on update root number comme ca les runs de la prochaine generations recommencent pas a 1
   #tt=[]-----> don't use
#    for p in population: #--> rejeter a la fin
#       tt.append(kur(p)) #--> rejeter a la fin



    for p,task in zip(population,task_range):
        run_name = ROOTNAME + INDEX_FORMAT_CODE % task
        print(run_name)


        variable_file=run_name+'.var'
        f1=open(variable_file,'w')
        f1.write('gene='+ str(p)+'\n')
        f1.close()



        submit_file=run_name+'-submit.sh'
        f2=open(submit_file,'w')
            #f2.write('/dls_sw/apps/python/anaconda/1.7.0/64/bin/python kur_fct_for_qsub.py'+' '+ run_name +'\n') # here on voit que kur_fct_for_qsub.py is called   MEDIUM QUEUE
        f2.write('mpiexec /dls_sw/apps/python/anaconda/1.7.0/64/bin/python kur_fct_for_qsub.py'+' '+ run_name +'\n') # here on voit que kur_fct_for_qsub.py is called HIGH QUEUE
        f2.close()

            # FBT: make the *-submit.sh executable 
        commande1='chmod +x '+submit_file
        subprocess.call(commande1,shell=True)
           


           #maintenant, on va creer les olution par le script ci-dessus puis la stocker dans un *.sol2-file.
           #commande2='./'+submit_file    #----->>>>> C'EST CETTE PARTIE QUI SERA REMPLACEE PAR LE QSUB
           #subprocess.call(commande2,shell=True)
        
        submit_job_file=run_name+'-submit_job.sh'
        f4=open(submit_job_file,'w')
            #f4.write('qsub -q ap-medium.q -l redhat_release=rhel6 -V -pe openmpi 1'+' '+ submit_file +'\n') # here on voit que kur_fct_for_qsub.py is called MEDIUM QUEUE
        f4.write('qsub -q ap-medium.q -l redhat_release=rhel6 -V -pe openmpi 1'+' '+ submit_file +'\n')                                    # HIGH QUEUE
        f4.close()
            # FBT: make the *-submit.sh executable
        commande11='chmod +x '+submit_job_file
        subprocess.call(commande11,shell=True)
  

            #maintenant, on va creer les olution par le script ci-dessus puis la stocker dans un *.sol2-file.
        commande22='./'+submit_job_file    #----->>>>> C'EST CETTE PARTIE QUI SERA REMPLACEE PAR LE QSUB
        subprocess.call(commande22,shell=True)      



#    read_files = [this_file for this_file in all_files 
#                    if (int(re.findall('\d+', this_file)[-1]) > 18000)]
#
#    print read_files
     


        #solution_file_1=run_name+'.sol1'
        #with open(solution_file_1,'w') as f1:
        #   f1.write('sol='+ str(kur(p))+'\n')

#        if task==17:
#            filename='submitscript'+ INDEX_FORMAT_CODE % task +'.sh'
#            with open(filename,'w') as f17:
#                f17.write
       
       




      #  tt.append(kur(p)) -----> don't use



    #wait that all solutions have been produced: trivial in interactive mode, but in the cluster, the execution times can be different so we must wait.


    print('waiting for files ...')




    # The set of blocks below is totally different from Matt's code, which doesn't work with E2S
    #----------------------------------------------------------------------------------------------------------------------------
    # 1 - we get the number of jobs submitted, both waiting and running ones
    time.sleep(3)
    aaa=get_nb_jobs()
    while aaa>0:
        aaa=get_nb_jobs() # at the moment, assumes the user only submits one job. Needs to be refined if several concurrent jobs.
        time.sleep(6)
    #----------------------------------------------------------------------------------------------------------------------------
    # 2-  we get the last generation of variable files that have been produced, i.e. length of population
    
    print(' the length of population is : ',str(len(population)))
    command88='ls -lart *.var | tail -' +str(len(population))
    print('the command88 is: ')
    print(command88)
    output88a = subprocess.Popen(command88, shell=True, stdout=subprocess.PIPE).communicate()[0]
    output88 = [line.split() for line in output88a.split('\n')[:-1]][0:] # from first line output to last one
    list_var_files=[x[8] for x in output88]
    print('list of variable files at this stage:\n')
    print(list_var_files)
    print('\n\n')

    #-----------------------------------------------------------------------------------------------------------------------------
    # 3 - we then extract their rootname
    list_last_generation_rootnames=[]
    for pp in range(len(list_var_files)):
        r2=os.path.splitext(list_var_files[pp])
        list_last_generation_rootnames.append(r2[0])
    #-----------------------------------------------------------------------------------------------------------------------------
    # 4 - we create the list of associated solutions (just the filenames)
    list_sol2_files=[dd+'.sol2' for dd in list_last_generation_rootnames]
    #----------------------------------------------------------------------------------------------------------------------------- 
    # 5 - now the tricky part: for each member of the population, we must retrieve the associated solution computed in the cluster
    #     To do that, is member of population is identified within the list of variables, and we then retrieve the *.sol2 file in the list
    #     This is because the position of population member and the variable file can be different, while the position of a data in the variable file and solution file are the same

    output_from_this_generation=[]
    for p in population:
        print('now processing the chromosome:')
        print(p)
        for p_var in list_last_generation_rootnames:
            options = {}
            variable_file_to_open=p_var+'.var'
            execfile(variable_file_to_open, options)
            schema = ("gene", "array")
            param_from_file=options["gene"]
            if p==param_from_file:
                print('genes found:')
                print('p:')
                print(p)
                print('param_from_file:')
                print(param_from_file)
                options = {}
                sol2_file=p_var+'.sol2'
                execfile(sol2_file, options)
                schema = ("sol", "array")
                print('the solution file is:')
                print(sol2_file)

                soluce_from_file=options["sol"]
                print('and the content is:')
                print(soluce_from_file)
                output_from_this_generation.append(soluce_from_file)
           # with open(p_var+'.sol2','r') as f333:

           # load variables in file into options structure

            # some checks (better find out about missing parameters now than later)

            #f333.close()

    with open('/E2S_JL/E2S-SRWopimiser/e2s_SRW/log_machine.txt','a') as f92:
       f92.write('\n\npopulation:')
       f92.write(str(population))
       f92.write('\n\n the generation output is:\n\n')
       f92.write(str(output_from_this_generation))
       f92.close()
   

    return output_from_this_generation
    #time.sleep(2)
    #print('tt vaut')
    #print(tt)
    #return tt  -> c'est ici que ca merde car ca passe pas a la seconde generation, en effet, tt a ete supprimer ci-dessus
    #return [kur(p) for p in population]
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################

def evaluate00(population):  # modified version
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print('populations')

    print(population)
    

    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    pool = multiprocessing.Pool(2)

    #results=pool.map(kur,[[1,2,1],[3,4,1]]) 

    results=pool.map(kur,population)
    #chaque p dans population sera un envoi dans le cluster
    # il faudra lire les resultats, puis les retourner pour etre envoyer a l'exterieur par evaluate 
    print(' the results are -------------------------------------------------------')
    print(results)
    print(' ----------- -------------------------------------------------------')   
    
    return results


############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################

# these are the bounds of the inputs
params = ("par1","par2","par3","par4","par5","par6",)   

##################################################################################################
#min_realvar = [-5, -5, -5]
#max_realvar = [ 5,  5,  5]

#individules = [
#       (-1.1534729487103972, -1.153112248623409, -1.121873860795176),
#       (-1.1036729877868408, -0.013225934565451625, -0.5393128633611639),
#    ]
#individules = [
#       [-1.1534729487103972, -1.153112248623409, -1.121873860795176],
#       [-1.1036729877868408, -0.013225934565451625, -0.5393128633611639],
#    ]
##################################################################################################


#eta_xp = 0.002856481
# ---------------------------------------------------------------------------
#I20 scan branch
#JL:optimisation of twiss parameters, 30 population and 20 generations              
#min_realvar = [ 2.6995, 0.087435896 ,4.4999 ,22.999 , 19.4999, 1.869495 , -0.19483,0.52554,0.1567840,0.07079280,0.002856470]
#max_realvar = [ 2.7005, 0.0874358971 ,4.5002 ,23.002 , 19.5002, 10.869495, -0.194828, 5.52554, 0.1567870,0.07079298, 0.002856482]#

#individules = [
#       (2.7 , 0.087435897 ,4.5, 23 , 19.5,4.869495,-0.1948295,1.52554,0.1567854,0.07079287,0.002856480),#JL:be careful with radius of spherical mirror,0.087 reduce the sigmax to 160um.
#       (2.7 , 0.087435897 ,4.5, 23 , 19.5,8.869495,-0.1948295,4.52554,0.1567854,0.07079287,0.002856480),
#    ]

# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
#I20 scan branch
#JL:boiled machine and beamline:optimisation of twiss parameters+beamline variations, 30 population and 20 generations              


#individules = [
#       (2.7 , 0.087435897 ,4.5, 23 , 19.5,4.869495,-0.1948295,1.52554,0.1567854,0.07079287,0.002856481),
#       (3.5 , 0.077435897 ,5  , 18 , 23  ,3.869495,-0.0      ,2.52554,0.0567854,0.01079287,0.004),
#    ]

#min_realvar = [  1, 0.05,2.5,20,15]
#max_realvar = [ 4 , 0.1 ,6.5,25,20]
min_realvar = [ 1, 0.07 ,3 ,20 , 15, 2, -0.5, 0, 0, 0  , 0.0]
max_realvar = [ 4, 0.1  ,6 ,25 , 25, 6  , 0 , 3, 0.5, 0.1, 0.005]

individules = [
       (2.7 , 0.087 ,4.5 , 23    , 19.5  ,4.869495,-0.1948295,1.52554,0.1567854,0.07079287,0.002856481),
       (3.75, 0.084 ,4.05, 21.01 , 18.14 ,3.869495,-0.0      ,2.52554,0.0567854,0.0,0.0 ),
    ]




# this is the population size
# larger population, better diversity of solutions
population_size = 100 # 

# this is the number of generations (iterations)
# more generations, better convergence
generations =50# 

# the seed used for the random number generator
# ensures repeatable results with the same
# paraneters
seed = 0

# this is the filename for the postscript front
# use ps2pdf front.ps to make a pdf from the postscript, view it
# in windows
front_filename = "front.ps"


###############################################################################
### Appart from 'def evaluate' definitions below this line are for our use
### only. They are not use as part of the NSGA paramters.

ELEGANT_MACRO_LIST = {}
THIS_FILE_PATH = os.path.dirname(os.path.abspath("__file__"))
TMP_DIR = os.path.join(THIS_FILE_PATH, 'tmp')
ROOTNAME = 'nsgaTest'
INDEX_FORMAT_CODE = '-%06d'


STATUS_FILE_PATH = os.path.join(TMP_DIR, 'status.py')
PENALTY_VALUE = 1E9

CORES = 3
TIMEOUT = '12:00:00'








############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################


if __name__ == "__main__":  # For testing
    evaluate(individules)

