#VSCode remote debugging
######
import ptvsd
ptvsd.enable_attach("my_secret", address = ('0.0.0.0', 3000))
#enable the below line of code only if you want the application to wait until the debugger has attached to it
ptvsd.wait_for_attach()
######

from smartPeak.core.__main__ import __main__
m = __main__()


# LCMS_MRM (TODO)
m.run_AbsoluteQuantitation_py(
    filename_filenames='/home/user/openMS_MRMworkflow/LCMS_MRM/filenames.csv',
    filename_params='/home/user/openMS_MRMworkflow/LCMS_SRM/MRMFeatureFinderScoring_params.csv',
    delimiter=',',
    )

# # GCMS_SRM
# m.run_AbsoluteQuantitation_py(
#     filename_filenames='/home/user/openMS_MRMworkflow/GCMS_SRM/filenames.csv',
#     filename_params='/home/user/openMS_MRMworkflow/GCMS_SRM/MRMFeatureFinderScoring_params.csv',
#     delimiter=',',
#     )

# # GCMS_fullScan
# m.run_AbsoluteQuantitation_py(
#     filename_filenames='/home/user/openMS_MRMworkflow/GCMS_fullScan/filenames.csv',
#     filename_params='/home/user/openMS_MRMworkflow/GCMS_fullScan/MRMFeatureFinderScoring_params.csv',
#     delimiter=',',
#     )

# from tests import runAllTests
# runAllTests()

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
