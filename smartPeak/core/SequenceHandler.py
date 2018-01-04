# -*- coding: utf-8 -*-
# utilities
import csv
import sys
# modules
from smartPeak.io.FileReader import FileReader
# 3rd part libraries
try:
    import pyopenms
    import numpy as np
except ImportError as e:
    print(e)


class SequenceHandler():
    """A class to manage the mapping of metadata and FeatureMaps
        (i.e., multiple samples in a run batch/sequence)"""

    def __init__(self):
        """
        """
        self.sequence = []
        self.index_to_sample = {}
        self.sample_to_index = {}

    def getSequence(self):
        """Return sequence"""
        return self.sequence

    def addSampleToSequence(self, meta_data, featureMap):
        """add meta_data and featureMap to a sequence list

        Args:
            meta_data (dict): dictionary of meta data (e.g., sample_name)
            featureMap (FeatureMap): processed data in a FeatureMap

        Returns:
            dict: injection: dictionary of meta_data and FeatureMap
        """

        sample_name = ''
        if 'sample_name' in meta_data.keys():
            sample_name = meta_data['sample_name']

        injection = {
            'meta_data': self.parse_metaData(meta_data),
            'featureMap': featureMap
        }

        self.sequence.append(injection)
        self.index_to_sample[len(self.sequence)-1] = sample_name
        self.sample_to_index[sample_name] = len(self.sequence)-1

    def getMetaValue(self, feature, subordinate, meta_value):
        """Returns the metaValue
        
        Args:
            feature (Feature): OpenMS::Feature corresponding to transition_group
            subordinate (Feature): OPENMS::Feature corresponding to transition

        Returns:
            float: datum: metaValue extraction from feature or subordinate
            
        """
        datum = None
        if meta_value == 'RT':
            datum = feature.getRT()
        else:
            datum = feature.getMetaValue(meta_value)
            if datum is None:
                datum = subordinate.getMetaValue(meta_value)
        return datum

    def getRequiredHeaders(self):
        """Return required headers in a sequence file"""

        # # MultiQuant Example
        # required_headers = [
        #     "SampleName","SampleID",
        #     "Comments","AcqMethod",
        #     "ProcMethod","RackCode","PlateCode","VialPos","SmplInjVol",
        #     "DilutFact","WghtToVol","Type","RackPos","PlatePos",
        #     "SetName","OutputFile"
        #     ]

        required_headers = [
            "sample_name", "sample_type",
            "comments", "acquisition_method", "processing_method",
            "rack_code", "plate_code", "vial_position", "rack_position", "plate_position",
            "injection_volume", "dilution_factor", "weight_to_volume",
            "set_name", "filename"
            ]

        return required_headers

    def parse_metaData(self, meta_data):
        """Parse a sequence file to ensure all headers are present
        
        Args:
            meta_data (dict): a dictionary of sample information

        Returns:
            dict: meta_data
        """

        sample_types = ["Unknown", "Standard", "QC", "Blank", "Double Blank", "Solvent"]
        sample_types_str = ",".join(sample_types)

        # check for required headers
        for header in self.getRequiredHeaders():
            if header not in meta_data:
                print(
                    'SequenceFile Error: required header in sequence list "' +
                    header + '" not found.')
                raise NameError('sequenceFile header')
                # meta_data[header] = None  # not needed
            
        # check for correctness of data
        if meta_data["sample_name"] is None:
            print(
                "SequenceFile Error: sample_name must be specified.")
            raise NameError('sample name')
        if meta_data["filename"] is None:
            print(
                "SequenceFile Error: filename must be specified.")
            raise NameError('filename name')

        if meta_data["sample_type"] is None or\
            meta_data["sample_type"] not in sample_types:
            print(
                "SequenceFile Error: sample_type for sample_name " +
                meta_data["sample_name"] + " is not correct.")
            print(
                "Supported samples types are the following: " +
                sample_types_str)
            raise NameError('sample type')

        # other checks...

        return meta_data

    def addFeatureMapToSequence(self, sample_name, featureMap):
        """add a featureMap to an existing sequence

        Args:
            sample_name (str): name of the sample (must be unique!)
            featureMap (FeatureMap): processed data in a FeatureMap

        Returns:
            dict: injection: dictionary of meta_data and FeatureMap
        """

        if sample_name not in self.sample_to_index.keys():
            print(
                "Sample name " + sample_name + " not found in sequence.")
            raise NameError("sample_name")
        else:
            self.sequence[self.sample_to_index[sample_name]]["featureMap"] = featureMap

