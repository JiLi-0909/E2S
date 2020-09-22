import socket
import subprocess


HOSTNAME = socket.gethostname().lower()


def get_job_id_string(local_id, environ_id, format_string):
    return local_id + '=$(printf -- "' + format_string + '" $' + environ_id +')'


# Diamond Environment
if 'diamond' in HOSTNAME:
    import pkg_resources
    import os
    #pkg_resources.require('nsga2==0.5')
    #pkg_resources.require('matplotlib==1.3.1')

    ELEGANT_BINARY = 'elegant'  # Rely on module command to place on PATH
    PELEGANT_BINARY = 'Pelegant'
    ELEGANT_MODULE_FILE = '/dls_sw/prod/tools/RHEL6-x86_64/defaults/modulefiles/elegant/28-1-0'
    SUBMIT_COMMAND = 'qsub'

    def job_is_running(job):
        if 'r' in job[4]:
            return True
        return False

    def job_is_waiting(job):
        if 'w' in job[4]:
            return True
        return False

    def job_id_from_job(job):
        return job[0]

    def get_running_jobs(jobname):
        print('2222to be or not to be, that\'s the question')
        command = 'qstat -g d'
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0]
        print('to be or not to be, that\'s the question')
        if not output:
            print('oh nooooo')
            return []
        output = [line.split() for line in output.split('\n')[:-1]][2:]
        output = [x for x in output if jobname == x[2]]
        return output

    def get_submission_text(
            timeout, job_range, cores, rootname,
            directory, job_index_format_specifier, summarise_command):

        root_path = os.path.join(directory, rootname)
        return '\n'.join([
            '#!/bin/bash',
            '#$ -l h_rt=' + timeout + ',' + 'infiniband=True',
            '#$ -t %d-%d' % job_range,
            '#$ -q ap-medium.q',
            '#$ -pe openmpi ' + str(cores),
            '#$ -N ' + rootname,
            '#$ -e ' + root_path + 'submit.e',
            '#$ -o ' + root_path + 'submit.o',
            'cd ' + directory,
            get_job_id_string(
                'padded_id', 'SGE_TASK_ID', job_index_format_specifier),
            'module load ' + ELEGANT_MODULE_FILE,
            (''
                + 'mpirun -mca btl openib,self -np \$NSLOTS '
                + PELEGANT_BINARY + ' evalDIAMONDdiff.ele '
                + '-macro=$(cat ' + root_path + '$padded_id.macros) '
                + '2> ' + root_path + '$padded_id.e '
                + '1> ' + root_path + '$padded_id.o '
            ),
            summarise_command,
            ])


# Hartree Environment

    
# SCARF Environment



else:
    print 'ERROR: Could not determine cluster'
    sys.exit(1)

