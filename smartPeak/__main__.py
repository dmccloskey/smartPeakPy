# coding: utf-8
from .smartPeak_openSWATH_cmd import smartPeak_openSWATH_cmd
from .smartPeak_openSWATH_py import smartPeak_openSWATH_py

class __main__():
    def run_openSWATH_cmd(
            self,
            filename,
            verbose=True):
        """Run the openSWATH commandline pipeline
        
        Args:
            filename (str): name of the workflow parameter filename
            verbose (bool): print command line statements to stdout
            
        Eamples:        
            from smartPeak.__main__ import __main__
            m = __main__()    
            filename='C:/Users/domccl/Dropbox (UCSD SBRG)/Project_FastPeak/openMS_MRMworkflow/openSWATH_cmd_params.csv',
            filename='/home/user/openMS_MRMworkflow/openSWATH_cmd_params.csv'
            m.run_openSWATH_cmd(filename);
            
        """
        openSWATH_cmd = smartPeak_openSWATH_cmd()
        openSWATH_cmd.read_openSWATH_cmd_params(filename)
        openSWATH_cmd.openSWATH_cmd(verbose_I=verbose)

    def run_openSWATH_py(
            self,
            ):
        """Run the openSWATH python pipeline
        
        Args:
            filename (str): name of the workflow parameter filename
            verbose (bool): print command line statements to stdout
            
        Eamples:
            
        """
        openSWATH_py = smartPeak_openSWATH_py()
        #openSWATH_py.read_openSWATH_cmd_params(filename)
        openSWATH_py.openSWATH_py()
