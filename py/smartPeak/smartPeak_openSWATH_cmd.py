# coding: utf-8
#system
import csv, sys
#module
from .smartPeak import smartPeak
from .smartPeak_i import smartPeak_i


class smartPeak_openSWATH_cmd():
    def __init__(self, openSWATH_cmd_params_I=None):

        if openSWATH_cmd_params_I and not openSWATH_cmd_params_I is None:
            self.openSWATH_cmd_params = openSWATH_cmd_params_I
        else:
            self.openSWATH_cmd_params = None

    def openSWATH_cmd(self, verbose_I=False):
        """openSWATH command line workflow
        
        FUNCTION ORDER:
        TargetedFileConverter : convert csv list of target compounds to traML
        MRMMapper: annotate raw .mzML
        OpenSwathDecoyGenerator: make the decoys
        OpenSwathChromatogramExtractor: extraction out ms2 data
        OpenSwathRTNormalizer: normalize the retention times
        OpenSwathAnalyzer: pick peaks and score chromatograms
        OpenSwathFeatureXMLToTSV: convert to csv
        OpenSwathConfidenceScoring: score the picked peaks
        OpenSwathFeatureXMLToTSV: convert to csv
        """
        smartpeak = smartPeak()
        for line in self.openSWATH_cmd_params:
            for fnc, params in line.items():
                cmd = smartpeak.make_osCmd(params, fnc)
                smartpeak.run_osCmd(cmd, verbose_I=verbose_I)

    def parse_openSWATH_cmd_params(self, data_I):
        """parse parameters from csv file

        Args
            data_I (list): e.g. [
                {'function': 'TargetedFileConverter ', 'name': '-in', 'delim': ' ', 'value': 'IsolateA1.csv'},
                {'function': 'TargetedFileConverter ', 'name': '-out', 'delim': ' ', 'value': 'IsolateA1.traML'},
                {'function': 'MRMMapper', 'name': '-in', 'delim': ' ', 'value': 'IsolateA1.mzML'},
                {'function': 'MRMMapper', 'name': '-tr', 'delim': ' ', 'value': 'IsolateA1.traML'},
                {'function': 'MRMMapper', 'name': '-out', 'delim': ' ', 'value': 'IsolateA1.csv'},
                {'function': 'MRMMapper', 'name': '-precursor_tolerance','delim':' ','value':0.5},
                {'function': 'MRMMapper', 'name': '-product_tolerance','delim':' ','value':0.5},
                {'function': 'MRMMapper', 'name': '-no-strict','delim':' ','value':''},
            ]

        Returns
            data_O (list): e.g. [
                {'ConvertTSVToTraML':[
                    {'param':'-in','delim':' ','value':'IsolateA1.csv'},
                    {'param':'-out','delim':' ','value':'IsolateA1.traML'}
                ]},
                {'MRMMapper':[
                    {'param':'-in','delim':' ','value':'IsolateA1.mzML'},
                    {'param':'-tr','delim':' ','value':'IsolateA1.traML'},
                    {'param':'-out','delim':' ','value':'IsolateA1_features.mzML'},
                    {'param':'-precursor_tolerance','delim':' ','value':0.5},
                    {'param':'-product_tolerance','delim':' ','value':0.5},
                    {'param':'-no-strict','delim':' ','value':''}
                ]}
                ]
        """
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
                function_params = {function_current:[]}
            #make the function parameter line
            function_param = {}
            function_param['param'] = d['name']
            function_param['delim'] = d['delim']
            function_param['value'] = d['value']
            function_params[function_current].append(function_param)
            #add in the last value
            if i==len(data_I)-1:
                data_O.append(function_params)
        return data_O

    def read_openSWATH_cmd_params(self,
        filename,
        delimiter = ','):
        """read table data from csv file representing
        representing the command line arguments to run the
        openSWATH workflow

        Args
            filename (str): header should include the following:
                order,
                function,
                name,
                delim,
                value,
                type,
                table,
                used_,
                comment_
            delimiiter (str): default = ','

        """
        smartpeak_i = smartPeak_i();
        smartpeak_i.read_csv(filename,delimiter)
        data_csv = smartpeak_i.getData();
        smartpeak_i.clear_data();
        data_params = self.parse_openSWATH_cmd_params(data_csv)
        self.openSWATH_cmd_params = data_params
