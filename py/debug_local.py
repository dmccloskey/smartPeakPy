from smartPeak.core.__main__ import __main__
m = __main__()

# Run Quantitation
m.run_AbsoluteQuantitation_py(
    filename_filenames='/home/user/openMS_MRMworkflow/Unknowns/filenames.csv',
    filename_params='/home/user/openMS_MRMworkflow/Unknowns/MRMFeatureFinderScoring_params.csv',
    delimiter=',',
    pick_peaks = False,
    select_peaks = False,
    quantify_peaks = False
    )
