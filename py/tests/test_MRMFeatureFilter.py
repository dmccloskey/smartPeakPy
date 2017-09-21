# -*- coding: utf-8 -*-
from smartPeak.core.smartPeak import smartPeak
from smartPeak.core.smartPeak_i import smartPeak_i
from . import data_dir
from smartPeak.pyTOPP.MRMFeatureFilter import MRMFeatureFilter
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class TestMRMFeatureFilter():
    
    def load_data(self,
        featureXML_i = "150601_0_BloodProject01_PLT_QC_Broth-1.featureXML",
        traML_csv_i = "BloodProject01_SWATH.csv",
        filename_params = "BloodProject01_MRMFeatureFinderScoring_params.csv"):
        """load the test data"""                   

        # load targeted experiment
        traML_csv_i = data_dir + "/" + traML_csv_i
        self.targeted = pyopenms.TargetedExperiment() #must use "PeptideSequence"
        if not traML_csv_i is None:
            tramlfile = pyopenms.TransitionTSVReader()
            tramlfile.convertTSVToTargetedExperiment(traML_csv_i.encode('utf-8'),21,self.targeted)

        # load the featureMap
        featureXML_i = data_dir + "/" + featureXML_i       

        # Store outfile as featureXML    
        featurexml = pyopenms.FeatureXMLFile()
        self.featureMap = pyopenms.FeatureMap()
        if not featureXML_i is None:
            featurexml.load(featureXML_i.encode('utf-8'), self.featureMap)
        
        # load the parameters
        filename_params = data_dir + "/" + filename_params
        smartpeak_i = smartPeak_i()
        smartpeak_i.read_openMSParams(filename_params,",")
        self.params = smartpeak_i.getData()
        smartpeak_i.clear_data()

    def test_filter_MRMFeatures(self):  
        self.load_data()    
        featureFilter = MRMFeatureFilter()
        output_filtered = featureFilter.filter_MRMFeatures(
            self.featureMap,
            self.targeted,
            self.params["MRMFeatureFilter.filter_MRMFeatures"])
        assert(output_filtered[0].getSubordinates()[0].getMetaValue("peak_apex_int") == 262623.5)
        assert(output_filtered[0].getSubordinates()[0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
        assert(output_filtered[0].getSubordinates()[0].getRT() == 15.894456338119507)
        assert(output_filtered[50].getSubordinates()[0].getMetaValue("peak_apex_int") == 1045662.0)
        assert(output_filtered[50].getSubordinates()[0].getMetaValue("native_id") == b'asp-L.asp-L_1.Heavy')
        assert(output_filtered[50].getSubordinates()[0].getRT() == 2.6657843421936036)