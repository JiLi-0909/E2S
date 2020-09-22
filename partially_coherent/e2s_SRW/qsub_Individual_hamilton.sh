#qsub  -q all.q -P ap -V  -pe openmpi 80 pan_runbatch_Individual_hamilton.sh
qsub -P ap -pe openmpi 80  pan_runbatch_Individual_hamilton.sh
