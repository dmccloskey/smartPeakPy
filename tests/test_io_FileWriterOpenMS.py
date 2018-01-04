# -*- coding: utf-8 -*-
# modules
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS
from smartPeak.core.SampleHandler import SampleHandler
from smartPeak.io.FileWriterOpenMS import FileWriterOpenMS
from smartPeak.core.SampleProcessor import SampleProcessor
from . import data_dir


class TestFileWriterOpenMS():
    """tests for FileReaderOpenMS
    """

    def test_store_featureMap(self):
        sampleHandler = SampleHandler()
        sampleProcessor = SampleProcessor()
        fileReaderOpenMS = FileReaderOpenMS()
        fileWriterOpenMS = FileWriterOpenMS()        

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_1") 
        fileReaderOpenMS.load_featureMap(sampleHandler, {'featureXML_i': featureXML_o})
        
        sampleProcessor.extract_metaData(sampleHandler)

        # store
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_1") 
        feature_csv_o = '''%s/features/%s.csv''' % (data_dir, "test_1")
        fileWriterOpenMS.store_featureMap(sampleHandler, {
            'featureXML_o': featureXML_o,
            'feature_csv_o': feature_csv_o})