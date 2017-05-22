#VSCode remote debugging
######
import ptvsd
ptvsd.enable_attach("my_secret", address = ('0.0.0.0', 3001))
# ptvsd.enable_attach(None, address = ('0.0.0.0', 3000))
#enable the below line of code only if you want the application to wait untill the debugger has attached to it
ptvsd.wait_for_attach()
######

from smartPeak.__main__ import __main__
m = __main__()

# # Test openSWATH_cmd
# filename='/home/user/openMS_MRMworkflow/openSWATH_cmd_params_Isolate1.csv'
# m.run_openSWATH_cmd(filename)

# # Test openSWATH_py
# m.run_openSWATH_py(
#     filename_filenames='/home/user/openMS_MRMworkflow/filenames.csv',
#     filename_params='/home/user/openMS_MRMworkflow/MRMFeatureFinderScoring_params.csv',
#     delimiter = ';'
#     );

# Test file conversions
m.convert_MQQMethod2Feature(
    filename_I='/home/user/openMS_MRMworkflow/qmethod.csv',
    filename_O='/home/user/openMS_MRMworkflow/feature.csv'
    )
