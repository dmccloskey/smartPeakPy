#utilities
import copy
#modules
from smartPeak.smartPeak import smartPeak
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class MRMFeatureValidator():
    """MRMFeatureFilter performs validation on features (FeatureMap)

    """
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

        Potential code optimizations
            identify True Negatives and False Negatives 
                (can be problematic due to selection of peaks not in the quantification target list...)
            add in plots and other visualizations
        """
        #reformat reference_data into a dict by unique key
        # TODO: need to add in the experiment_id and acquisition_method_id to feature or as a parameter
        # reference_data_dict = {(d['experiment_id'],d['acquisition_method_id'],d['quantitation_method_id'],d['sample_name'],d['component_name']):d for d in reference_data}
        reference_data_dict = {(d['component_name']):d for d in reference_data}
        #intialize y_true,y_pred
        y_true, y_pred = [], []
        # #TESTING FN:
        # reference_data_keys = []
        output_filtered = pyopenms.FeatureMap()
        for feature in features:
            subordinates_tmp = []
            for subordinate in feature.getSubordinates():
                fc_pass = False
                #make the reference_data_dict key
                reference_data_key = (subordinate.getMetaValue('native_id').decode('utf-8'))
                # #TESTING FN:
                # reference_data_keys.append(reference_data_key)
                if not reference_data_key in reference_data_dict.keys():
                    subordinate.setMetaValue('validation'.encode('utf-8'),'ND'.encode('utf-8'))
                    subordinates_tmp.append(subordinate)
                    continue
                y_true.append(1)
                #extract and format rt information
                if reference_data_dict[reference_data_key]['retention_time'] is None:
                    print('check')
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
                if fc_pass: #True Positive
                    subordinate.setMetaValue('validation'.encode('utf-8'),'TP'.encode('utf-8'))
                    subordinates_tmp.append(subordinate)
                    y_pred.append(1)
                else: #False Positive
                    subordinate.setMetaValue('validation'.encode('utf-8'),'FP'.encode('utf-8'))
                    subordinates_tmp.append(subordinate)
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
        # #TESTING FN:
        # # add in False Negative
        # for k in reference_data_dict.keys():
        #     if k not in reference_data_keys:
        #         y_pred.append(0)
        #         y_true.append(1)
        # calculate AUC, precision, accuracy, recall
        validation_metrics = self.calculate_validationMetrics(y_true,y_pred,verbose_I=True)
        return output_filtered,validation_metrics

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
        output = {"AUC":auc,"accuracy":accuracy,"recall":recall,"precision":precision}
        return output