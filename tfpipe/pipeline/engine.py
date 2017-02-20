"""Defines functionality for pipeline.

"""
from re import findall
from os import system
from sys import exit
from datetime import datetime
from tfpipe.utils import logger, DuplicateJobNames

class WorkFlow(object):
    """WorkFlow creates and executes job submission statements.

    """
    def __init__(self, job_list=[], lsf=True, slurm=False, name=None, additionalmodules={}):
        """Initialize WorkFlow.

        Method sets job lists and environment.  Depending on the environment, 
        job names are checked before submission.

        """
        self.jobs = job_list
        #LSF for the moment overides SLURM
        if lsf:
            self.lsf = True
            self.slurm = False
        elif slurm:
            self.lsf = False
            self.slurm = True
        else:
            #TODO I am not sure why we are allowing this situation. At somepoint we need to probably wipe this option
            self.lsf = False
            self.slurm = False
            assert False
        self._check_jobnames()
        self.additionalmodules = additionalmodules
        now = datetime.now()
        if not name:
            self._shell_script = '%s_tfpipe_workflow.sh' % \
                now.strftime("%Y%m%d%H%M%S")
        else:
            self._shell_script = name
        logger.info("WorkFlow created")

    def _check_jobnames(self):
        """Method to check job names for duplicates.

        WorkFlow terminates if duplicate is found in LSF mode.

        """
        job_names = [job.name for job in self.jobs]
        if (len(set(job_names)) == len(job_names)) and (self.lsf or self.slurm):
            logger.info("WorkFlow job names are unique.")
        elif (self.lsf or self.slurm):
            DuplicateJobNames("WARNING: WorkFlow job names are NOT unique.")

    def _create_submit_str(self, job):
        """Build submission string.

        Use lsf scheduler, bsub, if self.lsf is True.

        """
        #TODO Ok this may change things a bit now that the job object can store a memory requirement that will now have to be passed to the build_bsub
        if self.lsf:
            jobsched_str = self._build_bsub(job) or ''
        elif self.slurm:
            jobsched_str = self._build_sbatch(job) or ''
        else:
            assert False
        if job.redirect_output or job.redirect_error:
            job_str = '"' + str(job) + '"'
        else:
            job_str = str(job)
        self.current_submit_str = jobsched_str + job_str
        return self.current_submit_str

    # need to check # of individual dep conds in dep_options equals number 
    # of jobs passed to each dep condition
    def _update_dep_str(self, job):
        """Updates lsf dependency string.

        If dependency string was set explicitly during initialization, return 
        the dependency specified at initialization.  Otherwise, build dependency
        string using dep_str heuristic and the dependency condition variables 
        specified in the add_dependency method.

        """
        if job.dep_str_at_init:
            return '-w \"%s\"' % job.dep_str
        dep_options = findall(r"[\w']+", job.dep_str) 
        for depopt in set(dep_options):
            tmp_dep_str = job.dep_str.replace(depopt, depopt + "(%s)")
        job_deps = tuple([job.dep.get(jdo).pop(0).name for jdo in dep_options])
        return '-w \"%s\"' % (tmp_dep_str % job_deps)

    def _build_sbatch(self, job):
        """Create the sbatch (SLURM) command submission string.

        """
        #TODO Need to fix this!
        if not job.dep_str:
            job._build_dep_str()
        bargs = ' '.join(["%s %s" % (k, v) for k, v in job.bsub_args.items()])
        bdep = self._update_dep_str(job) if job.dep_str else ''
        sbatch = "sbatch -J %s %s -o %s %s " % (job.name,
                                                bdep,
                                                job.job_output_file,
                                                bargs)
        job_str = str(job)
        if job_str.count('|'):
            if (job_str.count('|')+1) > 8:
                exit("Too many threads.  Adapter file must be eight or less.")
            sbatch += '-n %d -R "span[hosts=1]" ' % (job_str.count('|') + 1)
        return sbatch

    #TODO Place in memory req from the job object into the bsub?
    def _build_bsub(self, job):
        """Create bsub (LSF) command submission string.

        """
        if not job.dep_str:
            job._build_dep_str()
        bargs = ' '.join(["%s %s" % (k, v) for k, v in job.bsub_args.items()])
        bdep = self._update_dep_str(job) if job.dep_str else ''
        bsub = "bsub -J %s %s -o %s %s " % (job.name,
                                                bdep,
                                                job.job_output_file,
                                                bargs)
        job_str = str(job)
        if job_str.count('|'):
            if (job_str.count('|')+1) > 8:
                exit("Too many threads.  Adapter file must be eight or less.")
            bsub += '-n %d -R "span[hosts=1]" ' % (job_str.count('|') + 1)
        return bsub

    def _build_shell_script(self):
        """ """
        mods = []
        #TODO I need to work on a way to allow alternate Modules depending on the server
        with open(self._shell_script, 'w') as f:
            f.write("#!/bin/bash\n")
            if self.lsf:
                f.write(". /nas02/apps/Modules/default/init/bash\n")
                for job in self.jobs:
                    try:
                        if job._module not in mods:
                            f.write("module load %s\n" % job._module)
                            mods.append(job._module)
                    except AttributeError:
                        pass
                for module in self.additionalmodules:
                    try:
                        if module not in mods:
                            f.write("module load %s\n" % module)
                            mods.append(module)
                    except AttributeError:
                        pass
            for job in self.jobs:
                f.write("%s\n" % self._create_submit_str(job))
        logger.info("WorkFlow Submission Script Created")

    def add_job(self, newjob):
        """Add job to list.

        """
        self.jobs.append(newjob)
        logger.info("WorkFlow ADD: %s" % newjob)

    def show(self):
        """Method shows all job submission strings and lists in WorkFlow.

        """
        for job in self.jobs:
            submit_str = self._create_submit_str(job)
            print submit_str
            logger.info("WorkFlow SHOW: %s" % submit_str)
            
    def run(self):
        """Method submits command list to shell.

        """
        self._build_shell_script()
        system("bash %s" % self._shell_script)
        logger.info("WorkFlow SUBMIT: %s" % self._shell_script)
