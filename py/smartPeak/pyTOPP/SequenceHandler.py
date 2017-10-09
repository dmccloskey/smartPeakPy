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

    def makeDataMatrixFromMetaValue(self, meta_value = 'calculated_concentrations',
        sample_types = ['Unknown']):
        """make a data matrix from a feature metaValue for 
            specified sample types

        Args:
            meta_value (string): name of the feature metaValue
            sample_types (list): list of strings corresponding to sample types

        Returns:
            list: columns: list of sample_names
            list: rows: list of tuples corresponding to component_name and component_group_name
            np.array: data: numpy data array of metaValues

        """
        # headers = [d['meta_value']['sample_name'] for d in self.sequence if d['meta_value']['sample_type'] in sample_types]
        # columns = ['component_name','component_group_name'] + headers

        columns = set()
        rows = set()

        # collect the metaValues
        data_dict = {}
        for d in self.sequence:
            if d['meta_value']['sample_type'] in sample_types:
                sample_name = d['meta_value']['sample_name']
                for feature in d['featureMap']:
                    component_group_name = feature.getMetaValue("PeptideRef").decode('utf-8')
                    for subordinate in feature.getSubordinates():
                        row_list_name = [component_group_name]
                        row_list_name.append(subordinate.getMetaValue('native_id').decode('utf-8'))
                        datum = subordinate.getMetaValue('calculated_concentration')
                        if datum and not datum is None:
                            data_dict[sample_name] = {}
                            data_dict[sample_name][row_list_name] = datum
                            columns.add(sample_name)
                            rows.add(row_list_name)
        columns = list(columns)
        columns.sort()
        rows = list (rows)
        rows.sort()

        # make the data matrix
        data = np.empty((len(rows),len(columns)))
        data.fill(np.nan)
        for i,r in enumerate(columns):
            for j,c in enumerate(rows):
                if c in data_dict.keys() and r in data_dict[c].keys():
                    data[i,j] = data_dict[c][r]

        return columns, rows, data

    def exportDataMatrixFromMetaValue(self, filename,
        meta_value = 'calculated_concentrations',
        sample_types = ['Unknown']):
        """export data matrix from feature metaValue to .csv

        Args:
            filename (string): name of the file
            ...

        """

        data_O = []
        columns, rows, data = self.makeDataMatrixFromMetaValue(meta_value = meta_value, sample_types = sample_types)
        header = ['component_name','component_group_name'] + columns
        for i,r in enumerate(rows):
            data_O.append(dict(zip(header, r + data[i,:])))
        
        # write dict to csv
        with open(filename, 'w',newline='') as f:
            writer = csv.DictWriter(f, fieldnames = header)
            try:
                writer.writeheader()
                writer.writerows(data_O)
            except csv.Error as e:
                sys.exit(e)