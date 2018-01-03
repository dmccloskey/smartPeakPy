# -*- coding: utf-8 -*-
from smartPeak.core.smartPeak import smartPeak
from smartPeak.io.FileReader import FileReader
from smartPeak.io.FileWriter import FileWriter


class __main__():

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
        # additional resources
        from smartPeak.core.SequenceHandler import SequenceHandler
        from smartPeak.core.FileWriterpenSWATH import FileWriterpenSWATH
        from smartPeak.core.smartPeak_AbsoluteQuantitation import \
            smartPeak_AbsoluteQuantitation

        # internal variables
        skipped_samples = []
        validation_metrics = []

        # class initializations        
        seqhandler = SequenceHandler()
        AbsoluteQuantitation = smartPeak_AbsoluteQuantitation()
        openSWATH = FileWriterpenSWATH()
        smartpeak_i = FileReader()

        # read in the files
        seqhandler.read_sequenceFile(filename_sequence, delimiter)
        smartpeak_i.read_openMSParams(filename_params, delimiter)
        params = smartpeak_i.getData()
        smartpeak_i.clear_data()

        # check for updated workflow parameters
        if "run_AbsoluteQuantitation" in params:
            smartpeak = smartPeak()
            workflow_parameters = {
                d['name']: smartpeak.castString(d['value'], d['type'])
                for d in params["run_AbsoluteQuantitation"]}
            if "pick_peaks" in workflow_parameters:
                pick_peaks = workflow_parameters["pick_peaks"]
            if "select_peaks" in workflow_parameters:
                select_peaks = workflow_parameters["select_peaks"]
            if "validate_peaks" in workflow_parameters:
                validate_peaks = workflow_parameters["validate_peaks"]
            if "check_peaks" in workflow_parameters:
                check_peaks = workflow_parameters["check_peaks"]
            if "quantify_peaks" in workflow_parameters:
                quantify_peaks = workflow_parameters["quantify_peaks"]
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

        for sequence in seqhandler.getSequence():
            print("processing sample " + sequence["meta_data"]["sample_name"])
            try:
                
                # dynamically make the filenames
                mzML_i = '''%s/mzML/%s''' % (
                    sequence["meta_data"]["data_dir"],
                    sequence["meta_data"]["filename"])
                traML_csv_i = '''%s/traML.csv''' % (sequence["meta_data"]["data_dir"])
                # trafo_csv_i = '''%s/trafo.csv''' % (data_dir)
                db_ini_i = '''%s/settings.ini''' % (sequence["meta_data"]["data_dir"])

                # load in the files
                openSWATH.load_TraML({'traML_csv_i': traML_csv_i}, verbose_I=verbose_I)                
                openSWATH.load_SWATHorDIA({})
                openSWATH.load_MSExperiment(
                    {'mzML_feature_i': mzML_i},
                    MRMMapping_params_I=params['MRMMapping'],
                    chromatogramExtractor_params_I=params['ChromatogramExtractor'],
                    verbose_I=verbose_I)
                openSWATH.extract_metaData(verbose_I=verbose_I)
                openSWATH.load_Trafo(  # skip transformation of RT
                    {},  # {'trafo_csv_i':trafo_csv_i},
                    params['MRMFeatureFinderScoring'],
                    verbose_I=verbose_I)

                # pick peaks with OpenSWATH
                featureXML_o = '''%s/features_tmp/%s.featureXML''' % (
                    sequence["meta_data"]["data_dir"],
                    sequence["meta_data"]["sample_name"]) 
                feature_csv_o = '''%s/features_tmp/%s.csv''' % (
                    sequence["meta_data"]["data_dir"],
                    sequence["meta_data"]["sample_name"])
                if pick_peaks:
                    # run the openSWATH workflow for metabolomics
                    openSWATH.openSWATH(
                        params['MRMFeatureFinderScoring'],
                        verbose_I=verbose_I)
                    # store
                    openSWATH.store_featureMap({
                        'featureXML_o': featureXML_o,
                        'feature_csv_o': feature_csv_o},
                        verbose_I=verbose_I)
                elif select_peaks or validate_peaks or quantify_peaks or check_peaks:
                    try:
                        openSWATH.load_featureMap(
                            {'featureXML_i': featureXML_o},
                            verbose_I=verbose_I)
                    except Exception as e:
                        print(e)

                # Filter and select features
                featureXML_o = '''%s/features/%s.featureXML''' % (
                    sequence["meta_data"]["data_dir"],
                    sequence["meta_data"]["sample_name"]) 
                feature_csv_o = '''%s/features/%s.csv''' % (
                    sequence["meta_data"]["data_dir"],
                    sequence["meta_data"]["sample_name"])
                if select_peaks:
                    mrmfeaturefilter_csv_i = '''%s/featureFilters.csv''' % (
                        sequence["meta_data"]["data_dir"])
                    openSWATH.filterAndSelect_py(
                        filenames_I={'mrmfeatureqcs_csv_i': mrmfeaturefilter_csv_i},
                        MRMFeatureFilter_filter_params_I=params[
                            'MRMFeatureFilter.filter_MRMFeatures'],
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
                    openSWATH.store_featureMap({
                        'featureXML_o': featureXML_o,
                        'feature_csv_o': feature_csv_o},
                        verbose_I=verbose_I)
                elif plot_peaks or validate_peaks or quantify_peaks or check_peaks:        
                    try:
                        openSWATH.load_featureMap(
                            {'featureXML_i': featureXML_o},
                            verbose_I=verbose_I)
                    except Exception as e:
                        print(e)

                # Plot peaks and features
                if plot_peaks:
                    # export diagnostic plots
                    features_pdf_o = '''%s/features/%s''' % (
                        sequence["meta_data"]["data_dir"],
                        sequence["meta_data"]["sample_name"]) 
                    openSWATH.export_featurePlots(
                        filenames_I={'features_pdf_o': features_pdf_o},
                        FeaturePlotter_params_I=params[
                            'FeaturePlotter'],
                        verbose_I=verbose_I)

                # Validate peaks
                # dynamically make the filenames
                featureXML_o = '''%s/features/%s.featureXML''' % (
                    sequence["meta_data"]["data_dir"],
                    sequence["meta_data"]["sample_name"]) 
                feature_csv_o = '''%s/features/%s.csv''' % (
                    sequence["meta_data"]["data_dir"],
                    sequence["meta_data"]["sample_name"])
                if validate_peaks:
                    # load in the validation data 
                    # (if no data is found, continue to the next sample)
                    ReferenceDataMethods_params_I = []
                    ReferenceDataMethods_params_I.extend(
                        params['ReferenceDataMethods.getAndProcess_referenceData_samples']
                        )
                    sample_names_I = '''['%s']''' % (sequence["meta_data"]["sample_name"])
                    ReferenceDataMethods_params_I.append({
                        'description': '', 'name': 'sample_names_I', 
                        'type': 'list', 'value': sample_names_I})
                    openSWATH.load_validationData(
                        {'db_ini_i': db_ini_i},
                        ReferenceDataMethods_params_I,
                        verbose_I=verbose_I
                        )
                    if not openSWATH.reference_data:
                        skipped_samples.append({
                            'sample_name': sequence["meta_data"]["sample_name"],
                            'error_message': 'no reference data found'})
                        print(
                            'Reference data not found for sample ' +
                            sequence["meta_data"]["sample_name"] + '.')
                        continue
                    # validate the data
                    openSWATH.validate(
                        params['MRMFeatureValidator.validate_MRMFeatures'],
                        verbose_I=verbose_I)
                    openSWATH.store_featureMap({
                        'featureXML_o': featureXML_o,
                        'feature_csv_o': feature_csv_o},
                        verbose_I=verbose_I)
                elif quantify_peaks or check_peaks:                   
                    try:
                        openSWATH.load_featureMap(
                            {'featureXML_i': featureXML_o},
                            verbose_I=verbose_I)
                    except Exception as e:
                        print(e)

                # Quantify peaks
                # dynamically make the filenames
                featureXML_o = '''%s/quantitation/%s.featureXML''' % (
                    sequence["meta_data"]["data_dir"],
                    sequence["meta_data"]["sample_name"]) 
                feature_csv_o = '''%s/quantitation/%s.csv''' % (
                    sequence["meta_data"]["data_dir"],
                    sequence["meta_data"]["sample_name"])
                if quantify_peaks:
                    quantitationMethods_csv_i = '''%s/quantitationMethods.csv''' % (
                        sequence["meta_data"]["data_dir"])
                    # load the quantitation method
                    AbsoluteQuantitation.load_quantitationMethods(
                        {'quantitationMethods_csv_i': quantitationMethods_csv_i},
                        verbose_I=verbose_I)
                    # quantify the components
                    AbsoluteQuantitation.setUnknowns(openSWATH.featureMap)
                    AbsoluteQuantitation.quantifyComponents(verbose_I=verbose_I)
                    # store
                    openSWATH.featureMap = AbsoluteQuantitation.getUnknowns()
                    openSWATH.store_featureMap({
                        'featureXML_o': featureXML_o,
                        'feature_csv_o': feature_csv_o},
                        verbose_I=verbose_I)
                elif check_peaks: 
                    try:
                        openSWATH.load_featureMap({'featureXML_i': featureXML_o})
                    except Exception as e:
                        # Peaks have not been quantified, try opening picked peaks
                        featureXML_o = '''%s/features/%s.featureXML''' % (
                            sequence["meta_data"]["data_dir"],
                            sequence["meta_data"]["sample_name"])
                        openSWATH.load_featureMap(
                            {'featureXML_i': featureXML_o},
                            verbose_I=verbose_I)

                # QC the peaks
                featureXML_o = '''%s/quantitation/%s.featureXML''' % (
                    sequence["meta_data"]["data_dir"],
                    sequence["meta_data"]["sample_name"]) 
                feature_csv_o = '''%s/quantitation/%s.csv''' % (
                    sequence["meta_data"]["data_dir"],
                    sequence["meta_data"]["sample_name"])
                if check_peaks:
                    mrmfeatureqcs_csv_i = '''%s/featureQCs.csv''' % (
                        sequence["meta_data"]["data_dir"])
                    openSWATH.filterAndSelect_py(
                        filenames_I={'mrmfeatureqcs_csv_i': mrmfeatureqcs_csv_i},
                        MRMFeatureFilter_filter_params_I=params[
                            'MRMFeatureFilter.filter_MRMFeatures.qc'],
                        # no selection
                        MRMFeatureSelector_select_params_I={},
                        MRMFeatureSelector_schedule_params_I={},
                        verbose_I=verbose_I
                    )
                    # store
                    openSWATH.store_featureMap({
                        'featureXML_o': featureXML_o,
                        'feature_csv_o': feature_csv_o},
                        verbose_I=verbose_I)

                # record features
                seqhandler.addFeatureMapToSequence(
                    sequence["meta_data"]["sample_name"], openSWATH.featureMap)
            except Exception as e:
                print(e)
                skipped_samples.append({
                    'sample_name': sequence["meta_data"]["sample_name"],
                    'error_message': e})
            # manual clear data for the next iteration
            openSWATH.clear_data()
        # export results
        if skipped_samples:
            smartpeak_o = FileWriter(skipped_samples)
            skippedSamples_csv_i = '''%s/mzML/skippedSamples.csv''' % (
                sequence["meta_data"]["data_dir"]
            )
            smartpeak_o.write_dict2csv(skippedSamples_csv_i)
        if validation_metrics:
            smartpeak_o = FileWriter(validation_metrics)
            validationMetrics_csv_i = '''%s/validation/validationMetrics.csv''' % (
                sequence["meta_data"]["data_dir"])
            smartpeak_o.write_dict2csv(validationMetrics_csv_i)
        sequenceSummary_csv_i = '''%s/SequenceSummary.csv''' % (
            sequence["meta_data"]["data_dir"])
        seqhandler.exportDataMatrixFromMetaValue(
            filename=sequenceSummary_csv_i,
            # meta_values=[
            # 'calculated_concentration','RT','peak_apex_int',
            # 'noise_background_level','leftWidth','rightWidth'],
            meta_values=['calculated_concentration'],
            sample_types=['Unknown']
        )