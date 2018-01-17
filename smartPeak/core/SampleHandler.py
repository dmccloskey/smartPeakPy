# -*- coding: utf-8 -*-


class SampleHandler():

    def __init__(self):
        self.meta_data = None
        self.featureMap = None
        self.sample_processing = None
        self.sequence_processing = None
        self.raw_data = None

    def clear_data(self):
        """Remove all data""" 
        self.meta_data = None
        self.featureMap = None
        self.sample_processing = None
        self.sequence_processing = None
        self.raw_data = None