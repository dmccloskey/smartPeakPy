# -*- coding: utf-8 -*-
# modules
from smartPeak.io.FileReader import FileReader
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS
from smartPeak.io.FileWriterOpenMS import FileWriterOpenMS
from smartPeak.core.RawDataHandler import RawDataHandler
from smartPeak.core.RawDataProcessor import RawDataProcessor
from smartPeak.core.SequenceGroupProcessor import SequenceGroupProcessor
from smartPeak.core.SequenceGroupHandler import SequenceGroupHandler
from . import data_dir


class TestSequenceGroupProcessor():
    """tests for SequenceGroupProcessor class
    """

    def test_extract_metaData(self):
        rawDataHandler = RawDataHandler()
        rawDataProcessor = RawDataProcessor()
        fileReaderOpenMS = FileReaderOpenMS()