# -*- coding: utf-8 -*-
"""
TODO:
1. add import statements
2. add base class (sbaas_base)
3. add query methods (sbaas_base)
4. test
"""


class RetentionComponents():
    """
    Select and normalize retention components
    """

    def get_retentionComponents(
        self,
        sample_names,
        component_names,
        used_=True,
        thresholds_query=''
    ):
        """Select retention components from data base
        
        Args:
            sample_names ([str]): calibrator or SST samples
            component_names ([str]): list of component names to be used as the retention components
            used_ (boolean): if used_ compounds should only be used; default: True
            thresholds_query (str): additional SQL text (e.g., 'signal_2_noise > 10.0') to add to the query WHERE clause
        
        Return:
            list: retention_components: list of dictionaries with values
        """

        query_cmd = '''SELECT "data_stage01_quantification_mqresultstable"."component_name",
                "data_stage01_quantification_mqresultstable"."component_group_name",
                AVG("data_stage01_quantification_mqresultstable"."retention_time"),
                stddev_samp("data_stage01_quantification_mqresultstable"."retention_time") 
            '''
        query_cmd += '''FROM "data_stage01_quantification_mqresultstable" 
            '''
        query_cmd += '''WHERE sample_name =ANY ('{%s}'::TEXT[]) 
                AND component_name =ANY ('{%s}'::TEXT[]) 
            ''' % (sample_names, component_names)
        if used_:
            query_cmd += '''AND used_ 
            '''
        if thresholds_query:
            query_cmd += '''AND %s
            '''            
        query_cmd += '''GROUP BY "data_stage01_quantification_mqresultstable"."component_name",
                "data_stage01_quantification_mqresultstable"."component_group_name" 
            '''
        query_cmd += '''ORDER BY component_name ASC 
            '''
        query_cmd += '''LIMIT 10000;
            '''
        try:
            pass
        except Exception as e:
            print(e)

    def normalize_retentionComponents(
        self,
        retention_components
        ):
        """Normalize retention components to the min/max
        
        Args:
            retention_components (list(dict())): list of dictionaries with values
            
        Return:
            list: retention_components (list(dict())): list of dictionaries with normalized values
                normalized values will be stored in key=Tr_recalibrated
        """

        rts = [d['avg'] for d in retention_components]
        rt_min = min(rts)
        rt_max = max(rts)
        for row in retention_components:
            row['Tr_recalibrated'] = (row['avg']-rt_min)/(rt_max-rt_min)*100.0

    def map_retentionComponents2Trafo(
        self,
        retention_components
        ):
        """Map retentionComponents to trafo (i.e., TraML) .csv file standard
        
        Args:
            retention_components (list(dict())): list of dictionaries with values
            
        Return:
            list: trafo_csv: trafo .csv file format
        """

        pass