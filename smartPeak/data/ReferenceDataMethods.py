# -*- coding: utf-8 -*-
from smartPeak.core.smartPeak_o import smartPeak_o
import time as time
from .DescriptiveStatistics import DescriptiveStatistics


class ReferenceDataMethods():
    """Methods for getting and processing reference validation data"""

    def getAndProcess_referenceData_samples(
        self,
        experiment_ids_I=[],
        sample_names_I=[],
        sample_types_I=[],
        acquisition_methods_I=[],
        quantitation_method_ids_I=[],
        component_names_I=[],
        component_group_names_I=[],
        where_clause_I='',
        used__I=True,
        experiment_limit_I=10000,
        mqresultstable_limit_I=1000000,
        settings_filename_I='settings.ini',
        data_filename_O=''
    ):
        """
        Args:

        Returns:

        """
        data_ref_processed = self.getAndProcess_referenceData(
            experiment_ids_I=experiment_ids_I,
            sample_names_I=sample_names_I,
            sample_types_I=sample_types_I,
            acquisition_methods_I=acquisition_methods_I,
            quantitation_method_ids_I=quantitation_method_ids_I,
            component_names_I=component_names_I,
            component_group_names_I=component_group_names_I,
            where_clause_I=where_clause_I,
            used__I=used__I,
            experiment_limit_I=experiment_limit_I,
            mqresultstable_limit_I=mqresultstable_limit_I,
            settings_filename_I=settings_filename_I,
        )
        if data_filename_O:
            smartpeak_o = smartPeak_o(data_ref_processed)
            smartpeak_o.write_dict2csv(filename=data_filename_O)
            return None
        else:
            return data_ref_processed       

    def getAndProcess_referenceData_calibrators(
        self,
        experiment_ids_I=[],
        sample_names_I=[],
        sample_types_I=[],
        acquisition_methods_I=[],
        quantitation_method_ids_I=[],
        component_names_I=[],
        component_group_names_I=[],
        where_clause_I='',
        used__I=True,
        experiment_limit_I=10000,
        mqresultstable_limit_I=1000000,
        settings_filename_I='settings.ini',
        data_filename_O=''
    ):
        """
        Args:

        Returns:

        """
        data_ref_processed = self.getAndProcess_referenceData(
            experiment_ids_I=experiment_ids_I,
            sample_names_I=sample_names_I,
            sample_types_I=sample_types_I,
            acquisition_methods_I=acquisition_methods_I,
            quantitation_method_ids_I=quantitation_method_ids_I,
            component_names_I=component_names_I,
            component_group_names_I=component_group_names_I,
            where_clause_I=where_clause_I,
            used__I=used__I,
            experiment_limit_I=experiment_limit_I,
            mqresultstable_limit_I=mqresultstable_limit_I,
            settings_filename_I=settings_filename_I,
        )
        # callapse the reference data to the average retention time
        calibrators_rt_dict = {}  # {'component_name':[Tr]}
        for row in data_ref_processed:
            key = (
                row['component_name'], row['component_group_name'], 
                row['experiment_id'], row['acquisition_method_id'], 
                row['quantitation_method_id'])
            if key not in calibrators_rt_dict.keys():
                calibrators_rt_dict[key] = []
            calibrators_rt_dict[key].append(row['retention_time'])
        # calculate the descriptive statistics for each component
        descStats = DescriptiveStatistics()
        calibrators_rt_list = []
        for k, v in calibrators_rt_dict.items():
            tmp = {
                'component_name': k[0], 'component_group_name': k[1], 
                'experiment_id': k[2], 'acquisition_method_id': k[3], 
                'quantitation_method_id': k[4],
                'sample_name': 'Calibrators'}
            out = descStats.calculate_descriptiveStats(data_I=v)
            tmp.update(out)
            tmp['retention_time'] = tmp['mean']
            calibrators_rt_list.append(tmp)
        if data_filename_O:
            smartpeak_o = smartPeak_o(calibrators_rt_list)
            smartpeak_o.write_dict2csv(filename=data_filename_O)
            return None
        else:
            return calibrators_rt_list

    def getAndProcess_referenceData(
        self,
        experiment_ids_I=[],
        sample_names_I=[],
        sample_types_I=[],
        acquisition_methods_I=[],
        quantitation_method_ids_I=[],
        component_names_I=[],
        component_group_names_I=[],
        where_clause_I='',
        used__I=True,
        experiment_limit_I=10000,
        mqresultstable_limit_I=1000000,
        settings_filename_I='settings.ini',
        verbose_I=False
    ):
        """
        Args:

        Returns:

        """
        # DB settings
        # # TODO: from SBaaS_base.postgresql_settings import postgresql_settings        
        pg_settings = postgresql_settings(settings_filename_I)
        # # TODO: from SBaaS_base.postgresql_orm import postgresql_orm
        pg_settings.set_sessionFromSettings(pg_settings.database_settings)
        session = pg_settings.get_session()
        engine = pg_settings.get_engine()
        # query the reference data
        st = time.time()
        from .ReferenceData import ReferenceData
        referenceData = ReferenceData(session, engine, pg_settings.datadir_settings)
        if verbose_I: 
            print("query the reference data")
        data_ref = referenceData.get_referenceData(
            experiment_ids_I=experiment_ids_I,
            sample_names_I=sample_names_I,
            sample_types_I=sample_types_I,
            acquisition_methods_I=acquisition_methods_I,
            quantitation_method_ids_I=quantitation_method_ids_I,
            component_names_I=component_names_I,
            component_group_names_I=component_group_names_I,
            where_clause_I=where_clause_I,
            used__I=used__I,
            experiment_limit_I=experiment_limit_I,
            mqresultstable_limit_I=mqresultstable_limit_I,
        )
        elapsed_time = time.time() - st
        if verbose_I: 
            print("Elapsed time: %.2fs" % elapsed_time)
        session.close()
        # process the reference data
        if verbose_I: 
            print("process the reference data")
        data_ref_processed = referenceData.process_referenceData(data_ref)
        elapsed_time = time.time() - st - elapsed_time
        if verbose_I: 
            print("Elapsed time: %.2fs" % elapsed_time)
        return data_ref_processed