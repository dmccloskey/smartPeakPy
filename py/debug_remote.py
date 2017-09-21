#VSCode remote debugging
######
import ptvsd
ptvsd.enable_attach("my_secret", address = ('0.0.0.0', 3000))
#enable the below line of code only if you want the application to wait until the debugger has attached to it
ptvsd.wait_for_attach()
######

from smartPeak.core.__main__ import __main__
m = __main__()

# # Test openSWATH_py
# m.run_openSWATH_validation_py(
#     filename_filenames='/home/user/openMS_MRMworkflow/Algo1Validation/filenames.csv',
#     filename_params='/home/user/openMS_MRMworkflow/Algo1Validation/MRMFeatureFinderScoring_params.csv', #QMIP
#     # filename_params='/home/user/openMS_MRMworkflow/Algo1Validation/MRMFeatureFinderScoring_params_filterControl.csv', #FILTERCONTROL
#     delimiter=','
#     )

# # Test MRMTransitionGroupPicker_py
# m.run_MRMTransitionGroupPicker_py(
#     filename_filenames='/home/user/openMS_MRMworkflow/BloodProject01/BloodProject01_SWATH_filenames.csv',
#     filename_params='/home/user/openMS_MRMworkflow/BloodProject01/BloodProject01_MRMFeatureFinderScoring_params.csv',
#     delimiter=','
#     )

# # Test PeakPickerMRM_py
# m.run_PeakPickerMRM_py(
#     filename_filenames='/home/user/openMS_MRMworkflow/BloodProject01_SWATH_filenames.csv',
#     filename_params='/home/user/openMS_MRMworkflow/BloodProject01/BloodProject01_PeakPickerMRM_params.csv',
#     delimiter=','
#     )

from tests.test_MRMMapper import TestMRMMapper
test = TestMRMMapper()
test.test_algorithm()

# from tests.test_OpenSwathFeatureXMLToTSV import TestOpenSwathFeatureXMLToTSV
# test = TestOpenSwathFeatureXMLToTSV()
# test.test_()

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

# from tests.test_smartPeak_AbsoluteQuantitation_py import TestAbsoluteQuantitation_py
# tabsquant = TestAbsoluteQuantitation_py()
# tabsquant.test_QuantifyComponents(debug = True)
