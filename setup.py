"""tfpipe setup script. """

from distutils.core import setup

setup(
    name='tfpipe',
    version='1.0.4',
    author='Karl Eklund',
    author_email='keklund@email.unc.edu',
    packages=['tfpipe', 
              'tfpipe.utils',
              'tfpipe.modules', 
              'tfpipe.modules.cli',
              'tfpipe.modules.fseq',
              'tfpipe.modules.gmap',
              'tfpipe.modules.mach',
              'tfpipe.modules.blast',
              'tfpipe.modules.plink',
              'tfpipe.modules.qiime',
              'tfpipe.modules.bowtie',
              'tfpipe.modules.fastqc',
              'tfpipe.modules.picard',
              'tfpipe.modules.tophat',
              'tfpipe.modules.dfilter',
              'tfpipe.modules.tagdust',
              'tfpipe.modules.abundant',
              'tfpipe.modules.bamtools',
              'tfpipe.modules.bedtools',
              'tfpipe.modules.samtools',
              'tfpipe.modules.bcl2fastq',
              'tfpipe.modules.blacklist',
              'tfpipe.modules.cufflinks',
              'tfpipe.modules.bcl2fastq2',
              'tfpipe.modules.sratoolkit',
              'tfpipe.modules.fastx_toolkit',
              'tfpipe.modules.cutadapt',
              'tfpipe.modules.star',
              'tfpipe.modules.rsem',
              'tfpipe.modules.python',
              'tfpipe.pipeline',],
    scripts=[#'bin/tfpipe_run',
             'examples/localhost.py',
             'examples/kure.py'],
    url='http://fureylab.web.unc.edu',
    license='LICENSE.txt',
    description='Terry Furey Lab Pipeline',
    long_description=open('README.txt', 'r').read(),
)

#    install_requires=[],
