"""Defines functionality for pipeline.

"""
from re import findall
from sys import exit
from subprocess import Popen, PIPE, STDOUT
from tfpipe.utils import logger

# add more checks and validation
class WorkFlow(object):
    """WorkFlow creates and executes job submission statements.

    """
    dep_options = ('done', 'ended', 'exit', 'external',
                   'post_done', 'post_err', 'started')
    def __init__(self, job_list=[], lsf=True):
        """Initialize WorkFlow.

        Method sets job lists and environment.  Depending on the
        environment, job names are checked before submission.

        """
        self.jobs = job_list
        self.lsf = lsf
        self._check_jobnames()
        logger.info("WorkFlow created")

    def _check_jobnames(self):
        """Method to check job names for duplicates.

        WorkFlow terminates if duplicate is found in LSF mode.

        """
        job_names = [job.name for job in self.jobs]
        if (len(set(job_names)) == len(job_names)) and self.lsf:
            logger.info("WorkFlow job names are unique.")
        elif self.lsf:
            logger.warn("WorkFlow job names are NOT unique.")
            exit("WARNING: WorkFlow job names are NOT unique.")

    def _create_submit_str(self, job):
        """Build submission string.

        Use lsf scheduler, bsub, if self.lsf is True.

        """
        return (self._build_bsub(job) if self.lsf else '') + str(job)

    def _create_submit_list(self, job):
        """Build list of submission command.
        
        Use lsf scheduler, bsub, if self.lsf is True.

        """
        bsub = self._build_bsub(job).split() if self.lsf else []
        return bsub + job.show_as_list()
        
    def _update_dep_str(self, job):
        """Updates lsf dependency string.

        """
        job_dep_options = findall(r"[\w']+", job.dep_str)
        print job.dep_str
        for depopt in job_dep_options:
            job.dep_str.replace(depopt, depopt + job.dep[depopt].pop(0))
        print job.dep_str
        return "&&".join([d.name for d in job.dep])

    def _build_bsub(self, job):
        """Create bsub command submission string.

        """
        bsub = "bsub -J %s -o ~/%s.out " % (job.name, job.name)
        bsub += "-w done(%s) " % self._update_dep_str(job) if job.dep else '' 
        
        return bsub

    def add_job(self, newjob):
        """ """
        pass

    def show(self):
        """Method shows all job submission strings and lists in WorkFlow.

        """
        for job in self.jobs:
            print self._create_submit_str(job)
#            print self._create_submit_list(job)
            logger.info("WorkFlow SHOW: %s" % 
                        self._create_submit_str(job))
            
    def run(self):
        """Method submits command list to shell.

        """
        for job in self.jobs:
            p = Popen(self._create_submit_list(job))
            retval = p.wait()
            logger.info("WorkFlow SUBMIT: %s" % 
                        self._create_submit_str(job))


# need ability to specify how dependency should work, whether 
# it's done, exited, ended, etc.


