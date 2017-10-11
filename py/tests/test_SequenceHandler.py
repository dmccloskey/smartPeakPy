# -*- coding: utf-8 -*-
from smartPeak.core.smartPeak import smartPeak
from smartPeak.core.smartPeak_i import smartPeak_i
from . import data_dir
from smartPeak.pyTOPP.SequenceHandler import SequenceHandler
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class TestSequenceHandler():
    
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

    def test_addSampleToSequence(self):
        seqhandler = SequenceHandler()

        # test data
        meta_data1 = {'filename':'file1','sample_name':'sample1'}
        featuremap1 = None
        
        meta_data2 = {'filename':'file2','sample_name':'sample2'}
        featuremap2 = None
        
        meta_data3 = {'filename':'file3','sample_name':'sample3'}
        featuremap3 = None

        # add the injections to the sequence
        seqhandler.addSampleToSequence(meta_data1, featuremap1)
        seqhandler.addSampleToSequence(meta_data2, featuremap2)
        seqhandler.addSampleToSequence(meta_data3, featuremap3)

        assert(len(seqhandler.sequence) == 3)
        assert(seqhandler.sequence_index[1] == 'sample2')

    def test_getMetaValue(self):
        self.load_data()    
        seqhandler = SequenceHandler()

        feature, subordinate, meta_value = None, None, None
        result = seqhandler.getMetaValue(feature, subordinate, meta_value)

        assert(result == 10.0) #TODO

    def test_makeDataMatrixFromMetaValue(self):  
        self.load_data()    
        seqhandler = SequenceHandler()

        columns, rows, data = seqhandler.makeDataMatrixFromMetaValue(
            meta_values = ["calculated_concentration"], sample_types = ["Unknown"])