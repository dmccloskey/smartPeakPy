#utilities
import copy
from math import log, exp, sqrt
#modules
from smartPeak.smartPeak import smartPeak
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class MRMFeatureQC():
    """MRMFeatureQC quality controls features (FeatureMap)

    """

    def check_MRMFeatures(
        self,
        chromatogram_mapped,
        features,
        targeted,
        qc_criteria = [],
        remove_filtered_transitions = True,         
        ):
        """Quality control features
            
        Args
            chromatogram_mapped (MSExperiment):
            features (FeatureMap):
            targeted (TraML): TraML input file containing the transitions
            qc_criteria (list,dict): e.g., [{"name":, "value":, }]
            remove_filtered_transitions (bool): remove filter transitions?
                if True: only transitions that pass the filter are returned
                if False: all transitions are returned with an annotation in 
                    metaValue specifying the QC that failed

        Returns
            output_O (FeatureMap): filtered features
        """
        smartpeak = smartPeak()
        output_filtered = pyopenms.FeatureMap()
        custom_filters = [
            "n_heavy","n_light", #labelTypes
            "n_detecting","n_quantifying","n_identifying", #transitionTypes
            "n_transitions"
            "ion_ratio","ms2_spectra"
            ]
        #filter features
        for feature in features:
            transitions = [t for t in targeted.getTransitions() if t.getPeptideRef() == feature.getMetaValue("PeptideRef")]
            subordinates_tmp = []
            custom_qc_metrics = {}
            custom_qc_metrics.update(self.count_labelsAndTransitionTypes(feature,transitions))
            custom_qc_metrics.update(self.calculate_ionRatio(feature,transitions))
            custom_qc_metrics.update({'ms2_spectra':1.0})

            for subordinate in feature.getSubordinates():
                #transition and peak quality controls
                transition = [t for t in transitions if t.getNativeID()==subordinate.getMetaValue("native_id")][0]
                #TODO: extract out QC criteria...
                fc_pass = True
                for fc in qc_criteria:
                    fc_pass_tmp = True
                    fc_value,fc_comparator = fc['value'].split('|')[0],fc['value'].split('|')[1]
                    f = feature.getMetaValue(fc['name'].encode('utf-8'))
                    if fc['name'] in custom_filters:
                        fc_pass_tmp = smartpeak.compareValues(
                            custom_qc_metrics[fc['name']],
                            smartpeak.parseString(fc_value),
                            fc_comparator)
                    elif not f is None:
                        fc_pass_tmp = smartpeak.compareValues(f,smartpeak.parseString(fc_value),fc_comparator)
                    s = subordinate.getMetaValue(fc['name'].encode('utf-8'))
                    if not s is None:
                        fc_pass_tmp = smartpeak.compareValues(s,smartpeak.parseString(fc_value),fc_comparator)
                    if fc_pass_tmp:
                        subordinate.setMetaValue(fc['name'].encode('utf-8'),'True'.encode('utf-8'))
                    else:
                        subordinate.setMetaValue(fc['name'].encode('utf-8'),'False'.encode('utf-8'))
                        fc_pass = False
                if fc_pass:
                    # subordinates_tmp.addFeature(subordinate,subordinate.getMetaValue("native_id"))
                    subordinates_tmp.append(subordinate)
                    if not remove_filtered_transitions:
                        subordinate.setMetaValue('used_'.encode('utf-8'),'True'.encode('utf-8'))
                else:
                    if not remove_filtered_transitions:
                        subordinate.setMetaValue('used_'.encode('utf-8'),'False'.encode('utf-8'))
                        subordinates_tmp.append(subordinate)
                # subordinates_tmp.append(subordinate)
                if fc_pass:
                    subordinates_tmp.append(subordinate)
            #copy out all feature values
            feature_tmp = copy.copy(feature)
            feature_tmp.setSubordinates(subordinates_tmp)
            output_filtered.push_back(feature_tmp)
        return output_filtered

    def count_labelsAndTransitionTypes(self,
        feature,
        transition):
        """Count the number of heavy and light transitions
        """
        n_heavy,n_light,n_quant,n_detect,n_ident,n_trans = 0,0,0,0,0,0
        for subordinate in feature.getSubordinates():
            transition = [t for t in transitions if t.getNativeID()==subordinate.getMetaValue("native_id")][0]
            label_type = subordinate.getMetaValue("LabelType")
            if label_type == 'Heavy':
                n_heavy += 1
            elif label_type == 'Light':
                n_light += 1
            if transition.isQuantifyingTransition():
                n_quant += 1
            if transition.isIdentifyingTransition():
                n_ident += 1
            if transition.isDetectingTransition():
                n_detect += 1
            n_trans += 1
        output = {
            "n_heavy":n_heavy,
            "n_light":n_light,
            "n_detecting":n_detect,
            "n_quantifying":n_quant,
            "n_identifying":n_ident,
            "n_transitions":n_trans
            }
        return output

    def calculate_ionRatio(self,
        feature,
        transition):
        """Calculate the ion ratio between quantifying and qualifying ion ratios

        Assumptions
            only 3 transitions exist:
                heavy, detecting
                light, quantifying and detecting
                light, detecting
        """
        quant_peak_height = 1.0
        qual_peak_height = 1.0
        for subordinate in feature.getSubordinates():
            transition = [t for t in transitions if t.getNativeID()==subordinate.getMetaValue("native_id")][0]
            label_type = subordinate.getMetaValue("LabelType")
            if label_type == 'Light' and transition.isQuantifyingTransition():
                quant_peak_height = subordinate.getMetaValue("peak_apex_int".encode('utf_8'))
            if label_type == 'Light' and not transition.isQuantifyingTransition() and transition.isDetectingTransition():
                qual_peak_height = subordinate.getMetaValue("peak_apex_int".encode('utf_8'))
        ion_ratio = qual_peak_height/quant_peak_height
        return {"ion_ratio":ion_ratio}

    def calculate_spectralLibraryMatch(self,
        feature,
        transition):
        """Calculate the forward and reverse spectral library match

        Todo...
        """

    def calculate_peakQualityMetrics(self,
        feature,
        transition):
        """Calculate the following peak quality metrics:
            assymetry factor
            USP tailing factor
            change in baseline to height
            points across the peak
            etc.

        Todo...
        """

    def calculate_peakResolution(self,
        feature,
        transition):
        """Calculate resolution and retention time difference between critical pairs

        Todo
        """

    def calculate_quantificationQualityMetrics(self,
        feature,
        transition):
        """Calculate accuracy, bias, R2, LLOQ, ULOQ, etc.

        Todo
        """