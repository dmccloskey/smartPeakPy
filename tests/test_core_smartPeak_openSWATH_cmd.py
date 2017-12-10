# -*- coding: utf-8 -*-
# utilities
import copy
# modules
from smartPeak.core.smartPeak_openSWATH_cmd import smartPeak_openSWATH_cmd
from . import data_dir


class test_smartPeak_openSWATH_cmd():
    """tests for smartPeak_openSWATH_cmd"""
    
    # # TODO
    # def run_openSWATH_cmd(
    #         self,
    #         filename,
    #         verbose=True):
    #     """Run the openSWATH commandline pipeline
        
    #     Args:
    #         filename (str): name of the workflow parameter filename
    #         verbose (bool): print command line statements to stdout
            
    #     Eamples:        
    #         from smartPeak.__main__ import __main__
    #         m = __main__()    
    #         filename='C:/Users/domccl/Dropbox (UCSD SBRG)/
    #             Project_FastPeak/openMS_MRMworkflow/openSWATH_cmd_params.csv',
    #         filename='/home/user/openMS_MRMworkflow/openSWATH_cmd_params.csv'
    #         m.run_openSWATH_cmd(filename);
            
    #     """
    #     openSWATH_cmd = smartPeak_openSWATH_cmd()
    #     openSWATH_cmd.read_openSWATH_cmd_params(filename)
    #     openSWATH_cmd.openSWATH_cmd(verbose_I=verbose)

    # def test_openSWATH_cmd(self):
    #     """Test openSWATH_cmd"""

    #     # filename='/home/user/openMS_MRMworkflow/openSWATH_cmd_params_QC1.csv'
    #     filename = '''/home/user/openMS_MRMworkflow/\
    #         openSWATH_cmd_params_QC1_FeatureXML2TSV.csv'''
    #     self.run_openSWATH_cmd(filename)

    #     # TODO: read in resulting file and compare to test file
