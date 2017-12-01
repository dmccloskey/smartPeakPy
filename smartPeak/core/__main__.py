# -*- coding: utf-8 -*-
from .smartPeak import smartPeak
from .smartPeak_i import smartPeak_i
from .smartPeak_o import smartPeak_o

class __main__():

    def run_PeakPickerMRM_py(
            self,
            filename_filenames,
            filename_params,
            delimiter = ','
            ):
        """Run the PeakPickerMRM python pipeline
        
        Args:
            filename (str): name of the workflow parameter filename
            verbose (bool): print command line statements to stdout
            
        Examples:
            
        """
        from .smartPeak_PeakPickerMRM_py import smartPeak_PeakPickerMRM_py
        PeakPickerMRM_py = smartPeak_PeakPickerMRM_py()
        smartpeak_i = smartPeak_i()
        smartpeak_i.read_pythonParams(filename_filenames,delimiter)
        filenames = smartpeak_i.getData()
        smartpeak_i.clear_data()
        smartpeak_i.read_openMSParams(filename_params,delimiter)
        params = smartpeak_i.getData()
        smartpeak_i.clear_data()
        for filename in filenames:
            for sample,v in filename.items():
                print("processing sample "+ sample)
                PeakPickerMRM_py.PeakPickerMRM_py(v,params['PeakPickerMRM'])

    def run_MRMTransitionGroupPicker_py(
            self,
            filename_filenames,
            filename_params,
            delimiter = ','
            ):
        """Run the MRMTransitionGroupPicker python pipeline
        
        Args:
            filename (str): name of the workflow parameter filename
            verbose (bool): print command line statements to stdout
            
        Examples:
            
        """
        from .smartPeak_MRMTransitionGroupPicker_py import smartPeak_MRMTransitionGroupPicker_py
        MRMTransitionGroupPicker_py = smartPeak_MRMTransitionGroupPicker_py()
        smartpeak_i = smartPeak_i()
        smartpeak_i.read_pythonParams(filename_filenames,delimiter)
        filenames = smartpeak_i.getData()
        smartpeak_i.clear_data()
        smartpeak_i.read_openMSParams(filename_params,delimiter)
        params = smartpeak_i.getData()
        smartpeak_i.clear_data()
        for filename in filenames:
            for sample,v in filename.items():
                print("processing sample "+ sample)
                MRMTransitionGroupPicker_py.MRMTransitionGroupPicker_py(
                    v,params['MRMTransitionGroupPicker'],
                    params['MRMFeatureFinderScoring']
                    )

    def run_openSWATH_py(
            self,
            filename_filenames,
            filename_params,
            delimiter = ','
            ):
        """Run the openSWATH python pipeline
        
        Args:
            filename (str): name of the workflow parameter filename
            verbose (bool): print command line statements to stdout

        Returns:
            list: output: list of featuremaps
            
        """
        output = []
        from .smartPeak_openSWATH_py import smartPeak_openSWATH_py
        openSWATH_py = smartPeak_openSWATH_py()
        smartpeak_i = smartPeak_i()
        smartpeak_i.read_pythonParams(filename_filenames,delimiter)
        filenames = smartpeak_i.getData()
        smartpeak_i.clear_data()
        smartpeak_i.read_openMSParams(filename_params,delimiter)
        params = smartpeak_i.getData()
        smartpeak_i.clear_data()
        for filename in filenames:
            for sample,v in filename.items():
                print("processing sample "+ sample)
                # load in the files
                openSWATH_py.load_TraML(v)
                openSWATH_py.load_MSExperiment(v,
                    True,
                    params['MRMMapping'])
                openSWATH_py.load_Trafo(v,
                    params['MRMFeatureFinderScoring'])
                openSWATH_py.load_SWATHorDIA({})
                # run the openSWATH workflow for metabolomics
                openSWATH_py.openSWATH_py(
                    params['MRMFeatureFinderScoring'])
                openSWATH_py.filterAndSelect_py(
                    v,
                    params['MRMFeatureFilter.filter_MRMFeatures'],
                    params['MRMFeatureSelector.select_MRMFeatures_score'],
                    params['MRMFeatureSelector.schedule_MRMFeatures_qmip'])
                # store
                openSWATH_py.store_featureMap(v)
                output.append(openSWATH_py.featureMap)
                # manual clear data for the next iteration
                openSWATH_py.clear_data()

    def run_openSWATH_validation_py(
            self,
            filename_filenames,
            filename_params,
            delimiter = ','
            ):
        """Run the openSWATH python pipeline
        
        Args:
            filename (str): name of the workflow parameter filename
            verbose (bool): print command line statements to stdout
            
        TODO:
            make new method: run_openSWATH_validation_py
            
        """
        validation_metrics = []
        skipped_samples = []
        from .smartPeak_openSWATH_py import smartPeak_openSWATH_py
        openSWATH_py = smartPeak_openSWATH_py()

        smartpeak_i = smartPeak_i()
        smartpeak_i.read_pythonParams(filename_filenames,delimiter)
        filenames = smartpeak_i.getData()
        smartpeak_i.clear_data()
        smartpeak_i.read_openMSParams(filename_params,delimiter)
        params = smartpeak_i.getData()
        smartpeak_i.clear_data()

        cnt = 0
        batch_cnt = 0
        for sample,v in filenames.items():
            print("processing sample "+ sample)
            try:
                # dynamically make the filenames
                data_dir = v['data_dir']
                # mzML_I = '''/home/user/mzML_validationData/%s.mzML'''%(sample)
                mzML_I = '''%s/mzML/%s.mzML'''%(data_dir,sample) 
                traML_csv_i = '''%s/traML.csv'''%(data_dir)
                trafo_csv_i = '''%s/trafo.csv'''%(data_dir)
                mrmfeatureqcs_csv_i = '''%s/%s'''%(data_dir,v["mrmfeatureqcs_csv_i"])
                db_ini_i = '''%s/settings_metabolomics.ini'''%(data_dir)
                featureXML_o = '''%s/features/%s.featureXML'''%(data_dir,sample) 
                feature_csv_o = '''%s/features/%s.csv'''%(data_dir,sample)
                # load in the validation data (if no data is found, continue to the next sample)
                ReferenceDataMethods_params_I = []
                ReferenceDataMethods_params_I.extend(params['ReferenceDataMethods.getAndProcess_referenceData_samples'])
                sample_names_I = '''['%s']'''%(sample)
                ReferenceDataMethods_params_I.append({'description': '', 'name': 'sample_names_I', 'type': 'list', 'value': sample_names_I})
                openSWATH_py.load_validationData(
                    {'db_ini_i':db_ini_i},
                    ReferenceDataMethods_params_I
                    )
                if not openSWATH_py.reference_data:
                    skipped_samples.append({'sample_name':sample,
                        'error_message':'no reference data found'})
                    print('Reference data not found for sample ' + sample + '.')
                    continue
                # load in the files
                openSWATH_py.load_TraML({'traML_csv_i':traML_csv_i})
                openSWATH_py.load_SWATHorDIA({})
                openSWATH_py.load_MSExperiment({'mzML_feature_i':mzML_I},
                    True,
                    params['MRMMapping'])
                openSWATH_py.extract_metaData()
                openSWATH_py.load_Trafo(
                    {},#{'trafo_csv_i':trafo_csv_i},
                    params['MRMFeatureFinderScoring'])
                # run the openSWATH workflow for metabolomics
                openSWATH_py.openSWATH_py(
                    params['MRMFeatureFinderScoring'])
                # Filter and select
                openSWATH_py.filterAndSelect_py(
                    filenames_I={'mrmfeatureqcs_csv_i':mrmfeatureqcs_csv_i},
                    MRMFeatureFilter_filter_params_I=params['MRMFeatureFilter.filter_MRMFeatures'],
                    MRMFeatureSelector_select_params_I=params['MRMFeatureSelector.select_MRMFeatures_qmip'],
                    MRMFeatureSelector_schedule_params_I=params['MRMFeatureSelector.schedule_MRMFeatures_qmip'])
                # openSWATH_py.filterAndSelect_py(
                #     filenames_I={'mrmfeatureqcs_csv_i':mrmfeatureqcs_csv_i},
                #     MRMFeatureFilter_filter_params_I=params['MRMFeatureFilter.filter_MRMFeatures'],
                #     MRMFeatureSelector_select_params_I=params['MRMFeatureSelector.select_MRMFeatures_score'],
                #     MRMFeatureSelector_schedule_params_I={})
                # store
                openSWATH_py.store_featureMap(
                    {'featureXML_o':featureXML_o,
                    'feature_csv_o':feature_csv_o})
                # validate the data
                # openSWATH_py.load_featureMap({'featureXML_i':featureXML_o})
                openSWATH_py.validate_py(params['MRMFeatureValidator.validate_MRMFeatures'])
                # store
                openSWATH_py.store_featureMap(
                    {'featureXML_o':featureXML_o,
                    'feature_csv_o':feature_csv_o})
                tmp = {}
                tmp.update(openSWATH_py.validation_metrics)
                tmp.update({'sample_name':sample})
                validation_metrics.append(tmp)
            except Exception as e:
                print(e)
                skipped_samples.append({'sample_name':sample,
                    'error_message':e})
            # manual clear data for the next iteration
            openSWATH_py.clear_data()
            # # export the data at period intervals
            # cnt += 1
            # if cnt > 10:
            #     if validation_metrics:
            #         smartpeak_o = smartPeak_o(validation_metrics)
            #         validationMetrics_csv_i = '''/home/user/openMS_MRMworkflow/Algo1Validation/validationMetrics_%s.csv'''%batch_cnt
            #         smartpeak_o.write_dict2csv(validationMetrics_csv_i)
            #     if skipped_samples:
            #         smartpeak_o = smartPeak_o(skipped_samples)
            #         skippedSamples_csv_i = '''/home/user/openMS_MRMworkflow/Algo1Validation/skippedSamples_%s.csv'''%batch_cnt
            #         smartpeak_o.write_dict2csv(skippedSamples_csv_i)
            #     cnt = 0
            #     batch_cnt += 1
        if validation_metrics:
            smartpeak_o = smartPeak_o(validation_metrics)
            validationMetrics_csv_i = '''%s/validation/validationMetrics.csv'''%(data_dir)
            smartpeak_o.write_dict2csv(validationMetrics_csv_i)
        if skipped_samples:
            smartpeak_o = smartPeak_o(skipped_samples)
            skippedSamples_csv_i = '''%s/validation/skippedSamples.csv'''%(data_dir)
            smartpeak_o.write_dict2csv(skippedSamples_csv_i)

    def run_openSWATH_py(
            self,
            filename_filenames,
            filename_params,
            delimiter = ','
            ):
        """Run the openSWATH python pipeline
        
        Args:
            filename (str): name of the workflow parameter filename
            verbose (bool): print command line statements to stdout

        Returns:
            list: output: list of featuremaps
            
        """
        output = []
        skipped_samples = []

        from .smartPeak_openSWATH_py import smartPeak_openSWATH_py
        openSWATH_py = smartPeak_openSWATH_py()
        smartpeak_i = smartPeak_i()
        smartpeak_i.read_pythonParams(filename_filenames,delimiter)
        filenames = smartpeak_i.getData()
        smartpeak_i.clear_data()
        smartpeak_i.read_openMSParams(filename_params,delimiter)
        params = smartpeak_i.getData()
        smartpeak_i.clear_data()
        for sample,v in filenames.items():
            print("processing sample "+ sample)
            try:
                ## OPTION 1: filenames defined in .csv file
                # # load in the files
                # openSWATH_py.load_TraML(v)
                # openSWATH_py.load_MSExperiment(v,
                #     map_chromatograms_I = True,
                #     MRMMapping_params_I = params['MRMMapping'])
                # openSWATH_py.load_Trafo(v,
                #     params['MRMFeatureFinderScoring'])
                # openSWATH_py.load_SWATHorDIA({})
                # # run the openSWATH workflow for metabolomics
                # openSWATH_py.openSWATH_py(
                #     params['MRMFeatureFinderScoring'])
                # openSWATH_py.filterAndSelect_py(
                #     v,
                #     params['MRMFeatureFilter.filter_MRMFeatures'],
                #     params['MRMFeatureSelector.select_MRMFeatures_score'],
                #     params['MRMFeatureSelector.schedule_MRMFeatures_qmip'])
                # # store
                # openSWATH_py.store_featureMap(v)

                ## OPTION 2: dynamically make the filenames
                data_dir = v['data_dir']
                mzML_I = '''%s/data/%s.mzML'''%(data_dir,sample)
                traML_csv_i = '''%s/traML.csv'''%(data_dir)
                trafo_csv_i = '''%s/trafo.csv'''%(data_dir)
                mrmfeatureqcs_csv_i = '''%s/%s'''%(data_dir,v["mrmfeatureqcs_csv_i"])
                featureXML_o = '''%s/features/%s.featureXML'''%(data_dir,sample) 
                feature_csv_o = '''%s/features/%s.csv'''%(data_dir,sample)
                # load in the files
                openSWATH_py.load_TraML({'traML_csv_i':traML_csv_i})
                openSWATH_py.load_SWATHorDIA({})
                openSWATH_py.load_MSExperiment({'mzML_feature_i':mzML_I},
                    True,
                    params['MRMMapping'])
                openSWATH_py.extract_metaData()
                openSWATH_py.load_Trafo( #skip transformation of RT
                    {},#{'trafo_csv_i':trafo_csv_i},
                    params['MRMFeatureFinderScoring'])
                # run the openSWATH workflow for metabolomics
                openSWATH_py.openSWATH_py(
                    params['MRMFeatureFinderScoring'])
                openSWATH_py.filterAndSelect_py(
                    {'mrmfeatureqcs_csv_i':mrmfeatureqcs_csv_i},
                    params['MRMFeatureFilter.filter_MRMFeatures'],
                    params['MRMFeatureSelector.select_MRMFeatures_qmip'],
                    params['MRMFeatureSelector.schedule_MRMFeatures_qmip'])
                # store
                openSWATH_py.store_featureMap(
                    {'featureXML_o':featureXML_o,
                    'feature_csv_o':feature_csv_o})
                output.append(openSWATH_py.featureMap)
                # manual clear data for the next iteration
                openSWATH_py.clear_data()
            except Exception as e:
                print(e)
                skipped_samples.append({'sample_name':sample,
                    'error_message':e})
        if skipped_samples:
            smartpeak_o = smartPeak_o(skipped_samples)
            skippedSamples_csv_i = '''%s/data/skippedSamples.csv'''%(data_dir)
            smartpeak_o.write_dict2csv(skippedSamples_csv_i)
        return output

    def run_AbsoluteQuantitation_py(
            self,
            filename_filenames,
            filename_params,
            delimiter = ',',
            pick_peaks = True,
            select_peaks = True,
            validate_peaks = False,
            quantify_peaks = True,
            check_peaks = False,
            ):
        """Run the AbsoluteQuantitation python pipeline
        
        Args:
            filename (str): name of the workflow parameter filename
            verbose (bool): print command line statements to stdout
            
        TODO:
            remove run_openSWATH and run_openSWATH_validation
            
        """
        from smartPeak.pyTOPP.SequenceHandler import SequenceHandler
        seqhandler = SequenceHandler()

        skipped_samples = []
        output = []
        validation_metrics = []

        from smartPeak.core.smartPeak_openSWATH_py import smartPeak_openSWATH_py
        from smartPeak.core.smartPeak_AbsoluteQuantitation_py import smartPeak_AbsoluteQuantitation_py
        AbsoluteQuantitation_py = smartPeak_AbsoluteQuantitation_py()
        openSWATH_py = smartPeak_openSWATH_py()
        smartpeak_i = smartPeak_i()
        smartpeak_i.read_pythonParams(filename_filenames,delimiter)
        filenames = smartpeak_i.getData()
        smartpeak_i.clear_data()
        smartpeak_i.read_openMSParams(filename_params,delimiter)
        params = smartpeak_i.getData()
        smartpeak_i.clear_data()
        for sample,v in filenames.items():
            print("processing sample "+ sample)
            try:
                ## pick peaks with OpenSWATH
                # dynamically make the filenames
                data_dir = v['data_dir']
                mzML_i = '''%s/mzML/%s.mzML'''%(data_dir,sample)
                traML_csv_i = '''%s/traML.csv'''%(data_dir)
                trafo_csv_i = '''%s/trafo.csv'''%(data_dir)
                # load in the files
                openSWATH_py.load_TraML({'traML_csv_i':traML_csv_i})
                openSWATH_py.load_SWATHorDIA({})
                openSWATH_py.load_MSExperiment({'mzML_feature_i':mzML_i},
                    map_chromatograms_I = True,
                    MRMMapping_params_I = params['MRMMapping'])
                openSWATH_py.extract_metaData()
                openSWATH_py.meta_data['sample_type'] = 'Unknown'
                openSWATH_py.load_Trafo( #skip transformation of RT
                    {},#{'trafo_csv_i':trafo_csv_i},
                    params['MRMFeatureFinderScoring'])
                    
                featureXML_o = '''%s/features_tmp/%s.featureXML'''%(data_dir,sample) 
                feature_csv_o = '''%s/features_tmp/%s.csv'''%(data_dir,sample)
                if pick_peaks:
                    # run the openSWATH workflow for metabolomics
                    openSWATH_py.openSWATH_py(
                        params['MRMFeatureFinderScoring'])
                    # store
                    openSWATH_py.store_featureMap(
                        {'featureXML_o':featureXML_o,
                        'feature_csv_o':feature_csv_o})
                else:
                    openSWATH_py.load_featureMap({'featureXML_i':featureXML_o})

                ## Filter and select features
                mrmfeaturefilter_csv_i = '''%s/FeatureFilters.csv'''%(data_dir)
                featureXML_o = '''%s/features/%s.featureXML'''%(data_dir,sample) 
                feature_csv_o = '''%s/features/%s.csv'''%(data_dir,sample)
                if select_peaks:
                    openSWATH_py.filterAndSelect_py(
                        filenames_I={'mrmfeatureqcs_csv_i':mrmfeaturefilter_csv_i},
                        MRMFeatureFilter_filter_params_I=params['MRMFeatureFilter.filter_MRMFeatures'],
                        # qmip algorithm
                        MRMFeatureSelector_select_params_I=params['MRMFeatureSelector.select_MRMFeatures_qmip'],
                        MRMFeatureSelector_schedule_params_I=params['MRMFeatureSelector.schedule_MRMFeatures_qmip']
                        # score algorithm
                        # MRMFeatureSelector_select_params_I=params['MRMFeatureSelector.select_MRMFeatures_score'],
                        # MRMFeatureSelector_schedule_params_I={}
                    )
                    # store
                    openSWATH_py.store_featureMap(
                        {'featureXML_o':featureXML_o,
                        'feature_csv_o':feature_csv_o})
                else:                    
                    openSWATH_py.load_featureMap({'featureXML_i':featureXML_o})

                ## Validate peaks
                # dynamically make the filenames
                featureXML_o = '''%s/features/%s.featureXML'''%(data_dir,sample) 
                feature_csv_o = '''%s/features/%s.csv'''%(data_dir,sample)
                if validate_peaks:
                    # load in the validation data (if no data is found, continue to the next sample)
                    ReferenceDataMethods_params_I = []
                    ReferenceDataMethods_params_I.extend(params['ReferenceDataMethods.getAndProcess_referenceData_samples'])
                    sample_names_I = '''['%s']'''%(sample)
                    ReferenceDataMethods_params_I.append({'description': '', 'name': 'sample_names_I', 'type': 'list', 'value': sample_names_I})
                    openSWATH_py.load_validationData(
                        {'db_ini_i':db_ini_i},
                        ReferenceDataMethods_params_I
                        )
                    if not openSWATH_py.reference_data:
                        skipped_samples.append({'sample_name':sample,
                            'error_message':'no reference data found'})
                        print('Reference data not found for sample ' + sample + '.')
                        continue
                    # validate the data
                    openSWATH_py.validate_py(params['MRMFeatureValidator.validate_MRMFeatures'])
                    openSWATH_py.store_featureMap(
                        {'featureXML_o':featureXML_o,
                        'feature_csv_o':feature_csv_o})
                else:
                    openSWATH_py.load_featureMap({'featureXML_i':featureXML_o})

                ## Quantify peaks
                # dynamically make the filenames
                quantitationMethods_csv_i = '''%s/quantitationMethods.csv'''%(data_dir)
                featureXML_o = '''%s/quantitation/%s.featureXML'''%(data_dir,sample) 
                feature_csv_o = '''%s/quantitation/%s.csv'''%(data_dir,sample)
                if quantify_peaks:
                    # load the quantitation method
                    AbsoluteQuantitation_py.load_quantitationMethods(
                        {'quantitationMethods_csv_i':quantitationMethods_csv_i})
                    # quantify the components
                    AbsoluteQuantitation_py.setUnknowns(openSWATH_py.featureMap)
                    AbsoluteQuantitation_py.quantifyComponents()
                    # store
                    openSWATH_py.featureMap = AbsoluteQuantitation_py.getUnknowns()
                    openSWATH_py.store_featureMap(
                        {'featureXML_o':featureXML_o,
                        'feature_csv_o':feature_csv_o})
                else:
                    openSWATH_py.load_featureMap({'featureXML_i':featureXML_o})

                ## QC the peaks
                mrmfeatureqcs_csv_i = '''%s/FeatureQCs.csv'''%(data_dir)
                featureXML_o = '''%s/quantitation/%s.featureXML'''%(data_dir,sample) 
                feature_csv_o = '''%s/quantitation/%s.csv'''%(data_dir,sample)
                if check_peaks:
                    openSWATH_py.filterAndSelect_py(
                        filenames_I={'mrmfeatureqcs_csv_i':mrmfeatureqcs_csv_i},
                        MRMFeatureFilter_filter_params_I=params['MRMFeatureFilter.filter_MRMFeatures.qc'],
                        # no selection
                        MRMFeatureSelector_select_params_I={},
                        MRMFeatureSelector_schedule_params_I={}
                    )
                    # store
                    openSWATH_py.store_featureMap(
                        {'featureXML_o':featureXML_o,
                        'feature_csv_o':feature_csv_o})
                else:
                    openSWATH_py.load_featureMap({'featureXML_i':featureXML_o})

                # record features
                seqhandler.addSampleToSequence(openSWATH_py.meta_data,openSWATH_py.featureMap)
            except Exception as e:
                print(e)
                skipped_samples.append({'sample_name':sample,
                    'error_message':e})
            # manual clear data for the next iteration
            openSWATH_py.clear_data()
        # export results
        if skipped_samples:
            smartpeak_o = smartPeak_o(skipped_samples)
            skippedSamples_csv_i = '''%s/mzML/skippedSamples.csv'''%(data_dir)
            smartpeak_o.write_dict2csv(skippedSamples_csv_i)
        if validation_metrics:
            smartpeak_o = smartPeak_o(validation_metrics)
            validationMetrics_csv_i = '''%s/validation/validationMetrics.csv'''%(data_dir)
            smartpeak_o.write_dict2csv(validationMetrics_csv_i)
        sequenceSummary_csv_i = '''%s/SequenceSummary.csv'''%(data_dir)
        seqhandler.exportDataMatrixFromMetaValue(
            filename = sequenceSummary_csv_i,
            meta_values = ['calculated_concentration','RT','peak_apex_int','noise_background_level','leftWidth','rightWidth'],
            # meta_values = ['calculated_concentration'],
            sample_types = ['Unknown']
        )
        return output