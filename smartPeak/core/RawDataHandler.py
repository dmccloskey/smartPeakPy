# -*- coding: utf-8 -*-


class RawDataHandler():
    def __init__(self):
        # input
        self.msExperiment = None
        self.chromatogram_map = None
        self.trafo = None
        self.swath = None
        # output
        self.featureMap = None
        self.meta_data = None
        self.validation_metrics = None
        # input (reused between RawDataHandlers)
        self.parameters = None
        self.targeted = None
        self.reference_data = None
        self.quantitation_methods = None
        self.feature_filter = None
        self.feature_qc = None

    def clear(self):
        """Remove all data"""   
        # input
        self.msExperiment = None
        self.chromatogram_map = None
        self.trafo = None
        self.swath = None
        # output
        self.featureMap = None
        self.meta_data = None
        # input (reused between RawDataHandlers)
        self.parameters = None
        self.targeted = None
        self.reference_data = None
        self.quantitation_methods = None
        self.feature_filter = None
        self.feature_qc = None
        
    def setFeatureMap(self, featureMap_I):
        """Set the featureMap"""
        self.featureMap = featureMap_I

    def getFeatureMap(self):
        """Return the featureMap"""
        return self.featureMap

    def setParameters(self, parameters_I):
        """Set the parameters"""
        self.parameters = parameters_I

    def getParameters(self):
        """Return the parameters"""
        return self.parameters

    def setTargeted(self, targeted_I):
        """Set the targeted"""
        self.targeted = targeted_I
        
    def getTargeted(self):
        """Return the targeted"""
        return self.targeted    

    def setReferenceData(self, reference_data_I):
        """Set the reference_data"""
        self.reference_data = reference_data_I
        
    def getReferenceData(self):
        """Return the reference_data"""
        return self.reference_data

    def setQuantitationMethods(self, quantitation_methods_I):
        """Set the quantitation_methods"""
        self.quantitation_methods = quantitation_methods_I
        
    def getQuantitationMethods(self):
        """Return the quantitation_methods"""
        return self.quantitation_methods

    def setFeatureFilter(self, feature_filter_I):
        """Set the feature_filter"""
        self.feature_filter = feature_filter_I
        
    def getFeatureFilter(self):
        """Return the feature_filter"""
        return self.feature_filter

    def setFeatureQC(self, feature_qc_I):
        """Set the feature_qc"""
        self.feature_qc = feature_qc_I
        
    def getFeatureQC(self):
        """Return the feature_qc"""
        return self.feature_qc