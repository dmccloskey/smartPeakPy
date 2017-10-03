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

# from tests import runAllTests
# runAllTests()

from tests.test_smartPeak_AbsoluteQuantitation_py import TestAbsoluteQuantitation_py
test = TestAbsoluteQuantitation_py()
test.test_QuantifyComponents(debug = True)

# from tests.test_smartPeak_openSWATH_py import TestSmartPeakOpenSWATH_py
# test = TestSmartPeakOpenSWATH_py()
# test.test_openSWATH_py(
#     # filename_filenames='/home/user/openMS_MRMworkflow/Algo1Validation/filenames.csv',
#     # filename_params='/home/user/openMS_MRMworkflow/Algo1Validation/MRMFeatureFinderScoring_params.csv', #QMIP
#     delimiter=',',
#     debug = False)


###TESTING:
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
