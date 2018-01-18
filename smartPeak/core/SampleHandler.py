# -*- coding: utf-8 -*-


class SampleHandler():

    def __init__(self):
        self.meta_data = None
        self.featureMap = None
        self.raw_data_processing = None
        self.sequence_group_processing = None
        self.raw_data = None

    def clear_data(self):
        """Remove all data""" 
        self.meta_data = None
        self.featureMap = None
        self.raw_data_processing = None
        self.sequence_group_processing = None
        self.raw_data = None