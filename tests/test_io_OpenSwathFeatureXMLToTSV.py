# -*- coding: utf-8 -*-
from smartPeak.io.FileReader import FileReader
from . import data_dir
from smartPeak.io.OpenSwathFeatureXMLToTSV import OpenSwathFeatureXMLToTSV
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class TestOpenSwathFeatureXMLToTSV():
    """TODO:

    1. make MRMFeatureFinderScoring_params_I
    2. add assertions
    """
    
    def load_data(
        self,
        featureXML_i="features/test_1_algorithm_MRMFeatureValidator.featureXML",
        traML_csv_i="traML_1.csv"
    ):
        """load the test data"""        

        # load targeted experiment
        traML_csv_i = data_dir + "/" + traML_csv_i
        self.targeted = pyopenms.TargetedExperiment()  # must use "PeptideSequence"
        if traML_csv_i is not None:
            tramlfile = pyopenms.TransitionTSVFile()
            tramlfile.convertTSVToTargetedExperiment(
                traML_csv_i.encode('utf-8'), 21, self.targeted)

        # load the featureMap
        featureXML_i = data_dir + "/" + featureXML_i     
        featurexml = pyopenms.FeatureXMLFile()
        self.featureMap = pyopenms.FeatureMap()
        if featureXML_i is not None:
            featurexml.load(featureXML_i.encode('utf-8'), self.featureMap)
    
    def test_get_header(self):
        self.load_data()
        featurescsv = OpenSwathFeatureXMLToTSV()
        header, keys, keys_subordinates = featurescsv.get_header(self.featureMap)
        assert(header[0] == 'transition_group_id')
        # assert(header[17] == 'peak_apices_sum')
        assert(keys[0] == b'potentialOutlier')
        # assert(keys[17] == b'nr_peaks')
        assert(keys_subordinates[0] == b'MZ')
        # assert(keys_subordinates[len(keys_subordinates)-1] == b'FeatureLevel')
    
    def test_convert_FeatureXMLToTSV(self):
        self.load_data()
        featurescsv = OpenSwathFeatureXMLToTSV()
        header, rows_O = featurescsv.convert_FeatureXMLToTSV(
            self.featureMap, self.targeted, run_id='run0', filename='run0.FeatureXML')
        assert(header[0] == 'transition_group_id')
        assert(header[17] == 'peak_apices_sum')
        assert(rows_O[0]['PeptideRef'] == '23dpg')
        assert(rows_O[0]['native_id'] == '23dpg.23dpg_1.Heavy')