# -*- coding: utf-8 -*-
from smartPeak.core.smartPeak import smartPeak
from smartPeak.core.smartPeak_i import smartPeak_i
from . import data_dir
from smartPeak.pyTOPP.OpenSwathFeatureXMLToTSV import OpenSwathFeatureXMLToTSV
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class TestOpenSwathFeatureXMLToTSV():
    """TODO:

    1. make MRMFeatureFinderScoring_params_I
    2. add assertions
    """
    
    def load_data(self,
        mzML_feature_i = "150601_0_BloodProject01_PLT_QC_Broth-1.mzML",
        traML_csv_i = "BloodProject01_SWATH.csv"):
        """load the test data"""        

        # load targeted experiment
        traML_csv_i = data_dir + "/" + traML_csv_i
        self.targeted = pyopenms.TargetedExperiment() #must use "PeptideSequence"
        if not traML_csv_i is None:
            tramlfile = pyopenms.TransitionTSVReader()
            tramlfile.convertTSVToTargetedExperiment(traML_csv_i.encode('utf-8'),21,self.targeted)

        # load chromatograms
        mzML_feature_i = data_dir + "/" + mzML_feature_i
        self.chromatograms = pyopenms.MSExperiment()
        if not mzML_feature_i is None:
            fh = pyopenms.FileHandler()
            fh.loadExperiment(mzML_feature_i.encode('utf-8'), self.chromatograms)
    
    def test_get_header(self,
        ):
        self.load_data()

        #TODO: assert()
    
    def test_convert_FeatureXMLToTSV(self,
        ):
        self.load_data()

        #TODO: assert()