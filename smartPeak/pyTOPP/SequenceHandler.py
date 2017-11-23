# -*- coding: utf-8 -*-
#utilities
import csv, sys
#modules
from smartPeak.core.smartPeak_i import smartPeak_i
#3rd part libraries
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
        self.sequence_index = {}

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
            'meta_data': meta_data,
            'featureMap': featureMap
        }

        self.sequence.append(injection)
        self.sequence_index[len(self.sequence)-1] = sample_name

    def makeDataMatrixFromMetaValue(self,
        meta_values = ['calculated_concentration'],
        sample_types = ['Unknown']):
        """make a data matrix from a feature metaValue for 
            specified sample types

        Args:
            meta_values (list): list of strings specifying the name of the feature metaValue
            sample_types (list): list of strings corresponding to sample types

        Returns:
            list: columns: list of sample_names
            list: rows: list of tuples corresponding to component_name and component_group_name
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
                        component_group_name = feature.getMetaValue("PeptideRef").decode('utf-8')
                        for subordinate in feature.getSubordinates():
                            row_tuple_name = (component_group_name, subordinate.getMetaValue('native_id').decode('utf-8'), meta_value)
                            datum = self.getMetaValue(feature, subordinate, meta_value)
                            if datum and not datum is None:
                                data_dict[sample_name][row_tuple_name] = datum
                                columns.add(sample_name)
                                rows.add(row_tuple_name)
        columns = list(columns)
        columns.sort()
        rows = list (rows)
        rows.sort()

        # make the data matrix
        data = np.empty((len(rows),len(columns)))
        data.fill(np.nan)
        for i,r in enumerate(rows):
            for j,c in enumerate(columns):
                if c in data_dict.keys() and r in data_dict[c].keys():
                    data[i,j] = data_dict[c][r]

        return columns, rows, data

    def exportDataMatrixFromMetaValue(self, filename,
        meta_values = ['calculated_concentration'],
        sample_types = ['Unknown']):
        """export data matrix from feature metaValue to .csv

        Args:
            filename (string): name of the file
            ...

        """

        data_O = []
        columns, rows, data = self.makeDataMatrixFromMetaValue(meta_values = meta_values, sample_types = sample_types)
        header = ['component_group_name','component_name','meta_value'] + columns
        for i,r in enumerate(rows):
            data_O.append(dict(zip(header, list(r) + list(data[i,:]))))
        
        # write dict to csv
        with open(filename, 'w',newline='') as f:
            writer = csv.DictWriter(f, fieldnames = header)
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