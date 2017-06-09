#utilities
import copy
#modules
from smartPeak.smartPeak import smartPeak
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class MRMFeatureFilter():
    """MRMFeatureFilter filters and selects features (FeatureMap)

    """

    def filter_MRMFeatures(
        self,features,
        filter_criteria={}
        ):
        """Filter features from a FeatureMap that satisfy filter criteria
        
        Args
            features (FeatureMap):
            filter_criteria (dict): e.g., {"name":, "value":, "order_by":, "comparator":}
                where order_by = "ASC" or "DESC"
                      comparator = "<", ">"
            n_peaks_max (int): maximum number of features per transition to extract

        Returns
            output_O (FeatureMap): filtered features
        """
        smartpeak = smartPeak()
        output_filtered = pyopenms.FeatureMap()
        #filter features
        for feature in features:
            subordinates_tmp = []
            for subordinate in feature.getSubordinates():
                # print(subordinate.getMetaValue("native_id"))
                # if subordinate.getMetaValue("native_id")==b'35cgmp.35cgmp_2.Light':
                #     print('check')
                fc_pass = True
                for fc in filter_criteria:
                    fc_value,fc_comparator = fc['value'].split('|')[0],fc['value'].split('|')[1]
                    f = feature.getMetaValue(fc['name'].encode('utf-8'))
                    if not f is None:
                        fc_pass = smartpeak.compareValues(f,smartpeak.parseString(fc_value),fc_comparator)
                    s = subordinate.getMetaValue(fc['name'].encode('utf-8'))
                    if not s is None:
                        fc_pass = smartpeak.compareValues(s,smartpeak.parseString(fc_value),fc_comparator)
                    if not fc_pass:
                        break
                if fc_pass:
                    # subordinates_tmp.addFeature(subordinate,subordinate.getMetaValue("native_id"))
                    subordinates_tmp.append(subordinate)
            #check that subordinates were found
            if not subordinates_tmp:
                continue
            #copy out all feature values
            feature_tmp = copy.copy(feature)
            feature_tmp.setSubordinates(subordinates_tmp)
            output_filtered.push_back(feature_tmp)
        return output_filtered

    def select_MRMFeatures(
        self,features,
        score_weights={},
        n_peaks_max=1):
        """Selects features from a FeatureMap that satisfy filter criteria
        
        Args
            features (FeatureMap):
            score_weights (dict): e.g., {"name":, "value":, }
            n_peaks_max (int): maximum number of features per transition to extract
                in ascending order

        Returns
            output_O (FeatureMap): filtered features
        """
        smartpeak = smartPeak()
        score_tmp = 0
        output_ranked = pyopenms.FeatureMap()
        #compute a pooled score for each transition and transition group
        for feature in features:
            subordinates_tmp = []
            for subordinate in feature.getSubordinates():
                pass
    
    def validate_MRMFeatures(
        self,
        reference_data,
        features,
        Tr_window = 1.0
        ):
        """Map reference data to FeatureMap
        
        Args
            reference_data (list(dict()): reference data
            features (FeatureMap): features
            Tr_window (float): retention time difference threshold
            
        Returns
            features_mapped (FeatureMap): mapped features
        """
        #reformat reference_data into a dict by unique key
        # TODO: need to add in the experiment_id and acquisition_method_id to feature or as a parameter
        # reference_data_dict = {(d['experiment_id'],d['acquisition_method_id'],d['sample_name'],d['component_name']):d for d in reference_data}
        reference_data_dict = {(d['sample_name'],d['component_name']):d for d in reference_data}
        #intialize counters
        n_features = features.size()
        n_dataReference = len(reference_data)
        n_features_mapped = 0
        n_features_validated = 0     
        validated_data = []
        output_filtered = pyopenms.FeatureMap()
        for feature in features:
            subordinates_tmp = []
            for subordinate in feature.getSubordinates():
                fc_pass = False
                #make the reference_data_dict key
                reference_data_key = (subordinate.getRunID(),subordinate.getMetaValue('native_id'))
                #extract and format rt information
                feature_rt = feature.getRT()
                if type(feature_rt)==type(''.encode('utf-8')):
                    feature_rt = feature_rt.decode('utf-8')
                feature_leftWidth = feature.getMetaValue('leftWidth')
                if type(value)==type(''.encode('utf-8')):
                    feature_leftWidth = feature_leftWidth.decode('utf-8')
                feature_reftWidth = feature.getMetaValue('reftWidth')
                if type(feature_reftWidth)==type(''.encode('utf-8')):
                    feature_reftWidth = feature_reftWidth.decode('utf-8')
                #validate the retention time
                if abs(reference_data_dict[reference_data_key]['retention_time'] - feature_rt) < Tr_window:
                    fc_pass = True
                if reference_data_dict[reference_data_key]['retention_time'] > feature_leftWidth \
                    and reference_data_dict[reference_data_key]['retention_time'] < feature_rightWidth:
                    fc_pass = True
                #other validation parameters
                #NOTE: if there are no other validation parameters that are
                #      transition-specific, there is no need to loop
                #      through each transition
                if fc_pass:
                    subordinates_tmp.append(subordinate)
                # 1. check Tr_gs +/- Tr < threshold
                # 2. check Tr_gs < rightWidth and Tr_gs > leftWidth
            #check that subordinates were found
            if not subordinates_tmp:
                continue
            #copy out all feature values
            feature_tmp = copy.copy(feature)
            feature_tmp.setSubordinates(subordinates_tmp)
            output_filtered.push_back(feature_tmp)
        return output_filtered
