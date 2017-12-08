# -*- coding: utf-8 -*-
from .smartPeak import smartPeak
from .smartPeak_i import smartPeak_i
from .smartPeak_o import smartPeak_o


class __main__():

    def main(
            self,
            filename_filenames,
            filename_params,
            delimiter=',',
            pick_peaks=True,
            select_peaks=True,
            validate_peaks=False,
            quantify_peaks=True,
            check_peaks=False,
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
        from smartPeak.pyTOPP.SequenceHandler import SequenceHandler
        from smartPeak.core.smartPeak_openSWATH_py import smartPeak_openSWATH_py
        from smartPeak.core.smartPeak_AbsoluteQuantitation_py import \
            smartPeak_AbsoluteQuantitation_py

        # internal variables
        skipped_samples = []
        output = []
        validation_metrics = []

        # class initializations        
        seqhandler = SequenceHandler()
        AbsoluteQuantitation_py = smartPeak_AbsoluteQuantitation_py()
        openSWATH_py = smartPeak_openSWATH_py()
        smartpeak_i = smartPeak_i()

        # read in the files
        smartpeak_i.read_pythonParams(filename_filenames, delimiter)
        filenames = smartpeak_i.getData()
        smartpeak_i.clear_data()
        smartpeak_i.read_openMSParams(filename_params, delimiter)
        params = smartpeak_i.getData()
        smartpeak_i.clear_data()

        # check for updated workflow parameters
        if "run_AbsoluteQuantitation_py" in params:
            smartpeak = smartPeak()
            workflow_parameters = {
                d['name']: smartpeak.castString(d['value'], d['type'])
                for d in params["run_AbsoluteQuantitation_py"]}
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

        for sample, v in filenames.items():
            print("processing sample " + sample)
            try:
                
                # dynamically make the filenames
                data_dir = v['data_dir']
                mzML_i = '''%s/mzML/%s.mzML''' % (data_dir, sample)
                traML_csv_i = '''%s/traML.csv''' % (data_dir)
                # trafo_csv_i = '''%s/trafo.csv''' % (data_dir)
                db_ini_i = '''%s/settings.ini''' % (data_dir)

                # load in the files
                openSWATH_py.load_TraML({'traML_csv_i': traML_csv_i}, verbose_I=verbose_I)                
                openSWATH_py.load_SWATHorDIA({})
                openSWATH_py.load_MSExperiment(
                    {'mzML_feature_i': mzML_i},
                    MRMMapping_params_I=params['MRMMapping'],
                    chromatogramExtractor_params_I=params['ChromatogramExtractor'],
                    verbose_I=verbose_I)
                openSWATH_py.extract_metaData(verbose_I=verbose_I)
                openSWATH_py.meta_data['sample_type'] = 'Unknown'
                openSWATH_py.load_Trafo(  # skip transformation of RT
                    {},  # {'trafo_csv_i':trafo_csv_i},
                    params['MRMFeatureFinderScoring'],
                    verbose_I=verbose_I)

                # pick peaks with OpenSWATH
                featureXML_o = '''%s/features_tmp/%s.featureXML''' % (data_dir, sample) 
                feature_csv_o = '''%s/features_tmp/%s.csv''' % (data_dir, sample)
                if pick_peaks:
                    # run the openSWATH workflow for metabolomics
                    openSWATH_py.openSWATH_py(
                        params['MRMFeatureFinderScoring'],
                        verbose_I=verbose_I)
                    # store
                    openSWATH_py.store_featureMap({
                        'featureXML_o': featureXML_o,
                        'feature_csv_o': feature_csv_o},
                        verbose_I=verbose_I)
                elif select_peaks or validate_peaks or quantify_peaks or check_peaks:
                    try:
                        openSWATH_py.load_featureMap(
                            {'featureXML_i': featureXML_o},
                            verbose_I=verbose_I)
                    except Exception as e:
                        print(e)

                # Filter and select features
                mrmfeaturefilter_csv_i = '''%s/FeatureFilters.csv''' % (data_dir)
                featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, sample) 
                feature_csv_o = '''%s/features/%s.csv''' % (data_dir, sample)
                if select_peaks:
                    openSWATH_py.filterAndSelect_py(
                        filenames_I={'mrmfeatureqcs_csv_i': mrmfeaturefilter_csv_i},
                        MRMFeatureFilter_filter_params_I=params[
                            'MRMFeatureFilter.filter_MRMFeatures'],
                        # qmip algorithm
                        MRMFeatureSelector_select_params_I=params[
                            'MRMFeatureSelector.select_MRMFeatures_qmip'],
                        MRMFeatureSelector_schedule_params_I=params[
                            'MRMFeatureSelector.schedule_MRMFeatures_qmip'],
                        # score algorithm
                        # MRMFeatureSelector_select_params_I=params['MRMFeatureSelector.select_MRMFeatures_score'],
                        # MRMFeatureSelector_schedule_params_I={}
                        verbose_I=verbose_I
                    )
                    # store
                    openSWATH_py.store_featureMap({
                        'featureXML_o': featureXML_o,
                        'feature_csv_o': feature_csv_o},
                        verbose_I=verbose_I)
                elif validate_peaks or quantify_peaks or check_peaks:        
                    try:
                        openSWATH_py.load_featureMap(
                            {'featureXML_i': featureXML_o},
                            verbose_I=verbose_I)
                    except Exception as e:
                        print(e)

                # Validate peaks
                # dynamically make the filenames
                featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, sample) 
                feature_csv_o = '''%s/features/%s.csv''' % (data_dir, sample)
                if validate_peaks:
                    # load in the validation data 
                    # (if no data is found, continue to the next sample)
                    ReferenceDataMethods_params_I = []
                    ReferenceDataMethods_params_I.extend(
                        params['ReferenceDataMethods.getAndProcess_referenceData_samples']
                        )
                    sample_names_I = '''['%s']''' % (sample)
                    ReferenceDataMethods_params_I.append({
                        'description': '', 'name': 'sample_names_I', 
                        'type': 'list', 'value': sample_names_I})
                    openSWATH_py.load_validationData(
                        {'db_ini_i': db_ini_i},
                        ReferenceDataMethods_params_I,
                        verbose_I=verbose_I
                        )
                    if not openSWATH_py.reference_data:
                        skipped_samples.append({
                            'sample_name': sample,
                            'error_message': 'no reference data found'})
                        print('Reference data not found for sample ' + sample + '.')
                        continue
                    # validate the data
                    openSWATH_py.validate_py(
                        params['MRMFeatureValidator.validate_MRMFeatures'],
                        verbose_I=verbose_I)
                    openSWATH_py.store_featureMap({
                        'featureXML_o': featureXML_o,
                        'feature_csv_o': feature_csv_o},
                        verbose_I=verbose_I)
                elif quantify_peaks or check_peaks:                   
                    try:
                        openSWATH_py.load_featureMap(
                            {'featureXML_i': featureXML_o},
                            verbose_I=verbose_I)
                    except Exception as e:
                        print(e)

                # Quantify peaks
                # dynamically make the filenames
                quantitationMethods_csv_i = '''%s/quantitationMethods.csv''' % (data_dir)
                featureXML_o = '''%s/quantitation/%s.featureXML''' % (data_dir, sample) 
                feature_csv_o = '''%s/quantitation/%s.csv''' % (data_dir, sample)
                if quantify_peaks:
                    # load the quantitation method
                    AbsoluteQuantitation_py.load_quantitationMethods(
                        {'quantitationMethods_csv_i': quantitationMethods_csv_i},
                        verbose_I=verbose_I)
                    # quantify the components
                    AbsoluteQuantitation_py.setUnknowns(openSWATH_py.featureMap)
                    AbsoluteQuantitation_py.quantifyComponents(verbose_I=verbose_I)
                    # store
                    openSWATH_py.featureMap = AbsoluteQuantitation_py.getUnknowns()
                    openSWATH_py.store_featureMap({
                        'featureXML_o': featureXML_o,
                        'feature_csv_o': feature_csv_o},
                        verbose_I=verbose_I)
                elif check_peaks: 
                    try:
                        openSWATH_py.load_featureMap({'featureXML_i': featureXML_o})
                    except Exception as e:
                        # Peaks have not been quantified, try opening picked peaks
                        featureXML_o = '''%s/features/%s.featureXML''' % (
                            data_dir, sample)
                        openSWATH_py.load_featureMap(
                            {'featureXML_i': featureXML_o},
                            verbose_I=verbose_I)

                # QC the peaks
                mrmfeatureqcs_csv_i = '''%s/FeatureQCs.csv''' % (data_dir)
                featureXML_o = '''%s/quantitation/%s.featureXML''' % (data_dir, sample) 
                feature_csv_o = '''%s/quantitation/%s.csv''' % (data_dir, sample)
                if check_peaks:
                    openSWATH_py.filterAndSelect_py(
                        filenames_I={'mrmfeatureqcs_csv_i': mrmfeatureqcs_csv_i},
                        MRMFeatureFilter_filter_params_I=params[
                            'MRMFeatureFilter.filter_MRMFeatures.qc'],
                        # no selection
                        MRMFeatureSelector_select_params_I={},
                        MRMFeatureSelector_schedule_params_I={},
                        verbose_I=verbose_I
                    )
                    # store
                    openSWATH_py.store_featureMap({
                        'featureXML_o': featureXML_o,
                        'feature_csv_o': feature_csv_o},
                        verbose_I=verbose_I)

                # record features
                seqhandler.addSampleToSequence(
                    openSWATH_py.meta_data, openSWATH_py.featureMap)
            except Exception as e:
                print(e)
                skipped_samples.append({
                    'sample_name': sample,
                    'error_message': e})
            # manual clear data for the next iteration
            openSWATH_py.clear_data()
        # export results
        if skipped_samples:
            smartpeak_o = smartPeak_o(skipped_samples)
            skippedSamples_csv_i = '''%s/mzML/skippedSamples.csv''' % (data_dir)
            smartpeak_o.write_dict2csv(skippedSamples_csv_i)
        if validation_metrics:
            smartpeak_o = smartPeak_o(validation_metrics)
            validationMetrics_csv_i = '''%s/validation/validationMetrics.csv''' % (
                data_dir)
            smartpeak_o.write_dict2csv(validationMetrics_csv_i)
        sequenceSummary_csv_i = '''%s/SequenceSummary.csv''' % (data_dir)
        seqhandler.exportDataMatrixFromMetaValue(
            filename=sequenceSummary_csv_i,
            # meta_values=[
            # 'calculated_concentration','RT','peak_apex_int',
            # 'noise_background_level','leftWidth','rightWidth'],
            meta_values=['calculated_concentration'],
            sample_types=['Unknown']
        )
        return output