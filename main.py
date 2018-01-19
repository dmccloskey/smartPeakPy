# -*- coding: utf-8 -*-
from smartPeak.core.SequenceHandler import SequenceHandler
from smartPeak.core.SequenceProcessor import SequenceProcessor
from smartPeak.io.SequenceWriter import SequenceWriter

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

# process all files
sequenceProcessor.processSequence(
    sequenceHandler) 

# store all features
raw_data_processing_methods = {
    "load_raw_data": False,
    "load_peaks": False,
    "pick_peaks": False,
    "filter_peaks": False,
    "select_peaks": False,
    "validate_peaks": False,
    "quantify_peaks": False,
    "check_peaks": False,
    "plot_peaks": False,
    "store_peaks": True}
sequenceProcessor.processSequence(
    sequenceHandler,
    raw_data_processing_methods_I=raw_data_processing_methods) 

# write out a summary of all files
sequenceSummary_csv_i = '''%s/SequenceSummary.csv''' % (dir_I)
sequenceWriter.write_dataMatrixFromMetaValue(
    sequenceHandler,
    filename=sequenceSummary_csv_i,
    # meta_data=[
    # 'calculated_concentration','RT','peak_apex_int',
    # 'noise_background_level','leftWidth','rightWidth'],
    meta_data=['calculated_concentration'],
    sample_types=['Unknown']
)