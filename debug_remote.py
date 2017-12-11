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

# # GCMS_fullScan
# m.main(
#     filename_filenames='/home/user/Data/GCMS_fullScan/filenames.csv',
#     filename_params='/home/user/Data/GCMS_fullScan/MRMFeatureFinderScoring_params.csv',
#     delimiter=',',
#     )

from tests.test_pyTOPP_SequenceHandler import TestSequenceHandler
test = TestSequenceHandler()
test.test_addSampleToSequence()
test.test_getMetaValue()
test.test_makeDataMatrixFromMetaValue()
test.test_parse_metaData()
test.test_addFeatureMapToSequence()
