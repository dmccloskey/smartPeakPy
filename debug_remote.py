#VSCode remote debugging
######
import ptvsd
ptvsd.enable_attach("my_secret", address = ('0.0.0.0', 3000))
#enable the below line of code only if you want the application to wait until the debugger has attached to it
ptvsd.wait_for_attach()
######

from smartPeak.core.__main__ import __main__
m = __main__()

# m.run_openSWATH_validation_py(
#     filename_filenames='/home/user/openMS_MRMworkflow/BloodProject01_validation/filenames.csv',
#     filename_params='/home/user/openMS_MRMworkflow/BloodProject01_validation/MRMFeatureFinderScoring_params.csv', #QMIP
#     # filename_params='/home/user/openMS_MRMworkflow/BloodProject01_validation/MRMFeatureFinderScoring_params_filterControl.csv', #FILTERCONTROL
#     delimiter=','
#     )

# m.run_AbsoluteQuantitation_py(
#     filename_filenames='/home/user/openMS_MRMworkflow/Unknowns/filenames.csv',
#     filename_params='/home/user/openMS_MRMworkflow/Unknowns/MRMFeatureFinderScoring_params.csv',
#     delimiter=',',
#     pick_peaks = False,
#     select_peaks = True,
#     validate_peaks = False,
#     quantify_peaks = True,
#     check_peaks = True,
#     )

m.run_AbsoluteQuantitation_py(
    filename_filenames='/home/user/openMS_MRMworkflow/GC-MS/filenames.csv',
    filename_params='/home/user/openMS_MRMworkflow/GC-MS/MRMFeatureFinderScoring_params.csv',
    delimiter=',',
    pick_peaks = True,
    select_peaks = True,
    validate_peaks = False,
    quantify_peaks = False
    )

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
