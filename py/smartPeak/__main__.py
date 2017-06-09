# coding: utf-8
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
            
        Eamples:
            
        """
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
                openSWATH_py.openSWATH_py(
                    v,
                    params['MRMFeatureFinderScoring'],
                    params['MRMFeatureFilter.filter_MRMFeatures'],
                    params['MRMFeatureFilter.select_MRMFeatures'])

    def run_testSmartPeak(self):
        from .test_smartPeak import test_smartPeak
        tests = test_smartPeak()
        tests.test_parseString()

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

    def run_get_referenceData(self,
        experiment_ids_I = [],
        sample_names_I = [],
        acquisition_methods_I = [],
        component_names_I = [],
        component_group_names_I = [],
        where_clause_I = '',
        used__I = True,
        experiment_limit_I = 10000,
        mqresultstable_limit_I = 1000000,
        settings_filename_I = 'settings.ini',
        data_filename_O = ''):
        """
        Args

        Returns

        Example

        """
        import time as time
        # DB settings
        from SBaaS_base.postgresql_settings import postgresql_settings
        from SBaaS_base.postgresql_orm import postgresql_orm
        pg_settings = postgresql_settings(settings_filename_I)
        pg_orm = postgresql_orm()
        pg_orm.set_sessionFromSettings(pg_settings.database_settings)
        session = pg_orm.get_session()
        engine = pg_orm.get_engine()
        # query the reference data
        st = time.time()
        from .data.ReferenceData import ReferenceData
        referenceData = ReferenceData(session,engine,pg_settings.datadir_settings)
        print("query the reference data")
        data_ref = referenceData.get_referenceData(
            experiment_ids_I = experiment_ids_I,
            sample_names_I = sample_names_I,
            acquisition_methods_I = acquisition_methods_I,
            component_names_I = component_names_I,
            component_group_names_I = [],
            where_clause_I = where_clause_I,
            used__I = used__I,
            experiment_limit_I = experiment_limit_I,
            mqresultstable_limit_I = mqresultstable_limit_I,
        )
        elapsed_time = time.time() - st
        print("Elapsed time: %.2fs" % elapsed_time)
        session.close()
        # process the reference data
        print("process the reference data")
        data_ref_processed = referenceData.process_referenceData(data_ref)
        elapsed_time = time.time() - st - elapsed_time
        print("Elapsed time: %.2fs" % elapsed_time)
        if data_filename_O:
            smartpeak_o = smartPeak_o(data_ref_processed)
            smartpeak_o.write_dict2csv(filename = data_filename_O)
        
    def run_validate_openSWATH(self,
        filename_filenames='',
        filename_params='',
        delimiter=','):
        """
        Args

        Returns

        Example

        """
        from .pyTOPP.MRMFeatureFilter import MRMFeatureFilter
        featureFilter = MRMFeatureFilter()
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
                data_ref = smartpeak_i.getData()
                smartpeak_i.clear_data()
                # map the reference data
                features_mapped = featureFilter.validate_MRMFeatures(
                    reference_data = data_ref,
                    features = features,
                    Tr_window = float(params['validate_MRMFeatures'][0]['value'])
                    )