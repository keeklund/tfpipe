""" """
from tfpipe.base import Job

class BedTools(Job):
    """

    """
    _module = 'bedtools/2.17.0'


class BamToBed(BedTools):
    """

    """
    _cmd = 'bedtools bamtobed '


class BedToBam(BedTools):
    """

    """
    _cmd = 'bedtools bedtobam '


class Intersect(BedTools):
    """

    """
    _cmd = 'bedtools intersect '


