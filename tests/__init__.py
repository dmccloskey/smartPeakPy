#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_smartPeak
----------------------------------

Tests for `smartPeak` module.
"""

from __future__ import absolute_import

from os.path import abspath, dirname, join

try:
    import pytest
    import pytest_benchmark
except ImportError:
    pytest = None

smartPeak_directory = abspath(join(dirname(abspath(__file__)), ".."))
smartPeak_location = abspath(join(smartPeak_directory, "smartPeak"))
data_dir = join(smartPeak_directory, "tests/data", "")
example_dir = join(smartPeak_directory, "examples", "")

# def test_all(args=None):
#     """ alias for running all unit-tests on installed smartPeak
#     """
#     if pytest:
#         args = args if args else []

#         return pytest.main(
#             ['--pyargs', 'smartPeak', '--benchmark-skip', '-v', '-rs'] + args
#         )
#     else:
#         raise ImportError('missing package pytest and pytest_benchmark'
#                           ' required for testing')

def runAllTests():
    from tests.test_core_Utilities import testUtilities
    test = testUtilities()
    test.test_castString()
    test.test_convert_byte2String()
    # test.test_convert_MQQMethod2Feature() # TODO
    test.test_convert_string2Byte()
    test.test_make_osCmd()
    test.test_parse_MQTransitionName()
    test.test_parseString()
    test.test_setParameters()

    from tests.test_io_OpenSwathFeatureXMLToTSV import TestOpenSwathFeatureXMLToTSV
    test = TestOpenSwathFeatureXMLToTSV()
    test.test_get_header()
    test.test_convert_FeatureXMLToTSV()

    # # TODO: update to new pyopenms interface (potential bug?)
    # # File "pyopenms/pyopenms_2.pyx", line 6748, in pyopenms.pyopenms_2.TransformationDescription.setDataPoints (pyopenms/pyopenms_2.cpp:143629)
    # # AssertionError: arg data wrong type
    # from tests.test_pyTOPP_OpenSwathRTNormalizer import TestOpenSwathRTNormalizer
    # test = TestOpenSwathRTNormalizer()
    # test.test_algorithm()

    # # TODO: refactor to C++
    # from tests.test_algorithm_MRMFeatureSelector import TestMRMFeatureSelector
    # test = TestMRMFeatureSelector()
    # test.test_select_MRMFeatures_score()
    # test.test_schedule_MRMFeatures_qmip()

    # # NOTE: requires database settings file
    # from tests.test_data_ReferenceDataMethods import TestReferenceDataMethods
    # test = TestReferenceDataMethods()
    # test.test_getAndProcessReferenceDataSamples()
    # test.test_getAndProcessReferenceDataCalibrators()

    from tests.test_data_DBConnection import TestDBConnection
    test = TestDBConnection()
    test.test_DBConnection()

    from tests.test_data_DBio import TestDBio
    test = TestDBio()
    test.test_convert_list2string()
    test.test_merge_keysAndListOfTuplest()
    test.test_execute_statement()
    test.test_execute_select()

    from tests.test_data_DBTableInterface import TestDBTableInterface
    test = TestDBTableInterface()
    test.test_get_tableName()
    test.test_get_tableColumns()
    test.test_get_tableDataTypes()
    test.test_get_sequenceName()
    test.test_createAndDropTable()
    test.test_alter_table()
    test.test_createAndDropTrigger()
    test.test_insert_row()
    test.test_update_rows()
    test.test_select_rows()

    from tests.test_data_DBTables import TestDBTables
    test = TestDBTables()
    test.test_set_tables()
    test.test_get_table()
    test.test_connect_tables()
    test.test_createAndDrop_tables()

    from tests.test_algorithm_MRMFeatureValidator import TestMRMFeatureValidator
    test = TestMRMFeatureValidator()
    test.test_validate_MRMFeatures()

    from tests.test_io_FileReaderOpenMS import TestFileReaderOpenMS
    test = TestFileReaderOpenMS()
    test.test_load_traML()
    test.test_load_MSExperiment()
    test.test_load_Trafo()
    test.test_load_featureMap()
    test.test_load_quantitationMethods()
    # test.test_load_standardsConcentrations()
    test.test_load_featureFilter()
    test.test_load_featureQC()

    from tests.test_io_FileWriterOpenMS import TestFileWriterOpenMS
    test = TestFileWriterOpenMS()
    test.test_store_featureMap()

    from tests.test_core_RawDataProcessor import TestRawDataProcessor
    test = TestRawDataProcessor()
    test.test_extract_metaData()
    test.test_pickFeatures()
    test.test_filterAndSelect()
    test.test_validateFeatures()
    test.test_quantifyComponents()
    test.test_checkFeatures()
    test.test_processRawData()

    from tests.test_core_SequenceHandler import TestSequenceHandler
    test = TestSequenceHandler()
    test.test_addSampleToSequence()
    test.test_getMetaValue()
    test.test_parse_metaData()
    test.test_addFeatureMapToSequence()
    test.test_getDefaultRawDataProcessingWorkflow()
    test.test_getDefaultSequenceGroupProcessingWorkflow()

    from tests.test_core_SequenceProcessor import TestSequenceProcessor
    test = TestSequenceProcessor()
    test.test_groupSamplesInSequence()
    test.test_addRawDataHandlerToSequence()

    from tests.test_io_SequenceWriter import TestSequenceWriter
    test = TestSequenceWriter()
    test.test_makeDataMatrixFromMetaValue()

    from tests.test_io_SequenceReader import TestSequenceReader
    test = TestSequenceReader()
    test.test_parse_sequenceFile()
    test.test_read_sequenceFile()
    test.test_parse_sequenceParameters()
    test.test_read_sequenceParameters()

    from tests.test_core_SequenceGroupProcessor import TestSequenceGroupProcessor
    test = TestSequenceGroupProcessor()
    test.test_getSampleIndicesBySampleType()
    test.test_optimizeCalibrationCurves()

    from tests.test_main import testMain
    test = testMain()
    test.test_main_LCMS_MRM()
    test.test_main_GCMS_SIM()