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

import pyopenms
import copy

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

# process and store all files
raw_data_processing_methods = [
    "load_raw_data",
    # "load_features",
    "pick_features",
    "quantify_features",
    "check_features",
]
sequenceProcessor.processSequence(
    sequenceHandler,
    raw_data_processing_methods_I=raw_data_processing_methods,
    verbose_I=True)

sequenceHandler_copy = copy.copy(sequenceHandler)

# filter and select
raw_data_processing_methods = [
    "filter_features",
    "select_features",
]
sequenceProcessor.processSequence(
    sequenceHandler,
    raw_data_processing_methods_I=raw_data_processing_methods,
    verbose_I=True)

for sample_cnt, sample_copy in enumerate(sequenceHandler_copy.getSequence()):
    sample_select = sequenceHandler.getSamplesInSequence([sample_copy.getMetaData()["sample_name"]])[0]
    features_annotated = pyopenms.FeatureMap()
    for feature_cnt, feature_copy in enumerate(sample_copy.getRawData().getFeatureMap()):    
        subordinates_annotated = []
        for subordinate_cnt, subordinate_copy in enumerate(feature_copy.getSubordinates()):
            subordinate_copy.setMetaValue("used_".encode('utf-8'), "false".encode('utf-8'))
            subordinates_annotated.append(subordinate_copy)
        for feature_select in sample_select.getRawData().getFeatureMap():
            if feature_select.getUniqueId() == feature_copy.getUniqueId():
                for subordinate_copy in subordinates_annotated:
                    for subordinate_select in feature_select.getSubordinates():
                        if subordinate_select.getMetaValue("native_id") == subordinate_copy.getMetaValue("native_id"):
                            subordinate_copy.setMetaValue("used_".encode('utf-8'), "true".encode('utf-8'))
                break        
        feature_copy.setSubordinates(subordinates_annotated)
        features_annotated.push_back(feature_copy)
    sequenceHandler_copy.getSequence()[sample_cnt].getRawData().setFeatureMap(features_annotated)

sequenceHandler = copy.copy(sequenceHandler_copy)

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
sequenceSummary_csv_i = '''%s/SequenceSummary.csv''' % (dir_I)
sequenceWriter.write_dataMatrixFromMetaValue(
    sequenceHandler,
    filename=sequenceSummary_csv_i,
    meta_data=['calculated_concentration','RT'],
    sample_types=['Unknown']
)

featureSummary_csv_i = '''%s/FeatureSummary.csv''' % (dir_I)
sequenceWriter.write_dataTableFromMetaValue(
    sequenceHandler,
    filename=featureSummary_csv_i,
    meta_data=[
        "RT", "peak_apex_int", "total_width", "width_at_50", 
        "tailing_factor", "asymmetry_factor", "baseline_delta_2_height", 
        "points_across_baseline", "points_across_half_height", "logSN",
        "calculated_concentration",
        "QC_transition_message", "QC_transition_pass", "QC_transition_score",
        "QC_transition_group_message", "QC_transition_group_score"],
    sample_types=['Unknown']
)