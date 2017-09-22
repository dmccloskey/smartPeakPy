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
    from tests.test_MRMMapper import TestMRMMapper
    test = TestMRMMapper()
    test.test_algorithm()

    from tests.test_OpenSwathFeatureXMLToTSV import TestOpenSwathFeatureXMLToTSV
    test = TestOpenSwathFeatureXMLToTSV()
    test.test_get_header()
    test.test_convert_FeatureXMLToTSV()

    from tests.test_OpenSwathRTNormalizer import TestOpenSwathRTNormalizer
    test = TestOpenSwathRTNormalizer()
    test.test_algorithm()

    from tests.test_MRMFeatureFilter import TestMRMFeatureFilter
    test = TestMRMFeatureFilter()
    test.test_filter_MRMFeatures()

    from tests.test_MRMFeatureSelector import TestMRMFeatureSelector
    test = TestMRMFeatureSelector()
    test.test_schedule_MRMFeatures_qmip()
    test.test_select_MRMFeatures_score()

    from tests.test_ReferenceDataMethods import TestReferenceDataMethods
    test = TestReferenceDataMethods()
    test.test_getAndProcessReferenceDataSamples()
    test.test_getAndProcessReferenceDataCalibrators()

    from tests.test_MRMFeatureValidator import TestMRMFeatureValidator
    test = TestMRMFeatureValidator()
    test.test_validate_MRMFeatures()

    from tests.test_smartPeak_openSWATH_py import TestSmartPeakOpenSWATH_py
    test = TestSmartPeakOpenSWATH_py()
    test.test_openSWATH_py(debug = True)
    test.test_validate_openSWATH(debug = True)