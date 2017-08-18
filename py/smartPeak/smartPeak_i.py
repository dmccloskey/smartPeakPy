# -*- coding: utf-8 -*-
import csv,sys
import copy
#custom modules
from io_utilities.base_importData import base_importData

class smartPeak_i(base_importData):
    """a class to import data"""            

    def parse_openMSParams(self):
        """parse parameters from csv file

        Args
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

        Returns
            data_O (dict): e.g. {
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
        function_param = {}
        for i, d in enumerate(data_I):
            #skip non-used lines
            if not d['used_'] or d['used_'] == "FALSE":
                continue
            #update function_current
            if d['function'] != function_current:
                function_current = d['function']
                if function_params:  #append only if list is not empty
                    data_O.update(function_params)
                function_params = {function_current:[]}
            #make the function parameter line
            function_param = {}
            function_param['name'] = d['name']
            function_param['value'] = d['value']
            if 'tags' in d.keys():
                function_param['tags'] = d['tags']
            if 'description' in d.keys():
                function_param['description'] = d['description']
            if 'type' in d.keys():
                function_param['type'] = d['type']
            function_params[function_current].append(function_param)
            #add in the last value
            if i==len(data_I)-1:
                data_O.update(function_params)
        self.setData(data_O)

    def read_openMSParams(self, filename, delimiter):
        """read table data from csv file representing
        representing the method arguments to run the
        openMS methods

        Args
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

        Args
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

        Returns
            data_O (list): e.g. [
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
        data_O = []
        function_current = ''
        function_params = {}
        function_param = {}
        for i, d in enumerate(data_I):
            #skip non-used lines
            if not d['used_'] or d['used_'] == "FALSE":
                continue
            #update function_current
            if d['function'] != function_current:
                function_current = d['function']
                if function_params:  #append only if list is not empty
                    data_O.append(function_params)
                function_params = {function_current:{}}
            #make the function parameter line
            function_param = {}
            function_param[d['name']] = d['value']
            function_params[function_current].update(function_param)
            #add in the last value
            if i==len(data_I)-1:
                data_O.append(function_params)
        self.setData(data_O)

    def read_pythonParams(self, filename, delimiter):
        """read table data from csv file representing
        representing the method arguments to run the
        any generic python function

        Args
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