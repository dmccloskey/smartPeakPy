# VSCode remote debugging
######
import ptvsd
ptvsd.enable_attach("my_secret", address=('0.0.0.0', 3000))
# enable the below line of code only if you want the application to wait
# until the debugger has attached to it
ptvsd.wait_for_attach()
######

from smartPeak.__main__ import __main__
m = __main__()

# # GCMS_fullScan
# m.main(
#     filename_filenames='/home/user/Data/GCMS_fullScan/filenames.csv',
#     filename_params='/home/user/Data/GCMS_fullScan/MRMFeatureFinderScoring_params.csv',
#     delimiter=',',
#     )

# from tests import runAllTests
# runAllTests()

from tests.test_main import testMain
test = testMain()
test.test_main_HPLC_FLD_Emmission1_StandardsAndUnknowns()