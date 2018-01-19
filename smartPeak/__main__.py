# -*- coding: utf-8 -*-
from smartPeak.core.Utilities import Utilities
from smartPeak.io.FileReader import FileReader
from smartPeak.io.FileWriter import FileWriter
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS
from smartPeak.io.FileWriterOpenMS import FileWriterOpenMS
from smartPeak.core.RawDataHandler import RawDataHandler
from smartPeak.core.RawDataProcessor import RawDataProcessor
from smartPeak.core.SequenceHandler import SequenceHandler
from smartPeak.core.SequenceProcessor import SequenceProcessor
from smartPeak.io.SequenceReader import SequenceReader
from smartPeak.io.SequenceWriter import SequenceWriter


class __main__():

    def main2(
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

        # check that all files are found
        raw_data_processing_methods = {
            "load_raw_data": True,
            "load_peaks": False,
            "pick_peaks": False,
            "filter_peaks": False,
            "select_peaks": False,
            "validate_peaks": False,
            "quantify_peaks": False,
            "check_peaks": False,
            "plot_peaks": False,
            "store_peaks": False}
        sequenceProcessor.processSequence(
            sequenceHandler,
            raw_data_processing_methods_I=raw_data_processing_methods) 

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

    def main(
        self,
        filename_sequence,
        filename_params,
        delimiter=',',
        pick_peaks=True,
        select_peaks=True,
        validate_peaks=False,
        quantify_peaks=True,
        check_peaks=False,
        plot_peaks=False,
        verbose_I=False,
        *Args,
        **Kwargs
    ):
        """Run the AbsoluteQuantitation python pipeline
        
        Args:
            filename (str): name of the workflow parameter filename
            verbose (bool): print command line statements to stdout
            
        """
        
        # internal variables
        skipped_samples = []
        validation_metrics = []

        # class initializations        
        seqHandler = SequenceHandler()
        seqWriter = SequenceWriter()
        seqReader = SequenceReader()
        rawDataProcessor = RawDataProcessor()
        fileReaderOpenMS = FileReaderOpenMS()
        fileWriterOpenMS = FileWriterOpenMS()
        fileReader = FileReader()

        # read in the files
        seqReader.read_sequenceFile(
            seqHandler, filename_sequence, delimiter)
        fileReader.read_openMSParams(filename_params, delimiter)
        params = fileReader.getData()
        fileReader.clear_data()

        # check for updated workflow parameters
        if "run_AbsoluteQuantitation" in params:
            utilities = Utilities()
            workflow_parameters = {
                d['name']: utilities.castString(d['value'], d['type'])
                for d in params["run_AbsoluteQuantitation"]}
            if "pick_peaks" in workflow_parameters:
                pick_peaks = workflow_parameters["pick_peaks"]
            if "filter_peaks" in workflow_parameters:
                filter_peaks = workflow_parameters["filter_peaks"]
            if "select_peaks" in workflow_parameters:
                select_peaks = workflow_parameters["select_peaks"]
            if "validate_peaks" in workflow_parameters:
                validate_peaks = workflow_parameters["validate_peaks"]
            if "quantify_peaks" in workflow_parameters:
                quantify_peaks = workflow_parameters["quantify_peaks"]
            if "check_peaks" in workflow_parameters:
                check_peaks = workflow_parameters["check_peaks"]
            if "plot_peaks" in workflow_parameters:
                plot_peaks = workflow_parameters["plot_peaks"]
            if "verbose_I" in workflow_parameters:
                verbose_I = workflow_parameters["verbose_I"]

        # check for workflow parameters integrity
        required_parameters = [
            "MRMMapping",
            "ChromatogramExtractor", "MRMFeatureFinderScoring",
            "MRMFeatureFilter.filter_MRMFeatures",
            "MRMFeatureSelector.select_MRMFeatures_qmip",
            "MRMFeatureSelector.schedule_MRMFeatures_qmip",
            "MRMFeatureSelector.select_MRMFeatures_score",
            "ReferenceDataMethods.getAndProcess_referenceData_samples",
            "MRMFeatureValidator.validate_MRMFeatures",
            "MRMFeatureFilter.filter_MRMFeatures.qc",
        ]
        for parameter in required_parameters:
            if parameter not in params:
                params[parameter] = []

        for sequence in seqHandler.getSequence():
            print("processing sample " + sequence.meta_data["sample_name"])
            try:
                rawDataHandler = RawDataHandler()
                
                # dynamically make the filenames
                mzML_i = '''%s/mzML/%s''' % (
                    sequence.meta_data["data_dir"],
                    sequence.meta_data["filename"])
                traML_csv_i = '''%s/traML.csv''' % (sequence.meta_data["data_dir"])
                # trafo_csv_i = '''%s/trafo.csv''' % (data_dir)
                db_json_i = '''%s/settings.ini''' % (sequence.meta_data["data_dir"])

                # load in the files
                fileReaderOpenMS.load_TraML(
                    rawDataHandler,  traML_csv_i, verbose_I=verbose_I)                
                fileReaderOpenMS.load_SWATHorDIA(rawDataHandler, {})
                fileReaderOpenMS.load_MSExperiment(
                    rawDataHandler, 
                    mzML_i,
                    MRMMapping_params_I=params['MRMMapping'],
                    chromatogramExtractor_params_I=params['ChromatogramExtractor'],
                    verbose_I=verbose_I)
                rawDataProcessor.extract_metaData(rawDataHandler, verbose_I=verbose_I)
                fileReaderOpenMS.load_Trafo(  # skip transformation of RT
                    rawDataHandler, 
                    None,  # {'trafo_csv_i':trafo_csv_i},
                    params['MRMFeatureFinderScoring'],
                    verbose_I=verbose_I)

                # pick peaks with OpenSWATH
                featureXML_o = '''%s/features_tmp/%s.featureXML''' % (
                    sequence.meta_data["data_dir"],
                    sequence.meta_data["sample_name"]) 
                feature_csv_o = '''%s/features_tmp/%s.csv''' % (
                    sequence.meta_data["data_dir"],
                    sequence.meta_data["sample_name"])
                if pick_peaks:
                    # run the openSWATH workflow for metabolomics
                    rawDataProcessor.pickFeatures(
                        rawDataHandler,
                        params['MRMFeatureFinderScoring'],
                        verbose_I=verbose_I)
                    # store
                    fileWriterOpenMS.store_featureMap(
                        rawDataHandler, featureXML_o, feature_csv_o,
                        verbose_I=verbose_I)
                elif filter_peaks or select_peaks or plot_peaks or validate_peaks\
                or quantify_peaks or check_peaks:
                    try:
                        fileReaderOpenMS.load_featureMap(
                            rawDataHandler,
                            featureXML_o,
                            verbose_I=verbose_I)
                    except Exception as e:
                        print(e)

                # Filter features
                featureXML_o = '''%s/features/%s.featureXML''' % (
                    sequence.meta_data["data_dir"],
                    sequence.meta_data["sample_name"]) 
                feature_csv_o = '''%s/features/%s.csv''' % (
                    sequence.meta_data["data_dir"],
                    sequence.meta_data["sample_name"])
                if filter_peaks:
                    featureFilter_csv_i = '''%s/featureFilters.csv''' % (
                        sequence.meta_data["data_dir"])
                    fileReaderOpenMS.load_featureFilter(
                        rawDataHandler,
                        featureFilter_csv_i
                        )
                    rawDataProcessor.filterFeatures(
                        rawDataHandler,
                        MRMFeatureFilter_filter_params_I=params[
                            'MRMFeatureFilter.filter_MRMFeatures'],
                        verbose_I=verbose_I
                    )
                    # store
                    fileWriterOpenMS.store_featureMap(
                        rawDataHandler, featureXML_o, feature_csv_o,
                        verbose_I=verbose_I)
                elif select_peaks or plot_peaks or validate_peaks or quantify_peaks\
                or check_peaks:        
                    try:
                        fileReaderOpenMS.load_featureMap(
                            rawDataHandler,
                            featureXML_o,
                            verbose_I=verbose_I)
                    except Exception as e:
                        try:  # in case features were not filtered previously
                            featureXML_o = '''%s/features_tmp/%s.featureXML''' % (
                                sequence.meta_data["data_dir"],
                                sequence.meta_data["sample_name"]) 
                            fileReaderOpenMS.load_featureMap(
                                rawDataHandler,
                                featureXML_o,
                                verbose_I=verbose_I)
                        except Exception as e:
                            print(e)

                # Select features
                featureXML_o = '''%s/features/%s.featureXML''' % (
                    sequence.meta_data["data_dir"],
                    sequence.meta_data["sample_name"]) 
                feature_csv_o = '''%s/features/%s.csv''' % (
                    sequence.meta_data["data_dir"],
                    sequence.meta_data["sample_name"])
                if select_peaks:
                    rawDataProcessor.selectFeatures(
                        rawDataHandler,
                        # qmip algorithm
                        MRMFeatureSelector_select_params_I=params[
                            'MRMFeatureSelector.select_MRMFeatures_qmip'],
                        MRMFeatureSelector_schedule_params_I=params[
                            'MRMFeatureSelector.schedule_MRMFeatures_qmip'],
                        # score algorithm
                        # MRMFeatureSelector_select_params_I=params[
                        #     'MRMFeatureSelector.select_MRMFeatures_score'],
                        # MRMFeatureSelector_schedule_params_I={},
                        verbose_I=verbose_I
                    )
                    # store
                    fileWriterOpenMS.store_featureMap(
                        rawDataHandler, featureXML_o, feature_csv_o,
                        verbose_I=verbose_I)
                elif plot_peaks or validate_peaks or quantify_peaks or check_peaks:        
                    try:
                        fileReaderOpenMS.load_featureMap(
                            rawDataHandler,
                            featureXML_o,
                            verbose_I=verbose_I)
                    except Exception as e:
                        print(e)

                # Plot peaks and features
                if plot_peaks:
                    # export diagnostic plots
                    features_pdf_o = '''%s/features/%s''' % (
                        sequence.meta_data["data_dir"],
                        sequence.meta_data["sample_name"]) 
                    rawDataProcessor.export_featurePlots(
                        rawDataHandler,
                        filenames_I={'features_pdf_o': features_pdf_o},
                        FeaturePlotter_params_I=params[
                            'FeaturePlotter'],
                        verbose_I=verbose_I)

                # Validate peaks
                # dynamically make the filenames
                featureXML_o = '''%s/features/%s.featureXML''' % (
                    sequence.meta_data["data_dir"],
                    sequence.meta_data["sample_name"]) 
                feature_csv_o = '''%s/features/%s.csv''' % (
                    sequence.meta_data["data_dir"],
                    sequence.meta_data["sample_name"])
                if validate_peaks:
                    # load in the validation data 
                    # (if no data is found, continue to the next sample)
                    ReferenceDataMethods_params_I = []
                    ReferenceDataMethods_params_I.extend(
                        params['ReferenceDataMethods.getAndProcess_referenceData_samples']
                        )
                    sample_names_I = '''['%s']''' % (sequence.meta_data["sample_name"])
                    ReferenceDataMethods_params_I.append({
                        'description': '', 'name': 'sample_names_I', 
                        'type': 'list', 'value': sample_names_I})
                    fileReaderOpenMS.load_validationData(
                        rawDataHandler,
                        db_json_i,
                        ReferenceDataMethods_params_I,
                        verbose_I=verbose_I
                        )
                    if not rawDataHandler.reference_data:
                        skipped_samples.append({
                            'sample_name': sequence.meta_data["sample_name"],
                            'error_message': 'no reference data found'})
                        print(
                            'Reference data not found for sample ' +
                            sequence.meta_data["sample_name"] + '.')
                        continue
                    # validate the data
                    rawDataProcessor.validateFeatures(
                        rawDataHandler,
                        params['MRMFeatureValidator.validate_MRMFeatures'],
                        verbose_I=verbose_I)
                    fileWriterOpenMS.store_featureMap(
                        rawDataHandler, featureXML_o, feature_csv_o,
                        verbose_I=verbose_I)
                elif quantify_peaks or check_peaks:                   
                    try:
                        fileReaderOpenMS.load_featureMap(
                            rawDataHandler,
                            featureXML_o,
                            verbose_I=verbose_I)
                    except Exception as e:
                        print(e)

                # Quantify peaks
                # dynamically make the filenames
                featureXML_o = '''%s/quantitation/%s.featureXML''' % (
                    sequence.meta_data["data_dir"],
                    sequence.meta_data["sample_name"]) 
                feature_csv_o = '''%s/quantitation/%s.csv''' % (
                    sequence.meta_data["data_dir"],
                    sequence.meta_data["sample_name"])
                if quantify_peaks:
                    quantitationMethods_csv_i = '''%s/quantitationMethods.csv''' % (
                        sequence.meta_data["data_dir"])
                    # load the quantitation method
                    fileReaderOpenMS.load_quantitationMethods(
                        rawDataHandler,
                        quantitationMethods_csv_i,
                        verbose_I=verbose_I)
                    # quantify the components
                    rawDataProcessor.quantifyComponents(
                        rawDataHandler, verbose_I=verbose_I)
                    fileWriterOpenMS.store_featureMap(
                        rawDataHandler, featureXML_o, feature_csv_o,
                        verbose_I=verbose_I)
                elif check_peaks: 
                    try:
                        fileReaderOpenMS.load_featureMap(
                            rawDataHandler, featureXML_o)
                    except Exception as e:
                        # Peaks have not been quantified, try opening picked peaks
                        featureXML_o = '''%s/features/%s.featureXML''' % (
                            sequence.meta_data["data_dir"],
                            sequence.meta_data["sample_name"])
                        fileReaderOpenMS.load_featureMap(
                            rawDataHandler,
                            featureXML_o,
                            verbose_I=verbose_I)

                # QC the peaks
                featureXML_o = '''%s/quantitation/%s.featureXML''' % (
                    sequence.meta_data["data_dir"],
                    sequence.meta_data["sample_name"]) 
                feature_csv_o = '''%s/quantitation/%s.csv''' % (
                    sequence.meta_data["data_dir"],
                    sequence.meta_data["sample_name"])
                if check_peaks:
                    featureQC_csv_i = '''%s/featureQCs.csv''' % (
                        sequence.meta_data["data_dir"])
                    fileReaderOpenMS.load_featureQC(
                        rawDataHandler,
                        featureQC_csv_i
                        )
                    rawDataProcessor.checkFeatures(
                        rawDataHandler,
                        MRMFeatureFilter_qc_params_I=params[
                            'MRMFeatureFilter.filter_MRMFeatures.qc'],
                        verbose_I=verbose_I
                    )
                    # store
                    fileWriterOpenMS.store_featureMap(
                        rawDataHandler, featureXML_o, feature_csv_o,
                        verbose_I=verbose_I)

                # record features
                seqHandler.addFeatureMapToSequence(
                    sequence.meta_data["sample_name"], rawDataHandler.featureMap)
            except Exception as e:
                print(e)
                skipped_samples.append({
                    'sample_name': sequence.meta_data["sample_name"],
                    'error_message': e})
            # manual clear data for the next iteration
            rawDataHandler.clear_data()
        # export results
        if skipped_samples:
            smartpeak_o = FileWriter(skipped_samples)
            skippedSamples_csv_i = '''%s/mzML/skippedSamples.csv''' % (
                sequence.meta_data["data_dir"]
            )
            smartpeak_o.write_dict2csv(skippedSamples_csv_i)
        if validation_metrics:
            smartpeak_o = FileWriter(validation_metrics)
            validationMetrics_csv_i = '''%s/validation/validationMetrics.csv''' % (
                sequence.meta_data["data_dir"])
            smartpeak_o.write_dict2csv(validationMetrics_csv_i)
        sequenceSummary_csv_i = '''%s/SequenceSummary.csv''' % (
            sequence.meta_data["data_dir"])
        seqWriter.write_dataMatrixFromMetaValue(
            seqHandler,
            filename=sequenceSummary_csv_i,
            # meta_data=[
            # 'calculated_concentration','RT','peak_apex_int',
            # 'noise_background_level','leftWidth','rightWidth'],
            meta_data=['calculated_concentration'],
            sample_types=['Unknown']
        )