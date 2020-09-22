#!/bin/bash



# modules
module purge
#module load global/cluster-ap
module load openmpi/3.1.4
#module load python/ana

# job environment
#SRW_NPROCS=50
#SRW_EXE_PATH=/dls_sw/apps/python/anaconda/1.7.0/64/bin/

# run SRW
#mpiexec python SRW_individualelectrons.py SRW.input 
#mpiexec python SRW_individualelectrons_BLasParam.py SRW.input
#mpiexec /dls_sw/apps/python/anaconda/1.7.0/64/bin/python SRW_individualelectrons_BLasParam.py SRW.input


mpirun -np $NSLOTS /dls_sw/apps/python/anaconda/4.6.14/64/envs/python2.7/bin/python SRW_individualelectrons_BLasParam.py SRW.input

#/dls_sw/apps/python/anaconda/1.7.0/64/bin/python
#/dls_sw/apps/python/anaconda/4.6.14/64/envs/python2.7/bin/python

# OLD command
#mpiexec /dls_sw/apps/python/anaconda/1.7.0/64/bin/python  SRW_individualelectrons_BLasParam.py SRW.input

