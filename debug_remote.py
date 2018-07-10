# VSCode remote debugging
######
import ptvsd
ptvsd.enable_attach("my_secret", address=('0.0.0.0', 3000))
# enable the below line of code only if you want the application to wait
# until the debugger has attached to it
ptvsd.wait_for_attach()
######

# -*- coding: utf-8 -*-
from smartPeak.core.SequenceHandler import SequenceHandler
from smartPeak.core.SequenceProcessor import SequenceProcessor
from smartPeak.io.SequenceWriter import SequenceWriter

from smartPeak.core.RawDataProcessor import RawDataProcessor

sequenceHandler = SequenceHandler()
sequenceProcessor = SequenceProcessor()
sequenceWriter = SequenceWriter()

# set the directory for all files and data
dir_I = "/home/user/Data"
sequenceHandler.setDirStatic(dir_I)
sequenceHandler.setDirDynamic(dir_I)

sequenceProcessor.createSequence(
    sequenceHandler,
    delimiter=","
)

# # process and store all files
# raw_data_processing_methods = [
#     "load_raw_data",
#     # "load_features",
#     "pick_features",
#     "quantify_features",
#     "check_features",
#     "store_features",
# ]
# sequenceProcessor.processSequence(
#     sequenceHandler,
#     raw_data_processing_methods_I=raw_data_processing_methods,
#     verbose_I=True)

# process and store all files
raw_data_processing_methods = [
    "load_features",
]
sequenceProcessor.processSequence(
    sequenceHandler,
    raw_data_processing_methods_I=raw_data_processing_methods,
    verbose_I=True)

for sample in sequenceHandler.getSequence():
    sample.getRawData().saveCurrentFeatureMapToHistory()

# filter and select
raw_data_processing_methods = [
    "filter_features",
    "select_features",
]
sequenceProcessor.processSequence(
    sequenceHandler,
    raw_data_processing_methods_I=raw_data_processing_methods,
    verbose_I=True)

rawDataProcessor = RawDataProcessor()
for sample in sequenceHandler.getSequence():
    rawDataProcessor.annotateUsedFeatures(sample.getRawData(), verbose_I=True)

# report and plot only
raw_data_processing_methods = [
    # "load_raw_data",
    # "load_features",
    "store_features",
    # "plot_features"
]
sequenceProcessor.processSequence(
    sequenceHandler,
    raw_data_processing_methods_I=raw_data_processing_methods,
    verbose_I=True)

# write out a summary of all files
# sequenceSummary_csv_i = '''%s/SequenceSummary.csv''' % (dir_I)
# sequenceWriter.write_dataMatrixFromMetaValue(
#     sequenceHandler,
#     filename=sequenceSummary_csv_i,
#     meta_data=['calculated_concentration','RT'],
#     sample_types=['Unknown']
# )

featureSummary_csv_i = '''%s/FeatureSummary.csv''' % (dir_I)
sequenceWriter.write_dataTableFromMetaValue(
    sequenceHandler,
    filename=featureSummary_csv_i,
    meta_data=[
        "used_", "RT", "peak_apex_int", "total_width", "width_at_50", 
        "tailing_factor", "asymmetry_factor", "baseline_delta_2_height", 
        "points_across_baseline", "points_across_half_height", "logSN",
        "calculated_concentration",
        "QC_transition_message", "QC_transition_pass", "QC_transition_score",
        "QC_transition_group_message", "QC_transition_group_score"],
    sample_types=['Unknown']
)
