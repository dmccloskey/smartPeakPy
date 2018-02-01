# -*- coding: utf-8 -*-
from smartPeak.core.SequenceHandler import SequenceHandler
from smartPeak.core.SequenceProcessor import SequenceProcessor
from smartPeak.io.SequenceWriter import SequenceWriter


class __main__():

    def example_LCMS_MRM_Unknowns(
        self,
        dir_I,
        delimiter_I=",",
        verbose_I=False,
        *Args,
        **Kwargs
    ):
        """Run the AbsoluteQuantitation python pipeline
        
        Args:
            dir_I (str): name of the directory (filenames will be created dynamically)
            verbose (bool): print command line statements to stdout
            
        """
        
        sequenceHandler = SequenceHandler()
        sequenceProcessor = SequenceProcessor()
        sequenceWriter = SequenceWriter()

        # set the directory for all files and data
        sequenceHandler.setDirStatic(dir_I)
        sequenceHandler.setDirDynamic(dir_I)

        sequenceProcessor.createSequence(
            sequenceHandler,
            delimiter=","
        )

        # process all files
        raw_data_processing_methods = [
            "load_raw_data",
            # "load_features",
            "pick_features",
            "filter_features",
            "select_features",
            # "validate_features",
            "quantify_features",
            "check_features",
        ]
        sequenceProcessor.processSequence(
            sequenceHandler,
            raw_data_processing_methods_I=raw_data_processing_methods)

        # store all features
        raw_data_processing_methods = [
            "store_features", 
            # "plot_features"
        ]
        sequenceProcessor.processSequence(
            sequenceHandler,
            raw_data_processing_methods_I=raw_data_processing_methods) 

        # write out a summary of all files
        sequenceSummary_csv_i = '''%s/SequenceSummary.csv''' % (dir_I)
        sequenceWriter.write_dataMatrixFromMetaValue(
            sequenceHandler,
            filename=sequenceSummary_csv_i,
            meta_data=['calculated_concentration'],
            sample_types=['Unknown']
        )

    def example_LCMS_MRM_Standards(
        self,
        dir_I,
        delimiter_I=",",
        verbose_I=False,
        *Args,
        **Kwargs
    ):
        """Run the AbsoluteQuantitation python pipeline
        
        Args:
            dir_I (str): name of the directory (filenames will be created dynamically)
            verbose (bool): print command line statements to stdout
            
        """
        
        sequenceHandler = SequenceHandler()
        sequenceProcessor = SequenceProcessor()
        sequenceWriter = SequenceWriter()

        # set the directory for all files and data
        sequenceHandler.setDirStatic(dir_I)
        sequenceHandler.setDirDynamic(dir_I)

        sequenceProcessor.createSequence(
            sequenceHandler,
            delimiter=","
        )

        # 1. process all files
        # raw_data_processing_methods = [
        #     "load_raw_data",
        #     "pick_features",
        #     "filter_features",
        #     "select_features",
        #     "check_features",
        #     "store_features", 
        #     # "plot_features"
        # ]
        raw_data_processing_methods = [
            "load_raw_data",
            "load_features",
        ]
        sequenceProcessor.processSequence(
            sequenceHandler,
            raw_data_processing_methods_I=raw_data_processing_methods)

        # 2. process optimize calibrators
        sequence_segment_processing_methods = [
            "calculate_calibration",
            "store_quantitation_methods",
            # "load_quantitation_methods",
            # "store_components_to_concentrations"
        ]
        sequenceProcessor.processSequenceSegments(
            sequenceHandler,
            sequence_segment_processing_methods_I=sequence_segment_processing_methods)

        # 3. quantify standards for QC
        raw_data_processing_methods = [
            # "load_raw_data",
            # "load_features",
            # "pick_features",
            # "filter_features",
            # "select_features",
            # "validate_features",
            "quantify_features",
            "check_features",
            "store_features", 
            # "plot_features"
        ]
        sequenceProcessor.processSequence(
            sequenceHandler,
            raw_data_processing_methods_I=raw_data_processing_methods)

        # write out a summary of all files
        sequenceSummary_csv_i = '''%s/SequenceSummary.csv''' % (dir_I)
        sequenceWriter.write_dataMatrixFromMetaValue(
            sequenceHandler,
            filename=sequenceSummary_csv_i,
            meta_data=['calculated_concentration'],
            sample_types=['Unknown']
        )