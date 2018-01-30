# -*- coding: utf-8 -*-


class SampleHandler():

    def __init__(self):
        self.meta_data = None
        # self.featureMap = None
        self.raw_data_processing = None
        self.sequence_group_processing = None
        self.raw_data = None

    def clear_data(self):
        """Remove all data""" 
        self.meta_data = None
        # self.featureMap = None
        self.raw_data_processing = None
        self.sequence_group_processing = None
        self.raw_data = None

    def setMetaData(self, meta_data_I):
        """Set the meta_data"""
        self.meta_data = meta_data_I

    def getMetaData(self):
        """Return the meta_data"""
        return self.meta_data

    def setRawData(self, raw_data_I):
        """Set the raw_data"""
        self.raw_data = raw_data_I

    def getRawData(self):
        """Return the raw_data"""
        return self.raw_data
