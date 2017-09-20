#VSCode local debugging

from smartPeak.__main__ import __main__
m = __main__()

# Run Quantitation
m.run_openSWATH_py(
    filename_filenames='/home/user/openMS_MRMworkflow/BloodProject01/BloodProject01_SWATH_filenames.csv',
    filename_params='/home/user/openMS_MRMworkflow/BloodProject01/BloodProject01_MRMFeatureFinderScoring_params.csv',
    delimiter=','
    )
m.run_AbsoluteQuantitation_py(
    filename_filenames='/home/user/openMS_MRMworkflow/BloodProject01/BloodProject01_SWATH_filenames.csv',
    filename_params='/home/user/openMS_MRMworkflow/BloodProject01/BloodProject01_MRMFeatureFinderScoring_params.csv',
    delimiter=','
    )
