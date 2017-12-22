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

from tests.test_data_DBTableInterface import TestDBTableInterface
test = TestDBTableInterface()
test.test_get_tableName()
test.test_get_tableColumns()
test.test_get_sequenceName()
test.test_createAndDropTable()

# from tests import runAllTests
# runAllTests()