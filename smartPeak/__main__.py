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
            "store_features", 
            # "plot_features"
        ]

        # process all files
        raw_data_processing_methods = [
            "load_raw_data",
            "load_features",
            "check_features",
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
            meta_data=['calculated_concentration'],
            sample_types=['Unknown']
        )

        featureSummary_csv_i = '''%s/FeatureSummary.csv''' % (dir_I)
        sequenceWriter.write_dataTableFromMetaValue(
            sequenceHandler,
            filename=featureSummary_csv_i,
            meta_data=[
                "peak_apex_int", "total_width", "width_at_50", 
                "tailing_factor", "asymmetry_factor", "baseline_delta_2_height", 
                "points_across_baseline", "points_across_half_height", "logSN",
                "QC_transition_message"],
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
        raw_data_processing_methods = [
            "load_raw_data",
            "pick_features",
            "filter_features",
            "filter_features",
            "select_features",
            "check_features",
            "store_features", 
            # "plot_features"
        ]
        # raw_data_processing_methods = [
        #     "load_raw_data",
        #     "load_features",
        #     "filter_features",
        #     "check_features",
        #     "store_features", 
        #     # "quantify_features",
        #     # "store_features", 
        #     # "plot_features"
        # ]
        sequenceProcessor.processSequence(
            sequenceHandler,
            raw_data_processing_methods_I=raw_data_processing_methods,
            verbose_I=True)

        # 2. process optimize calibrators
        sequence_segment_processing_methods = [
            "calculate_calibration",
            "plot_calibrators",
            "store_quantitation_methods",
            # "load_quantitation_methods",
            # "store_components_to_concentrations"
        ]
        sequenceProcessor.processSequenceSegments(
            sequenceHandler,
            sequence_segment_processing_methods_I=sequence_segment_processing_methods,
            verbose_I=True)

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
            raw_data_processing_methods_I=raw_data_processing_methods,
            verbose_I=True)

        # write out a summary of all files
        sequenceSummary_csv_i = '''%s/SequenceSummary.csv''' % (dir_I)
        sequenceWriter.write_dataMatrixFromMetaValue(
            sequenceHandler,
            filename=sequenceSummary_csv_i,
            meta_data=['calculated_concentration'],
            sample_types=['Standard']
        )