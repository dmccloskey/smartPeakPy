# -*- coding: utf-8 -*-
# modules
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS
from smartPeak.core.SampleHandler import SampleHandler
from smartPeak.io.FileWriterOpenMS import FileWriterOpenMS
from . import data_dir


class TestFileWriterOpenMS():
    """tests for FileReaderOpenMS
    """

    def test_store_featureMap(self):
        sampleHandler = SampleHandler()
        fileReaderOpenMS = FileReaderOpenMS()
        fileWriterOpenMS = FileWriterOpenMS()        

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_1") 
        fileReaderOpenMS.load_featureMap(sampleHandler, {'featureXML_i': featureXML_o})

        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(sampleHandler, {'traML_csv_i': traML_csv_i})

        # missing meta data in .featureXML
        sampleHandler.meta_data = {}
        sampleHandler.meta_data['sample_name'] = "150601_0_BloodProject01_PLT_QC_Broth-1"
        sampleHandler.meta_data['filename'] = "/home/user/code/tests/data//mzML/mzML_1.mzML"

        # store
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_1") 
        feature_csv_o = '''%s/features/%s.csv''' % (data_dir, "test_1")
        fileWriterOpenMS.store_featureMap(sampleHandler, {
            'featureXML_o': featureXML_o,
            'feature_csv_o': feature_csv_o})