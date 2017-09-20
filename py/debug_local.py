#VSCode local debugging

from smartPeak.__main__ import __main__
m = __main__()

# Run Quantitation
m.convert_MQQMethod2Feature(
    filename_I='C:/Users/domccl/Dropbox (UCSD SBRG)/Project_FastPeak/openMS_MRMworkflow/qmethod.csv',
    filename_O='C:/Users/domccl/Dropbox (UCSD SBRG)/Project_FastPeak/openMS_MRMworkflow/feature.csv'
    )
