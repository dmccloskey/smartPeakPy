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

    def makeDataMatrixFromMetaValue(
        self,
        meta_values=['calculated_concentration'],
        sample_types=['Unknown']
    ):
        """make a data matrix from a feature metaValue for 
            specified sample types

        Args:
            meta_values (list): 
                list of strings specifying the name of the feature metaValue
            sample_types (list): list of strings corresponding to sample types

        Returns:
            list: columns: list of sample_names
            list: rows: 
                list of tuples corresponding to component_name and component_group_name
            np.array: data: numpy data array of metaValues

        """

        columns = set()
        rows = set()

        # collect the metaValues
        data_dict = {}
        for d in self.sequence:
            if d['meta_data']['sample_type'] in sample_types:
                sample_name = d['meta_data']['sample_name']
                data_dict[sample_name] = {}
                for meta_value in meta_values:
                    for feature in d['featureMap']:
                        component_group_name = feature.getMetaValue(
                            "PeptideRef").decode('utf-8')
                        for subordinate in feature.getSubordinates():
                            row_tuple_name = (
                                component_group_name, 
                                subordinate.getMetaValue(
                                    'native_id').decode('utf-8'), meta_value)
                            datum = self.getMetaValue(feature, subordinate, meta_value)
                            if datum and datum is not None:
                                data_dict[sample_name][row_tuple_name] = datum
                                columns.add(sample_name)
                                rows.add(row_tuple_name)
        columns = list(columns)
        columns.sort()
        rows = list(rows)
        rows.sort()

        # make the data matrix
        data = np.empty((len(rows), len(columns)))
        data.fill(np.nan)
        for i, r in enumerate(rows):
            for j, c in enumerate(columns):
                if c in data_dict.keys() and r in data_dict[c].keys():
                    data[i, j] = data_dict[c][r]

        return columns, rows, data

    def exportDataMatrixFromMetaValue(
        self,
        filename,
        meta_values=['calculated_concentration'],
        sample_types=['Unknown']
    ):
        """export data matrix from feature metaValue to .csv

        Args:
            filename (string): name of the file
            ...

        """

        data_O = []
        columns, rows, data = self.makeDataMatrixFromMetaValue(
            meta_values=meta_values, sample_types=sample_types)
        header = ['component_group_name', 'component_name', 'meta_value'] + columns
        for i, r in enumerate(rows):
            data_O.append(dict(zip(header, list(r) + list(data[i, :]))))
        
        # write dict to csv
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            try:
                writer.writeheader()
                writer.writerows(data_O)
            except csv.Error as e:
                sys.exit(e)

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

    def read_sequenceFile(self, filename, delimiter=','):
        """Import a sequence file"""

        # read in the data
        smartpeak_i = FileReader()
        smartpeak_i.read_csv(filename, delimiter)
        self.parse_sequenceFile(smartpeak_i.getData())
        smartpeak_i.clear_data()

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

    def parse_sequenceFile(self, sequence_file):
        """Parse a sequence file to ensure all headers are present
        
        Args:
            sequenceFile (list): list of dictionaries of sequence information
        """

        for seq in sequence_file:
            self.addSampleToSequence(seq, None)

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

