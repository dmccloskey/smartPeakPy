# -*- coding: utf-8 -*-
from smartPeak.core.smartPeak import smartPeak
from smartPeak.core.smartPeak_i import smartPeak_i
from smartPeak.core.smartPeak_o import smartPeak_o
from smartPeak.core.smartPeak_openSWATH_py import smartPeak_openSWATH_py
from smartPeak.core.smartPeak_AbsoluteQuantitation_py import smartPeak_AbsoluteQuantitation_py
from . import data_dir
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class TestAbsoluteQuantitation_py():
    
    def test_QuantifyComponents(self,
        filename_filenames = "BloodProject01_SWATH_filenames.csv",
        filename_params = None,
        delimiter = ',',
        debug = True):
        """Test and Run the AbsoluteQuantitation python pipeline
        
        Args:
            filename_filenames (str): name of the workflow files
            filename_params (str): name of the worflow parameter file
            delimiter (str): .csv file delimiter
            debug (bool): if True, assertions are made on default data
            verbose (bool): print command line statements to stdout,
            
        """
        filename_filenames = data_dir + "/" + filename_filenames

        skipped_samples = []
        output = []

        AbsoluteQuantitation_py = smartPeak_AbsoluteQuantitation_py()
        openSWATH_py = smartPeak_openSWATH_py()
        smartpeak_i = smartPeak_i()
        smartpeak_i.read_pythonParams(filename_filenames,delimiter)
        filenames = smartpeak_i.getData()
        smartpeak_i.clear_data()
        # smartpeak_i.read_openMSParams(filename_params,delimiter)
        # params = smartpeak_i.getData()
        # smartpeak_i.clear_data()
        for filename in filenames:
            for sample,v in filename.items():
                print("processing sample "+ sample)
                try:
                    # dynamically make the filenames
                    quantitationMethods_csv_i = '''%s/%s'''%(data_dir,v["quantitationMethods_csv_i"])
                    featureXML_o = '''%s/quantitation/%s.featureXML'''%(data_dir,sample) 
                    feature_csv_o = '''%s/quantitation/%s.csv'''%(data_dir,sample)
                    featureXML_i = '''%s/features/%s.featureXML'''%(data_dir,sample) 
                    feature_csv_i = '''%s/features/%s.csv'''%(data_dir,sample)
                    # load the quantitation method
                    AbsoluteQuantitation_py.load_quantitationMethods(
                        {'quantitationMethods_csv_i':quantitationMethods_csv_i})
                    # quantify the components
                    AbsoluteQuantitation_py.load_unknowns(
                        {'featureXML_i':[featureXML_i]})
                    AbsoluteQuantitation_py.quantifyComponents()
                    # store
                    openSWATH_py.store_featureMap(
                        {'featureXML_o':[featureXML_o]})
                except Exception as e:
                    print(e)
                    skipped_samples.append({'sample_name':sample,
                        'error_message':e})
                # manual clear data for the next iteration
                openSWATH_py.clear_data()
        if not debug:
            if skipped_samples:
                smartpeak_o = smartPeak_o(skipped_samples)
                skippedSamples_csv_i = '''%s/mzML/skippedSamples.csv'''%(data_dir)
                smartpeak_o.write_dict2csv(skippedSamples_csv_i)
            return output

    def test_OptimizeCalibrators(self,
        filenames_I):
        """Test the optimization of Calibrators"""

        spaq = smartPeak_AbsoluteQuantitation_py()
        spaq.load_quantitationStandards(
            filenames_I
        )
        #spaq.()
        spaq.store_quantitationMethods(
            filenames_I
        )