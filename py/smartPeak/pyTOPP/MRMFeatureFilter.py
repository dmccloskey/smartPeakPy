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
        filter_criteria=[]
        ):
        """Filter features from a FeatureMap that satisfy filter criteria
        
        Args
            features (FeatureMap):
            filter_criteria (list,dict): e.g., [{"name":, "value":, }]
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

    def align_MRMFeatures(
        self,features,targeted,anchors,
        alignment_criteria=[]
        ):
        """Aligns feature Tr (retention time, normalized retention time)
        and removes features that violate retention time order

        Args
            features (FeatureMap):
            targeted (TraML): transition list in targetedExperiment
            anchors (TraML): transition list in targetedExperiment

        Returns
            output_O (FeatureMap): filtered features

        """
        #convert Tr to To
        #Tr: absolute or normalized retention time
        #To: retention time order
        To_dict = {}
        #1: reorder features by Tr
        #2: convert Tr to To
        #3: create index for each compound {compound:{To:,Tr:}}

        #remove achors that have multiple Tr

        #iteratively remove features that violate To starting with
        #the first achor (right to left and left to right)


    def select_MRMFeatures(
        self,features,
        score_weights=[]):
        """Selects the best feature from a FeatureMap based on a scoring criteria
        
        Args
            features (FeatureMap):
            score_weights (list,dict): e.g., [{"name":, "value":, }]
            n_peaks_max (int): maximum number of features per transition to extract
                in ascending order

        Returns
            output_O (FeatureMap): selected features
        """
        smartpeak = smartPeak()
        score_tmp = 0
        output_ranked = pyopenms.FeatureMap()
        #compute a pooled score for each transition group
        transition_group_id_current = ''
        best_transition_group = None
        best_transition_group_score = 0
        for feature in features:
            subordinates_tmp = []
            transition_group_id = feature.getMetaValue("PeptideRef").decode('utf-8')
            # add the best transition
            if transition_group_id != transition_group_id_current and not best_transition_group is None:
                output_ranked.push_back(best_transition_group)
            # initialize the best transition
            if transition_group_id != transition_group_id_current:
                transition_group_id_current = transition_group_id
                best_transition_group = None
                best_transition_group_score = 0
            for score_weight in score_weights:
                score = float(feature.getMetaValue(score_weight['name']))*float(score_weight['value'])
                if best_transition_group_score < score:
                    best_transition_group_score = score
                    best_transition_group = feature
        #add in the last best transition
        output_ranked.push_back(best_transition_group)
        return output_ranked

    def validate_MRMFeatures(
        self,
        reference_data,
        features,
        Tr_window = 1.0
        ):
        """Map reference data to FeatureMap
        
        Args
            reference_data (list(dict())): reference data
            features (FeatureMap): features
            Tr_window (float): retention time difference threshold
            
        Returns
            features_mapped (FeatureMap): mapped features
        """
        #reformat reference_data into a dict by unique key
        # TODO: need to add in the experiment_id and acquisition_method_id to feature or as a parameter
        # reference_data_dict = {(d['experiment_id'],d['acquisition_method_id'],d['sample_name'],d['component_name']):d for d in reference_data}
        reference_data_dict = {(d['component_name']):d for d in reference_data}
        #intialize y_true,y_pred
        y_true, y_pred = [], []
        output_filtered = pyopenms.FeatureMap()
        for feature in features:
            subordinates_tmp = []
            for subordinate in feature.getSubordinates():
                fc_pass = False
                #make the reference_data_dict key
                reference_data_key = (subordinate.getMetaValue('native_id').decode('utf-8'))
                if not reference_data_key in reference_data_dict.keys():
                    continue
                y_true.append(1)
                #extract and format rt information
                reference_rt = float(reference_data_dict[reference_data_key]['retention_time'])
                feature_rt = feature.getRT()
                feature_leftWidth = feature.getMetaValue('leftWidth')
                feature_rightWidth = feature.getMetaValue('rightWidth')
                #validate the retention time
                if abs(reference_rt - feature_rt) < Tr_window:
                    fc_pass = True
                if reference_rt > feature_leftWidth \
                    and reference_rt < feature_rightWidth:
                    fc_pass = True
                #other validation parameters
                #NOTE: if there are no other validation parameters that are
                #      transition-specific, there is no need to loop
                #      through each transition
                if fc_pass:
                    subordinates_tmp.append(subordinate)
                    y_pred.append(1)
                else:
                    y_pred.append(0)
                # #TESTING:
                #     print('Tr for transition ' + subordinate.getMetaValue('native_id').decode('utf-8') + ' does not match the reference.')
                
            #check that subordinates were found
            if not subordinates_tmp:
                continue
            #copy out all feature values
            feature_tmp = copy.copy(feature)
            feature_tmp.setSubordinates(subordinates_tmp)
            output_filtered.push_back(feature_tmp)
        # calculate AUC, precision, accuracy, recall
        auc,accuracy,recall,precision = self.calculate_validationMetrics(y_true,y_pred,verbose_I=True)
        return output_filtered

    def calculate_validationMetrics(self,y_true,y_pred,verbose_I=False):
        """
        Calculate the auc, accuracy, recall, and precision

        Args:
            y_true (list or array): ground truth values
            y_pred (list or array): predicted values
            verbose_I (bool): if True, print results; default = False

        Returns:
            auc (float): area under the ROC
            accuracy (float): (tp + tn) / (tp + tn + fp + fn)
            recall (float): tp / (tp + fn)
            precision (float): tp / (tp + fp)
        """
        # calculate AUC, precision, accuracy, recall
        import numpy as np
        from sklearn import metrics
        auc,accuracy,recall,precision = None, None, None, None
        fpr, tpr, thresholds = metrics.roc_curve(y_true, y_pred)
        auc = metrics.auc(fpr, tpr)
        #accuracy = (tp + tn) / (tp + tn + fp + fn)
        accuracy = metrics.accuracy_score(y_true, y_pred, normalize=True)
        #recall = tp / (tp + fn)
        recall = metrics.recall_score(y_true, y_pred, average='macro') 
        #precision = tp / (tp + fp)
        precision = metrics.precision_score(y_true, y_pred, average='macro')
        if verbose_I:
            print("AUC: " + str(auc))
            print("accuracy: " + str(accuracy))
            print("recall: " + str(recall))
            print("precision: " + str(precision))
        return auc,accuracy,recall,precision
