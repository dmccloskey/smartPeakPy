# -*- coding: utf-8 -*-
from smartPeak.core.smartPeak import smartPeak
from smartPeak.core.smartPeak_i import smartPeak_i
from . import data_dir
from smartPeak.pyTOPP.MRMFeatureFilter import MRMFeatureFilter
from smartPeak.pyTOPP.MRMFeatureSelector import MRMFeatureSelector
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class TestMRMFeatureSelector():
    
    def load_data(self,
        featureXML_i = "features/150601_0_BloodProject01_PLT_QC_Broth-1_1.featureXML",
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

    def test_schedule_MRMFeatures_qmip(self):  
        self.load_data()    
        featureFilter = MRMFeatureFilter()
        output_filtered = featureFilter.filter_MRMFeatures(
            self.featureMap,
            self.targeted,
            self.params["MRMFeatureFilter.filter_MRMFeatures"])   
        featureSelector = MRMFeatureSelector()         
        output_selected = featureSelector.schedule_MRMFeatures_qmip(
            features = output_filtered,
            tr_expected = [],    
            targeted = self.targeted,
            schedule_criteria = self.params["MRMFeatureSelector.schedule_MRMFeatures_qmip"])
        assert(output_selected[0].getSubordinates()[0].getMetaValue("peak_apex_int") == 262623.5)
        assert(output_selected[0].getSubordinates()[0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
        assert(output_selected[0].getSubordinates()[0].getRT() == 15.8944563381195)
        assert(output_selected[50].getSubordinates()[0].getMetaValue("peak_apex_int") == 13919.0)
        assert(output_selected[50].getSubordinates()[0].getMetaValue("native_id") == b'glyclt.glyclt_1.Heavy')
        assert(output_selected[50].getSubordinates()[0].getRT() == 3.14837637761434)
    
    def test_select_MRMFeatures_score(self):  
        self.load_data()    
        featureFilter = MRMFeatureFilter()
        output_filtered = featureFilter.filter_MRMFeatures(
            self.featureMap,
            self.targeted,
            self.params["MRMFeatureFilter.filter_MRMFeatures"])   
        featureSelector = MRMFeatureSelector()  
        output_selected = featureSelector.select_MRMFeatures_score(
            output_filtered,
            self.params["MRMFeatureSelector.select_MRMFeatures_score"])
        assert(output_selected[0].getSubordinates()[0].getMetaValue("peak_apex_int") == 1946.5)
        assert(output_selected[0].getSubordinates()[0].getMetaValue("native_id") == b'23dpg.23dpg_1.Light')
        assert(output_selected[0].getSubordinates()[0].getRT() == 16.4121927001953)
        assert(output_selected[50].getSubordinates()[0].getMetaValue("peak_apex_int") == 922.0)
        assert(output_selected[50].getSubordinates()[0].getMetaValue("native_id") == b'f6p.f6p_1.Light')
        assert(output_selected[50].getSubordinates()[0].getRT() == 8.0184300549825)