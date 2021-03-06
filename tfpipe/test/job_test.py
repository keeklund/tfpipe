"""Unittest tests for tfpipe Job class.

"""
import unittest
from tfpipe.base import Job
from tfpipe.modules.galaxy import FastqToFasta
from tfpipe.utils import InvalidInput, InvalidObjectCall

class JobBadInput(unittest.TestCase):
    """Most of Job testing in following Test Class.

    Important to note that Job was written to be inheritted, not called 
    directly.

    """
    def test_job_input(self):
        """Job cannot be called directly."""
        self.assertRaises(InvalidObjectCall, Job)


class ModuleEmptyInit(unittest.TestCase):
    """Test initialization of module when key-word input arguments are empty.

    """
    def setUp(self):
        """Set up a job initialized with out input parameters.

        Job used in class test cases.

        """
        self.fq2a_job = FastqToFasta()

    def test_job_init_cmd(self):
        """Module should inherit job and initialize cmd.

        """
        self.assertEqual(self.fq2a_job.cmd, 'fastq_to_fasta')

    def test_job_init_args(self):
        """Module initialized without args, args should be empty dictionary.

        """
        self.assertDictEqual(self.fq2a_job.args, {})

    def test_job_init_name(self):
        """Module init without name, name should be random string, 8 letters.

        """
        self.assertTrue(len(self.fq2a_job.name) == 8)
        self.assertIsInstance(self.fq2a_job.name, str)

    def test_job_init_dep_str(self):
        """Module dependency string should be empty.

        """
        self.assertEqual(self.fq2a_job.dep_str, '')

    def test_job_init_dep_at_init(self):
        """Module if dep_string is empty, attribute False.
        
        """
        self.assertFalse(self.fq2a_job.dep_str_at_init)

    def test_job_init_dep(self):
        """Dependencies are empty, nested lists in a dictionary.

        """
        self.assertIsInstance(self.fq2a_job.dep, dict)
        for k in self.fq2a_job.dep.keys():
            self.assertIsInstance(self.fq2a_job.dep[k], list)
            self.assertEqual(self.fq2a_job.dep[k], [])

    def test_job_as_string(self):
        """__str__ method returns a command line execution representation.

        """
        self.assertEqual(str(self.fq2a_job), "fastq_to_fasta  ")

    def test_add_argument(self):
        """Method to add arguments to job.

        """
        self.fq2a_job.add_argument('-i', 'inputfile.fq')
        self.assertDictEqual(self.fq2a_job.args, {'-i': 'inputfile.fq'})
        self.assertEqual(str(self.fq2a_job), 'fastq_to_fasta -i inputfile.fq')

    def test_add_jobname(self):
        """Replace 8 char random string with human readable option.

        """
        self.fq2a_job.add_jobname("ThisIsMyTestJob")
        self.assertEqual(self.fq2a_job.name, "ThisIsMyTestJob")

    def test_add_dependency_invalid_arg(self):
        """Test dependency condition passed is a valid LSF option.

        """
        # problem here with assertRaises
        self.assertRaises(InvalidInput, 
                          self.fq2a_job.add_dependencies,
                          typo=['somejob',])

    def test_add_dependency_no_dep_str(self):
        """Add dependency, create LSF dependency string.

        """
        self.fq2a_job.add_dependencies(done=['job1', 'job2'],
                                       exit=['job3'])
        self.assertDictEqual(self.fq2a_job.dep, 
                             {'done':['job1','job2'],
                              'exit':['job3',],
                              'ended': [], 
                              'external': [],
                              'post_done': [], 
                              'post_err': [], 
                              'started': []})
        self.fq2a_job.add_dependencies(ended=['job4',])
        self.assertDictEqual(self.fq2a_job.dep,
                             {'done':['job1','job2'],
                              'exit':['job3',],
                              'ended': ['job4',], 
                              'external': [],
                              'post_done': [], 
                              'post_err': [], 
                              'started': []})

    def test_add_dependency_with_dep_str(self):
        """Add dependency, build LSF dependency string.

        """
        self.fq2a_job.add_dependencies(done=['job1', 'job2'],
                                       exit=['job3'])
        self.assertDictEqual(self.fq2a_job.dep, 
                             {'done':['job1','job2'],
                              'exit':['job3',],
                              'ended': [], 
                              'external': [],
                              'post_done': [], 
                              'post_err': [], 
                              'started': []})
        self.fq2a_job.add_dependencies(ended=['job4',], 
                                       dep_str="done||done||ended||exit")
        self.assertDictEqual(self.fq2a_job.dep,
                             {'done':['job1','job2'],
                              'exit':['job3',],
                              'ended': ['job4',], 
                              'external': [],
                              'post_done': [], 
                              'post_err': [], 
                              'started': []})

    def test_show_as_list(self):
        """Method returns cmd and arguments as list to submit to shell.

        Note: list not in order because arguements are stored as a dictionary.

        """
        self.fq2a_job.add_argument('-i', 'input_file.fq')
        self.fq2a_job.add_argument('-o', 'output_file.fa')
        self.assertListEqual(self.fq2a_job.show_as_list(),
                             ['fastq_to_fasta', 
                              '-o', 'output_file.fa',
                              '-i', 'input_file.fq'])

    def test_get_command(self):
        """Method returns cmd and argument as string to submit to shell.

        """
        self.fq2a_job.add_argument('-i', 'input_file.fq')
        self.fq2a_job.add_argument('-o', 'output_file.fa')
        self.assertEqual(self.fq2a_job.get_command(),
                         "fastq_to_fasta -o output_file.fa -i input_file.fq")


class ModuleInitWithParamaters(unittest.TestCase):
    """Test initialization of module when key-word input arguments are not empty.

    """
    def setUp(self):
        """Set up a job initialized with input parameters.

        Job used in class test cases.

        """
        self.fq2a_job = FastqToFasta(name='myFastq2Fasta',
                                     args={'-i': 'input_file.fq',
                                           '-o': 'output_file.fa'},
                                     dep_str='previous_job',
                                     )

    def test_job_init_cmd(self):
        """Module should inherit job and initialize cmd.

        """
        self.assertEqual(self.fq2a_job.cmd, 'fastq_to_fasta')

    def test_job_init_args(self):
        """Module initialized with args, args dictionary must match.

        """
        self.assertDictEqual(self.fq2a_job.args, {'-i': 'input_file.fq', 
                                                  '-o': 'output_file.fa'})

    def test_job_init_name(self):
        """Module init with name, name is initialized value.

        """
        self.assertEqual(self.fq2a_job.name, 'myFastq2Fasta')
        self.assertIsInstance(self.fq2a_job.name, str)

    def test_job_init_dep_str(self):
        """Module dependency string must match initialized dep_str.

        """
        self.assertEqual(self.fq2a_job.dep_str, 'previous_job')

    def test_job_init_dep_at_init(self):
        """Module if dep_string is not empty, attribute True.

        """
        self.assertTrue(self.fq2a_job.dep_str_at_init)

    def test_job_as_string(self):
        """__str__ method returns a command line execution representation.

        """
        job_str = "fastq_to_fasta -o output_file.fa -i input_file.fq"
        self.assertEqual(str(self.fq2a_job), job_str)

    def test_add_argument(self):
        """Method to add arguments to job.

        """
        self.fq2a_job.add_argument('-C', '')
        self.assertDictEqual(self.fq2a_job.args, {'-i': 'input_file.fq',
                                                  '-o': 'output_file.fa',
                                                  '-C': ''})
        job_str = 'fastq_to_fasta -o output_file.fa -i input_file.fq -C'
        self.assertEqual(str(self.fq2a_job), job_str)

