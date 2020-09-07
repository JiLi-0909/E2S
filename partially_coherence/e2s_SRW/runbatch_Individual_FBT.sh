#!/bin/bash

#$ -cwd
#$ -N e2s_SRW
#$ -pe openmpi 10
#$ -l redhat_release=rhel6
#$ -q ap-medium.q

# modules
module purge
module load global/cluster-ap
module load openmpi/3.1.3
module load python/ana

# job environment
#SRW_NPROCS=50
#SRW_EXE_PATH=/dls_sw/apps/python/anaconda/1.7.0/64/bin/

# run SRW
#mpiexec python SRW_individualelectrons.py SRW.input 
mpiexec python SRW_individualelectrons_BLasParam_I20.py SRW_I20.input

# OLD command
#mpiexec /dls_sw/apps/python/anaconda/1.7.0/64/bin/python  SRW_individualelectrons_BLasParam.py SRW.input

