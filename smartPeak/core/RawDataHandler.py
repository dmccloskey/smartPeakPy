# -*- coding: utf-8 -*-


class RawDataHandler():
    def __init__(self):
        self.featureMap = None
        self.chromatogram_map = None
        self.targeted = None
        self.trafo = None
        self.msExperiment = None
        self.validation_metrics = None
        self.swath = None
        self.reference_data = None
        self.meta_data = None
        self.quantitationMethods = None

    def clear_data(self):
        """Remove all data"""        
        self.featureMap = None
        self.chromatogram_map = None
        self.targeted = None
        self.trafo = None
        self.msExperiment = None
        self.validation_metrics = None
        self.swath = None
        self.reference_data = None
        self.meta_data = None
        self.quantitationMethods = None