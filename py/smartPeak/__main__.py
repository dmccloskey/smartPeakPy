# -*- coding: utf-8 -*-
from .smartPeak import smartPeak
from .smartPeak_i import smartPeak_i
from .smartPeak_o import smartPeak_o

class __main__():
    def run_openSWATH_cmd(
            self,
            filename,
            verbose=True):
        """Run the openSWATH commandline pipeline
        
        Args:
            filename (str): name of the workflow parameter filename
            verbose (bool): print command line statements to stdout
            
        Eamples:        
            from smartPeak.__main__ import __main__
            m = __main__()    
            filename='C:/Users/domccl/Dropbox (UCSD SBRG)/Project_FastPeak/openMS_MRMworkflow/openSWATH_cmd_params.csv',
            filename='/home/user/openMS_MRMworkflow/openSWATH_cmd_params.csv'
            m.run_openSWATH_cmd(filename);
            
        """
        from .smartPeak_openSWATH_cmd import smartPeak_openSWATH_cmd
        openSWATH_cmd = smartPeak_openSWATH_cmd()
        openSWATH_cmd.read_openSWATH_cmd_params(filename)
        openSWATH_cmd.openSWATH_cmd(verbose_I=verbose)

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
            
        """
        validation_metrics = []
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
                openSWATH_py.load_MSExperiment(v)
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
                # validate the data
                # openSWATH_py.load_featureMap(v)
                openSWATH_py.load_validationData(
                    v,
                    params['ReferenceDataMethods.getAndProcess_referenceData_samples']
                    )
                openSWATH_py.validate_py(params['MRMFeatureValidator.validate_MRMFeatures'])
                # store
                openSWATH_py.store_featureMap(v)
                tmp = {}
                tmp.update(openSWATH_py.validation_metrics)
                tmp.update({'sample_name':sample})
                validation_metrics.append(tmp)
                # manual clear data for the next iteration
                openSWATH_py.clear_data()

    def convert_MQQMethod2Feature(self,filename_I,filename_O):
        """Convert MultiQuant QMethod file to feature.csv file
        
        """
        smartpeak_i = smartPeak_i()
        smartpeak_i.read_csv(filename_I,delimiter=',')
        MQQMethod = smartpeak_i.getData()
        smartpeak_i.clear_data()

        smartpeak = smartPeak()
        features = smartpeak.convert_MQQMethod2Feature(MQQMethod)
        headers = ['ProteinName',
            'FullPeptideName',
            'transition_group_id',
            'transition_name',
            'Tr_recalibrated',
            'Annotation',
            'RetentionTime',
            'PrecursorMz',
            'MS1 Res',
            'ProductMz',
            'MS2 Res',
            'Dwell',
            'Fragmentor',
            'Collision Energy',
            'Cell Accelerator Voltage',
            'LibraryIntensity',
            'decoy',
            'PeptideSequence',
            'LabelType',
            'PrecursorCharge',
            'FragmentCharge',
            'FragmentType',
            'FragmentSeriesNumber'
        ]
        smartpeak_o = smartPeak_o(features)
        smartpeak_o.write_dict2csv(filename_O,headers=headers)
        
    def run_validate_openSWATH(self,
        filename_filenames='',
        filename_params='',
        delimiter=','):
        """
        Args

        Returns

        Example

        """
        from .pyTOPP.MRMFeatureValidator import MRMFeatureValidator
        featureValidator= MRMFeatureValidator()
        from .pyTOPP.OpenSwathFeatureXMLToTSV import OpenSwathFeatureXMLToTSV
        featurescsv = OpenSwathFeatureXMLToTSV()
        from .smartPeak_openSWATH_py import smartPeak_openSWATH_py
        try:
            import pyopenms
        except ImportError as e:
            print(e)
        # openSWATH_py = smartPeak_openSWATH_py()
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
                # read in the FeatureMap
                features = pyopenms.FeatureMap()
                featurexml = pyopenms.FeatureXMLFile()
                featurexml.load(v['featureXML_i'].encode('utf-8'), features)
                # read in the reference data
                smartpeak_i.read_csv(v['referenceData_csv_i'],delimiter)
                # smartpeak_i.read_csv(v['calibrators_csv_i'],delimiter)
                data_ref = smartpeak_i.getData()
                smartpeak_i.clear_data()
                # map the reference data
                features_mapped,validation_metrics = featureValidator.validate_MRMFeatures(
                    reference_data = data_ref,
                    features = features,
                    Tr_window = float(params['validate_MRMFeatures'][0]['value'])
                    )
                # load and make the transition file
                targeted = pyopenms.TargetedExperiment() #must use "PeptideSequence"
                tramlfile = pyopenms.TransitionTSVReader()
                tramlfile.convertTSVToTargetedExperiment(v['traML_csv_i'].encode('utf-8'),21,targeted)
                # export the mapped features
                featurescsv.store(v['referenceData_mapped_csv_o'], features_mapped, targeted,
                    run_id = "",
                    filename = ""
                    )
                ##accuracy: 0.982035928144

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
        for filename in filenames:
            for sample,v in filename.items():
                print("processing sample "+ sample)
                try:
                    # dynamically make the filenames
                    data_dir = v['data_dir']
                    mzML_I = '''/home/user/mzML_validationData/%s.mzML'''%(sample)
                    traML_csv_i = '''%s/traML.csv'''%(data_dir)
                    trafo_csv_i = '''%s/trafo.csv'''%(data_dir)
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
                    openSWATH_py.load_MSExperiment({'mzML_feature_i':mzML_I})
                    openSWATH_py.load_Trafo(
                        {'trafo_csv_i':trafo_csv_i},
                        params['MRMFeatureFinderScoring'])
                    # run the openSWATH workflow for metabolomics
                    openSWATH_py.openSWATH_py(
                        params['MRMFeatureFinderScoring'])
                    openSWATH_py.filterAndSelect_py(
                        {},
                        params['MRMFeatureFilter.filter_MRMFeatures'],
                        #{},#
                        params['MRMFeatureSelector.select_MRMFeatures_score'],
                        params['MRMFeatureSelector.schedule_MRMFeatures_qmip'])
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
                # export the data at period intervals
                cnt += 1
                if cnt > 10:
                    if validation_metrics:
                        smartpeak_o = smartPeak_o(validation_metrics)
                        validationMetrics_csv_i = '''/home/user/openMS_MRMworkflow/Algo1Validation/validationMetrics_%s.csv'''%batch_cnt
                        smartpeak_o.write_dict2csv(validationMetrics_csv_i)
                    if skipped_samples:
                        smartpeak_o = smartPeak_o(skipped_samples)
                        skippedSamples_csv_i = '''/home/user/openMS_MRMworkflow/Algo1Validation/skippedSamples_%s.csv'''%batch_cnt
                        smartpeak_o.write_dict2csv(skippedSamples_csv_i)
                    cnt = 0
                    batch_cnt += 1
        if validation_metrics:
            smartpeak_o = smartPeak_o(validation_metrics)
            validationMetrics_csv_i = '''/home/user/openMS_MRMworkflow/Algo1Validation/validationMetrics.csv'''
            smartpeak_o.write_dict2csv(validationMetrics_csv_i)
        if skipped_samples:
            smartpeak_o = smartPeak_o(skipped_samples)
            skippedSamples_csv_i = '''/home/user/openMS_MRMworkflow/Algo1Validation/skippedSamples.csv'''
            smartpeak_o.write_dict2csv(skippedSamples_csv_i)