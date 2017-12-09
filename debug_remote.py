# VSCode remote debugging
######
import ptvsd
ptvsd.enable_attach("my_secret", address=('0.0.0.0', 3000))
# enable the below line of code only if you want the application to wait
# until the debugger has attached to it
ptvsd.wait_for_attach()
######

from smartPeak.core.__main__ import __main__
m = __main__()


# # LCMS_MRM
# m.main(
#     filename_filenames='/home/user/Data/LCMS_MRM/filenames.csv',
#     filename_params='/home/user/Data/LCMS_MRM/MRMFeatureFinderScoring_params.csv',
#     delimiter=',',
#     )

# # GCMS_SRM
# m.main(
#     filename_filenames='/home/user/Data/GCMS_SRM/filenames.csv',
#     filename_params='/home/user/Data/GCMS_SRM/MRMFeatureFinderScoring_params.csv',
#     delimiter=',',
#     )

# # GCMS_fullScan
# m.main(
#     filename_filenames='/home/user/Data/GCMS_fullScan/filenames.csv',
#     filename_params='/home/user/Data/GCMS_fullScan/MRMFeatureFinderScoring_params.csv',
#     delimiter=',',
#     )

from tests.test_core_main import testMain
test = testMain()
test.test_core_main_GCMS_SRM()

from tests import runAllTests
runAllTests()
