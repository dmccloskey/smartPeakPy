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

# from tests import runAllTests
# runAllTests()