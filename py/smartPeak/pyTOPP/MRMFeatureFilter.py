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
    """MRMFeatureFilter filters features (FeatureMap)

    """

    def filter_MRMFeatures(
        self,features,
        filter_criteria=[],
        remove_filtered_transitions = True,        
        ):
        """Filter features from a FeatureMap that satisfy a filter criteria
        
        Args
            features (FeatureMap):
            filter_criteria (list,dict): e.g., [{"name":, "value":, }]
            remove_filtered_transitions (bool): remove filter transitions?
                if True: only transitions that pass the filter are returrned
                if False: all transitions are returned with an annotation in 
                    metaValue for "used_" specifying True or False whether the peak passed the threshold

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
                    if not remove_filtered_transitions:
                        subordinate.setMetaValue('used_'.encode('utf-8'),'True'.encode('utf-8'))
                else:
                    if not remove_filtered_transitions:
                        subordinate.setMetaValue('used_'.encode('utf-8'),'False'.encode('utf-8'))
                        subordinates_tmp.append(subordinate)
            #check that subordinates were found
            if not subordinates_tmp:
                continue
            #copy out all feature values
            feature_tmp = copy.copy(feature)
            feature_tmp.setSubordinates(subordinates_tmp)
            output_filtered.push_back(feature_tmp)
        return output_filtered