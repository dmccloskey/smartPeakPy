from SBaaS_base.sbaas_base import sbaas_base
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select

class data_referenceData(sbaas_base):
    """
    Select reference data
    """

    def get_referenceData(
        self,
        experiment_ids = [],
        sample_names = [],
        used_ = True):
        """Select reference data

        Args
            experiment_ids ([str]): list of experiment ids
            sample_names ([str]): list of sample names
            used (boolean): default=True

        Returns
            reference_data (list(dict()))

        """
        data_O = []
        subquery1 = '''SELECT COUNT("experiment"."wid"),
                "experiment"."id",
                "experiment"."sample_name" FROM "experiment" 
            '''
        subquery1 = '''WHERE exp_type_id = 4 
            '''
        subquery1 = '''GROUP BY "experiment"."id",
                "experiment"."sample_name" 
            '''
        subquery1 = '''ORDER BY "experiment"."id" ASC,
                "experiment"."sample_name" ASC 
            '''
        subquery1 = '''LIMIT 10000;
            '''
        subquery2 = ''' '''
        query_cmd = ''' '''
        try:
            query_select = sbaas_base_query_select(self.session,self.engine,self.settings)
            data_O = [dict(d) for d in query_select.execute_select(query_cmd)]
        except Exception as e:
            print(e)
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