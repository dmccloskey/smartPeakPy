# coding: utf-8
from .smartPeak_openSWATH_cmd import smartPeak_openSWATH_cmd

class __main__():
    def run_openSWATH_cmd(
            self,
            filename='C:/Users/domccl/Dropbox (UCSD SBRG)/Project_FastPeak/openMS_MRMworkflow/openSWATH_cmd_params.csv',
            verbose=True):
        """ """
        openSWATH_cmd = smartPeak_openSWATH_cmd()
        openSWATH_cmd.read_openSWATH_cmd_params(filename)
        openSWATH_cmd.openSWATH_cmd(verbose_I=verbose)
