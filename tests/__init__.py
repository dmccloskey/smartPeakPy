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
    from tests.test_pyTOPP_OpenSwathFeatureXMLToTSV import TestOpenSwathFeatureXMLToTSV
    test = TestOpenSwathFeatureXMLToTSV()
    test.test_get_header()
    test.test_convert_FeatureXMLToTSV()

    ##TODO: update to new pyopenms interface (potential bug?)
    ## File "pyopenms/pyopenms_2.pyx", line 6748, in pyopenms.pyopenms_2.TransformationDescription.setDataPoints (pyopenms/pyopenms_2.cpp:143629)
    ## AssertionError: arg data wrong type
    # from tests.test_pyTOPP_OpenSwathRTNormalizer import TestOpenSwathRTNormalizer
    # test = TestOpenSwathRTNormalizer()
    # test.test_algorithm()

    # TODO: broke
    # from tests.test_pyTOPP_MRMFeatureSelector import TestMRMFeatureSelector
    # test = TestMRMFeatureSelector()
    # test.test_select_MRMFeatures_score()
    # test.test_schedule_MRMFeatures_qmip()

    # TODO: broke
    # #NOTE: requires database settings file
    # from tests.test_data_ReferenceDataMethods import TestReferenceDataMethods
    # test = TestReferenceDataMethods()
    # test.test_getAndProcessReferenceDataSamples()
    # test.test_getAndProcessReferenceDataCalibrators()

    from tests.test_pyTOPP_MRMFeatureValidator import TestMRMFeatureValidator
    test = TestMRMFeatureValidator()
    test.test_validate_MRMFeatures()

    from tests.test_core_smartPeak_openSWATH_py import TestSmartPeakOpenSWATH_py
    test = TestSmartPeakOpenSWATH_py()
    test.test_openSWATH_py(debug = True)
    test.test_validate_openSWATH(debug = True)

    from tests.test_core_smartPeak_AbsoluteQuantitation_py import TestAbsoluteQuantitation_py
    test = TestAbsoluteQuantitation_py()
    test.test_QuantifyComponents(debug = True)

    from tests.test_pyTOPP_SequenceHandler import TestSequenceHandler
    test = TestSequenceHandler()
    test.test_addSampleToSequence()
    test.test_getMetaValue()
    test.test_makeDataMatrixFromMetaValue()
