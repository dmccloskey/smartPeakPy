

class data_referenceData():
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
        reference_data = []
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
        try:
            pass
        except Exception as e:
            print(e)
        return reference_data
    
    def map_referenceData2Features(
        self,
        reference_data,
        features,
        Tr_window = 30
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