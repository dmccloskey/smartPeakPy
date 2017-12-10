# -*- coding: utf-8 -*-
import csv
import sys
import copy


class smartPeak_i():
    """a class to import data"""  

    def __init__(self):
        self.data = []

    def clear_data(self):
        """clear existing data"""
        # del self.data[:]
        self.data = []

    def getData(self):
        """get data
        
        Returns
            data (list,dict)
            
        """
        return copy.copy(self.data)

    def setData(self, data_I):
        """set data
        Args
            data_I (list,dict)
            
        """
        self.data = data_I
                   
    def read_csv(self, filename, delimiter=','):
        """read table data from csv file"""
        try:
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=delimiter)
                try:
                    keys = reader.fieldnames
                    for row in reader:
                        self.data.append(row)
                except csv.Error as e:
                    sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
        except IOError as e:
            sys.exit('%s does not exist' % e) 

    def parse_openMSParams(self):
        """parse parameters from csv file

        Args:
            data_I (list): e.g. [
            {'function': 'ConvertTSVToTraML', 'name': '-in', 'value': 'IsolateA1.csv'},
            {'function': 'ConvertTSVToTraML', 'name': '-out', 'value': 'IsolateA1.traML'},
            {'function': 'MRMMapper', 'name': '-in', 'value': 'IsolateA1.mzML'},
            {'function': 'MRMMapper', 'name': '-tr', 'value': 'IsolateA1.traML'},
            {'function': 'MRMMapper', 'name': '-out', 'value': 'IsolateA1.csv'},
            {'function': 'MRMMapper', 'name': '-precursor_tolerance','value':0.5},
            {'function': 'MRMMapper', 'name': '-product_tolerance','value':0.5},
            {'function': 'MRMMapper', 'name': '-no-strict','value':''},
            ]

        Returns:
            dict: data_O: e.g. {
                'ConvertTSVToTraML':[
                    {'name':'-in','value':'IsolateA1.csv'},
                    {'name':'-out','value':'IsolateA1.traML'}
                ]},
                {'MRMMapper':[
                    {'name':'-in','value':'IsolateA1.mzML'},
                    {'name':'-tr','value':'IsolateA1.traML'},
                    {'name':'-out','value':'IsolateA1_features.mzML'},
                    {'name':'-precursor_tolerance','value':0.5},
                    {'name':'-product_tolerance','value':0.5},
                    {'name':'-no-strict','value':''}
                ]}
        """

        data_I = self.getData()
        data_O = {}
        function_current = ''
        function_params = {}
        for i, d in enumerate(data_I):
            # skip non-used lines
            if not d['used_'] or d['used_'] == "FALSE":
                continue
            # update function_current
            function_current = d['function']
            if function_current not in data_O.keys():
                data_O[function_current] = []
            # make the function parameter line
            function_param = {}
            function_param['name'] = d['name']
            function_param['value'] = d['value']
            if 'tags' in d.keys():
                function_param['tags'] = d['tags']
            if 'description' in d.keys():
                function_param['description'] = d['description']
            if 'type' in d.keys():
                function_param['type'] = d['type']
            data_O[function_current].append(function_param)
        self.setData(data_O)

    def read_openMSParams(self, filename, delimiter):
        """read table data from csv file representing
        representing the method arguments to run the
        openMS methods

        Args:
            filename (str): header should include the following:
                function,
                name,
                value,
                type (optional),
                tag (optional),
                description (optional)
                used_,
                comment_ (optional)

        """
        self.read_csv(filename, delimiter)
        self.parse_openMSParams()
        
    def parse_pythonParams(self):
        """parse parameters from csv file

        Args:
            data_I (list): e.g. [
            {'function': 'ConvertTSVToTraML', 'name': '-in', 'value': 'IsolateA1.csv'},
            {'function': 'ConvertTSVToTraML', 'name': '-out', 'value': 'IsolateA1.traML'},
            {'function': 'MRMMapper', 'name': '-in', 'value': 'IsolateA1.mzML'},
            {'function': 'MRMMapper', 'name': '-tr', 'value': 'IsolateA1.traML'},
            {'function': 'MRMMapper', 'name': '-out', 'value': 'IsolateA1.csv'},
            {'function': 'MRMMapper', 'name': '-precursor_tolerance','value':0.5},
            {'function': 'MRMMapper', 'name': '-product_tolerance','value':0.5},
            {'function': 'MRMMapper', 'name': '-no-strict','value':''},
            ]

        Returns:
            list: data_O: e.g. [
                {'ConvertTSVToTraML':[
                    {'-in':'IsolateA1.csv'},
                    {'-out':'IsolateA1.traML'}
                ]},
                {'MRMMapper':[
                    {'-in':'IsolateA1.mzML'},
                    {'-tr':'IsolateA1.traML'},
                    {'-out':'IsolateA1_features.mzML'},
                    {'-precursor_tolerance':0.5},
                    {'-product_tolerance':0.5},
                    {'-no-strict':''}
                ]}
                ]
        """
        data_I = self.getData()
        data_O = {}
        for i, d in enumerate(data_I):
            # skip non-used lines
            if not d['used_'] or d['used_'] == "FALSE":
                continue
            # update function_current
            function_current = d['function']
            if function_current not in data_O.keys():
                data_O[function_current] = {}
            # make the function parameter line
            function_param = {}
            function_param[d['name']] = d['value']
            data_O[function_current].update(function_param)
        self.setData(data_O)

    def read_pythonParams(self, filename, delimiter):
        """read table data from csv file representing
        representing the method arguments to run the
        any generic python function

        Args:
            filename (str): header should include the following:
                function,
                name,
                value,
                type (optional),
                tag (optional),
                description (optional)
                used_,
                comment_ (optional)

        """
        self.read_csv(filename, delimiter)
        self.parse_pythonParams()