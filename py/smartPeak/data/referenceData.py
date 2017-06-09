from SBaaS_base.sbaas_base import sbaas_base
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select

"""

"""

class ReferenceData(sbaas_base):
    """
    Select reference data
    """

    def get_referenceData(
        self,
        experiment_ids_I = [],
        sample_names_I = [],
        acquisition_methods_I = [],
        component_names_I = [],
        component_group_names_I = [],
        where_clause_I = '',
        used__I = True,
        experiment_limit_I = 10000,
        mqresultstable_limit_I = 1000000):
        """Select reference data

        Args
            experiment_ids ([str]): list of experiment ids
            sample_names ([str]): list of sample names
            used (boolean): default=True

        Returns
            reference_data (list(dict()))

        """
        data_O = []
        #subquery 1: experiment
        subquery1 = '''SELECT "experiment"."id" AS experiment_id,
                "experiment"."sample_name", 
                "experiment"."acquisition_method_id"
            '''
        subquery1 += '''FROM "experiment" 
            '''
        subquery1 += '''WHERE exp_type_id = 4 
            '''
        if experiment_ids_I:
            cmd_q = '''AND "experiment"."id" =ANY ('{%s}'::text[]) ''' %(self.convert_list2string(experiment_ids_I))
            subquery1 += cmd_q
        if sample_names_I:
            cmd_q = '''AND "experiment"."sample_name" =ANY ('{%s}'::text[]) ''' %(self.convert_list2string(sample_names_I))
            subquery1 += cmd_q
        if acquisition_methods_I:
            cmd_q = '''AND "experiment"."acquisition_method_id" =ANY ('{%s}'::text[]) ''' %(self.convert_list2string(acquisition_methods_I))
            subquery1 += cmd_q
        subquery1 += '''GROUP BY "experiment"."id",
                "experiment"."sample_name", 
                "experiment"."acquisition_method_id"
            '''
        subquery1 += '''ORDER BY "experiment"."id" ASC,
                "experiment"."sample_name" ASC, 
                "experiment"."acquisition_method_id" ASC
            '''
        subquery1 += '''LIMIT %s
            ''' % experiment_limit_I
        #subquery 2: mqresultstable
        subquery2 = '''SELECT "data_stage01_quantification_mqresultstable"."id",
            "data_stage01_quantification_mqresultstable"."index_",
            "data_stage01_quantification_mqresultstable"."sample_index",
            "data_stage01_quantification_mqresultstable"."original_filename",
            "data_stage01_quantification_mqresultstable"."sample_name",
            "data_stage01_quantification_mqresultstable"."sample_id",
            "data_stage01_quantification_mqresultstable"."sample_comment",
            "data_stage01_quantification_mqresultstable"."sample_type",
            "data_stage01_quantification_mqresultstable"."acquisition_date_and_time",
            "data_stage01_quantification_mqresultstable"."rack_number",
            "data_stage01_quantification_mqresultstable"."plate_number",
            "data_stage01_quantification_mqresultstable"."vial_number",
            "data_stage01_quantification_mqresultstable"."dilution_factor",
            "data_stage01_quantification_mqresultstable"."injection_volume",
            "data_stage01_quantification_mqresultstable"."operator_name",
            "data_stage01_quantification_mqresultstable"."acq_method_name",
            "data_stage01_quantification_mqresultstable"."is_",
            "data_stage01_quantification_mqresultstable"."component_name",
            "data_stage01_quantification_mqresultstable"."component_index",
            "data_stage01_quantification_mqresultstable"."component_comment",
            "data_stage01_quantification_mqresultstable"."is_comment",
            "data_stage01_quantification_mqresultstable"."mass_info",
            "data_stage01_quantification_mqresultstable"."is_mass",
            "data_stage01_quantification_mqresultstable"."is_name",
            "data_stage01_quantification_mqresultstable"."component_group_name",
            "data_stage01_quantification_mqresultstable"."conc_units",
            "data_stage01_quantification_mqresultstable"."failed_query",
            "data_stage01_quantification_mqresultstable"."is_failed_query",
            "data_stage01_quantification_mqresultstable"."peak_comment",
            "data_stage01_quantification_mqresultstable"."is_peak_comment",
            "data_stage01_quantification_mqresultstable"."actual_concentration",
            "data_stage01_quantification_mqresultstable"."is_actual_concentration",
            "data_stage01_quantification_mqresultstable"."concentration_ratio",
            "data_stage01_quantification_mqresultstable"."expected_rt",
            "data_stage01_quantification_mqresultstable"."is_expected_rt",
            "data_stage01_quantification_mqresultstable"."integration_type",
            "data_stage01_quantification_mqresultstable"."is_integration_type",
            "data_stage01_quantification_mqresultstable"."area",
            "data_stage01_quantification_mqresultstable"."is_area",
            "data_stage01_quantification_mqresultstable"."corrected_area",
            "data_stage01_quantification_mqresultstable"."is_corrected_area",
            "data_stage01_quantification_mqresultstable"."area_ratio",
            "data_stage01_quantification_mqresultstable"."height",
            "data_stage01_quantification_mqresultstable"."is_height",
            "data_stage01_quantification_mqresultstable"."corrected_height",
            "data_stage01_quantification_mqresultstable"."is_corrected_height",
            "data_stage01_quantification_mqresultstable"."height_ratio",
            "data_stage01_quantification_mqresultstable"."area_2_height",
            "data_stage01_quantification_mqresultstable"."is_area_2_height",
            "data_stage01_quantification_mqresultstable"."corrected_area2height",
            "data_stage01_quantification_mqresultstable"."is_corrected_area2height",
            "data_stage01_quantification_mqresultstable"."region_height",
            "data_stage01_quantification_mqresultstable"."is_region_height",
            "data_stage01_quantification_mqresultstable"."quality",
            "data_stage01_quantification_mqresultstable"."is_quality",
            "data_stage01_quantification_mqresultstable"."retention_time",
            "data_stage01_quantification_mqresultstable"."is_retention_time",
            "data_stage01_quantification_mqresultstable"."start_time",
            "data_stage01_quantification_mqresultstable"."is_start_time",
            "data_stage01_quantification_mqresultstable"."end_time",
            "data_stage01_quantification_mqresultstable"."is_end_time",
            "data_stage01_quantification_mqresultstable"."total_width",
            "data_stage01_quantification_mqresultstable"."is_total_width",
            "data_stage01_quantification_mqresultstable"."width_at_50",
            "data_stage01_quantification_mqresultstable"."is_width_at_50",
            "data_stage01_quantification_mqresultstable"."signal_2_noise",
            "data_stage01_quantification_mqresultstable"."is_signal_2_noise",
            "data_stage01_quantification_mqresultstable"."baseline_delta_2_height",
            "data_stage01_quantification_mqresultstable"."is_baseline_delta_2_height",
            "data_stage01_quantification_mqresultstable"."modified_",
            "data_stage01_quantification_mqresultstable"."relative_rt",
            "data_stage01_quantification_mqresultstable"."used_",
            "data_stage01_quantification_mqresultstable"."calculated_concentration",
            "data_stage01_quantification_mqresultstable"."accuracy_",
            "data_stage01_quantification_mqresultstable"."comment_",
            "data_stage01_quantification_mqresultstable"."use_calculated_concentration",
            "data_stage01_quantification_mqresultstable"."start_time_at_5",
            "data_stage01_quantification_mqresultstable"."end_time_at_5",
            "data_stage01_quantification_mqresultstable"."width_at_5",
            "data_stage01_quantification_mqresultstable"."start_time_at_10",
            "data_stage01_quantification_mqresultstable"."end_time_at_10",
            "data_stage01_quantification_mqresultstable"."width_at_10",
            "data_stage01_quantification_mqresultstable"."slope_of_baseline",
            "data_stage01_quantification_mqresultstable"."tailing_factor",
            "data_stage01_quantification_mqresultstable"."asymmetry_factor",
            "data_stage01_quantification_mqresultstable"."ion_ratio",
            "data_stage01_quantification_mqresultstable"."expected_ion_ratio",
            "data_stage01_quantification_mqresultstable"."points_across_baseline",
            "data_stage01_quantification_mqresultstable"."points_across_half_height",
            "subquery1"."experiment_id",
            "subquery1"."acquisition_method_id"
        '''
        subquery2 += '''FROM "data_stage01_quantification_mqresultstable",
            (%s) AS subquery1 
        ''' %subquery1
        subquery2 += '''WHERE "data_stage01_quantification_mqresultstable"."sample_name" = "subquery1"."sample_name" 
        '''
        if component_names_I:
            cmd_q = '''AND "data_stage01_quantification_mqresultstable"."component_name" =ANY ('{%s}'::text[]) ''' %(self.convert_list2string(component_names_I))
            subquery2 += cmd_q
        if component_group_names_I:
            cmd_q = '''AND "data_stage01_quantification_mqresultstable"."component_group_name" =ANY ('{%s}'::text[]) ''' %(self.convert_list2string(component_group_names_I))
            subquery2 += cmd_q
        if used__I:
            subquery2 += '''AND used_ '''
        elif not used__I:
            subquery2 += '''AND NOT used_ '''

        subquery2 += '''ORDER BY "subquery1"."experiment_id" ASC,
                "subquery1"."acquisition_method_id" ASC,
                "data_stage01_quantification_mqresultstable"."sample_name" ASC,
                "data_stage01_quantification_mqresultstable"."component_name" ASC
            '''
        subquery2 += '''LIMIT %s
            ''' % mqresultstable_limit_I
        #final query
        query_cmd = '''%s; ''' %subquery2
        try:
            query_select = sbaas_base_query_select(self.session,self.engine,self.settings)
            data_O = [dict(d) for d in query_select.execute_select(query_cmd)]
        except Exception as e:
            print(e)
        return data_O

    def process_referenceData(self,
        data_I):
        """Process the reference data
        1. remove all internal standards that are not referenced by an analyte
        2. integrity check of pertinent data

        Args
            data_I (list, dict)

        Returns
            data_O (list, dict):
        """
        is_names = [d['is_name'] for d in data_I if not d['is_name'] is None]
        data_O = []
        for row in data_I:
            if row['component_name'] in is_names and row['is_']:
                data_O.append(row)
            elif not row['is_']:
                data_O.append(row)
        return data_O
    
    def map_referenceData2Features(
        self,
        reference_data,
        features,
        Tr_window = 1.0
        ):
        """Map reference data to FeatureMap
        
        Args
            reference_data (list(dict()): reference data
            features (FeatureMap): features
            
        Returns
            features_mapped (FeatureMap): mapped features
        """

        # 1. check Tr_gs +/- Tr < threshold
        # 2. check Tr_gs < rightWidth and Tr_gs > leftWidth