# coding: utf-8
from .smartPeak_openSWATH_cmd import smartPeak_openSWATH_cmd
from .smartPeak_openSWATH_py import smartPeak_openSWATH_py
from .smartPeak_i import smartPeak_i

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
            filename_filenames,
            filename_params,
            delimiter = ','
            ):
        """Run the openSWATH python pipeline
        
        Args:
            filename (str): name of the workflow parameter filename
            verbose (bool): print command line statements to stdout
            
        Eamples:
            
        """
        from .test_smartPeak import test_smartPeak
        tests = test_smartPeak()
        tests.test_parseString()

        openSWATH_py = smartPeak_openSWATH_py()
        smartpeak_i = smartPeak_i();
        smartpeak_i.read_pythonParams(filename_filenames,delimiter)
        filenames = smartpeak_i.getData();
        smartpeak_i.clear_data();
        smartpeak_i.read_openMSParams(filename_params,delimiter);
        params = smartpeak_i.getData();
        smartpeak_i.clear_data();
        for filename in filenames:
            for sample,v in filename.items():
                print("processing sample "+ sample)
                openSWATH_py.openSWATH_py(v,params['MRMFeatureFinderScoring'])
