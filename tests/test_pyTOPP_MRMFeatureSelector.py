# -*- coding: utf-8 -*-
from smartPeak.core.smartPeak import smartPeak
from smartPeak.core.smartPeak_i import smartPeak_i
from . import data_dir
from smartPeak.pyTOPP.MRMFeatureSelector import MRMFeatureSelector
import copy
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class TestMRMFeatureSelector():
    
    def load_data(
        self,
        featureXML_i="features/150601_0_BloodProject01_PLT_QC_Broth-1_1.featureXML",
        traML_csv_i="BloodProject01_SWATH.csv",
        mrmfeatureqcs_csv_i="test_pyTOPP_MRMFeatureQCFile.csv",
        filename_params="test_pyTOPP_MRMFeatureSelector_params.csv"
    ):
        """load the test data"""                   

        # load targeted experiment
        traML_csv_i = data_dir + "/" + traML_csv_i
        self.targeted = pyopenms.TargetedExperiment()  # must use "PeptideSequence"
        if traML_csv_i is not None:
            tramlfile = pyopenms.TransitionTSVReader()
            tramlfile.convertTSVToTargetedExperiment(
                traML_csv_i.encode('utf-8'), 21, self.targeted)

        # load the featureMap
        featureXML_i = data_dir + "/" + featureXML_i    
        featurexml = pyopenms.FeatureXMLFile()
        self.featureMap = pyopenms.FeatureMap()
        if featureXML_i is not None:
            featurexml.load(featureXML_i.encode('utf-8'), self.featureMap)
        
        # load the parameters
        filename_params = data_dir + "/" + filename_params
        smartpeak_i = smartPeak_i()
        smartpeak_i.read_openMSParams(filename_params, ",")
        self.params = smartpeak_i.getData()
        smartpeak_i.clear_data()

        # set up MRMFeatureFilter and parse the MRMFeatureFilter params
        featureFilter = pyopenms.MRMFeatureFilter()
        parameters = featureFilter.getParameters()
        smartpeak = smartPeak()
        parameters = smartpeak.updateParameters(
            parameters,
            self.params["MRMFeatureFilter.filter_MRMFeatures"],
            )
        featureFilter.setParameters(parameters) 

        # read in the parameters for the MRMFeatureQC
        mrmfeatureqcs_csv_i = data_dir + "/" + mrmfeatureqcs_csv_i
        featureQC = pyopenms.MRMFeatureQC()
        featureQCFile = pyopenms.MRMFeatureQCFile()
        featureQCFile.load(mrmfeatureqcs_csv_i.encode('utf-8'), featureQC)
        self.featureQC = featureQC  

    def test_schedule_MRMFeatures_qmip(self):  
        self.load_data()    

        featureFilter = pyopenms.MRMFeatureFilter()
        output_filtered = copy.copy(self.featureMap)
        featureFilter.FilterFeatureMap(
            output_filtered,
            self.featureQC,
            self.targeted)

        featureSelector = MRMFeatureSelector()         
        output_selected = featureSelector.schedule_MRMFeatures_qmip(
            features=output_filtered,
            tr_expected=[],    
            targeted=self.targeted,
            schedule_criteria=self.params["MRMFeatureSelector.schedule_MRMFeatures_qmip"],
            score_weights=self.params["MRMFeatureSelector.select_MRMFeatures_qmip"])
        assert(output_selected[0].getSubordinates()[0].getMetaValue(
            "peak_apex_int") == 262623.5)
        assert(output_selected[0].getSubordinates()[0].getMetaValue(
            "native_id") == b'23dpg.23dpg_1.Heavy')
        assert(output_selected[0].getSubordinates()[0].getRT() == 15.8944563381195)
        assert(output_selected[50].getSubordinates()[0].getMetaValue(
            "peak_apex_int") == 1080.0)
        assert(output_selected[50].getSubordinates()[0].getMetaValue(
            "native_id") == b'oxa.oxa_1.Heavy')
        assert(output_selected[50].getSubordinates()[0].getRT() == 13.4963475631714)
    
    def test_select_MRMFeatures_score(self):  
        self.load_data()       

        featureFilter = pyopenms.MRMFeatureFilter()
        output_filtered = copy.copy(self.featureMap)
        featureFilter.FilterFeatureMap(
            output_filtered,
            self.featureQC,
            self.targeted)  
        featureSelector = MRMFeatureSelector()  
        # # TODO: pyopenms.FeatureXMLFile().store(
        #   "tests/data/150601_0_BloodProject01_PLT_QC_Broth-1_2.featureXML".encode(
        #       'utf-8'), output_filtered)
        # then use 150601_0_BloodProject01_PLT_QC_Broth-1_2.featureXML 
        # instead of 150601_0_BloodProject01_PLT_QC_Broth-1_1.featureXML
        output_selected = featureSelector.select_MRMFeatures_score(
            output_filtered,
            self.params["MRMFeatureSelector.select_MRMFeatures_score"])
        assert(output_selected[0].getSubordinates()[0].getMetaValue(
            "peak_apex_int") == 0.0)
        assert(output_selected[0].getSubordinates()[0].getMetaValue(
            "native_id") == b'23dpg.23dpg_1.Heavy')
        assert(output_selected[0].getSubordinates()[0].getRT() == 17.2147079447428)
        assert(output_selected[50].getSubordinates()[0].getMetaValue(
            "peak_apex_int") == 0.0)
        assert(output_selected[50].getSubordinates()[0].getMetaValue(
            "native_id") == b'f1p.f1p_1.Heavy')
        assert(output_selected[50].getSubordinates()[0].getRT() == 13.4859151489258)