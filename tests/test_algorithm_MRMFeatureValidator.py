# -*- coding: utf-8 -*-
from smartPeak.core.smartPeak import smartPeak
from smartPeak.io.FileReader import FileReader
from . import data_dir
from smartPeak.algorithm.MRMFeatureValidator import MRMFeatureValidator
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class TestMRMFeatureValidator():
    
    def load_data(
        self,
        featureXML_i="features/test_2.featureXML",
        referenceData_csv_i="referenceData_1.csv",
        filename_params="test_pyTOPP_MRMFeatureValidator_params.csv"
    ):
        """load the test data"""                   

        # load the reference data
        referenceData_csv_i = data_dir + "/" + referenceData_csv_i
        self.reference_data = []
        if referenceData_csv_i is not None:            
            smartpeak_i = FileReader()
            smartpeak_i.read_csv(referenceData_csv_i)
            self.reference_data = smartpeak_i.getData()
            smartpeak_i.clear_data()

        # load the featureMap
        featureXML_i = data_dir + "/" + featureXML_i    
        featurexml = pyopenms.FeatureXMLFile()
        self.featureMap = pyopenms.FeatureMap()
        if featureXML_i is not None:
            featurexml.load(featureXML_i.encode('utf-8'), self.featureMap)
        
        # load the parameters
        filename_params = data_dir + "/" + filename_params
        smartpeak_i = FileReader()
        smartpeak_i.read_openMSParams(filename_params, ",")
        self.params = smartpeak_i.getData()
        smartpeak_i.clear_data()

    def test_validate_MRMFeatures(self):    
        self.load_data()    
        featureValidator= MRMFeatureValidator()
        features_mapped,validation_metrics = featureValidator.validate_MRMFeatures(
            reference_data=self.reference_data,
            features=self.featureMap,
            Tr_window=float(self.params[
                'MRMFeatureValidator.validate_MRMFeatures'][0]['value'])
            )
        # refactor to us pytest.approx
        assert(validation_metrics["accuracy"] == 0.98709677419354835)