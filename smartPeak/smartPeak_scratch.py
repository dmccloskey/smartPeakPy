# coding: utf-8
from .smartPeak import smartPeak

class main():
    def __init__(self,data_dir_I=None):
        if data_dir_I and not data_dir_I is None:
            self.data_dir = data_dir_I
        else:
            self.data_dir = '/home/user/openMS_MRMworkflow/'

        self.cmd_params = [
            #file 1
            {'ConvertTSVToTraML':[
                {'param':'-in','delim':' ','value':self.data_dir+'IsolateA1.csv'},
                {'param':'-out','delim':' ','value':self.data_dir+'IsolateA1.traML'}
            ]},{'MRMMapper':[
                {'param':'-in','delim':' ','value':self.data_dir+'IsolateA1.mzML'},
                {'param':'-tr','delim':' ','value':self.data_dir+'IsolateA1.traML'},
                {'param':'-out','delim':' ','value':self.data_dir+'IsolateA1_features.mzML'},
                {'param':'-precursor_tolerance','delim':' ','value':0.5},
                {'param':'-product_tolerance','delim':' ','value':0.5},
                {'param':'-no-strict','delim':' ','value':''}
            ]},{'OpenSwathAnalyzer':[
                {'param':'-in','delim':' ','value':self.data_dir+'IsolateA1_features.mzML'},
                {'param':'-tr','delim':' ','value':self.data_dir+'IsolateA1.traML'},
                {'param':'-out','delim':' ','value':self.data_dir+'IsolateA1_openSWATH.mzML'},
                {'param':'-no-strict','delim':' ','value':''},
                #TODO parameters
            ]},{'OpenSwathFeatureXMLToTSV':[
                {'param':'-in','delim':' ','value':self.data_dir+'IsolateA1_openSWATH.mzML'},
                {'param':'-tr','delim':' ','value':self.data_dir+'IsolateA1.traML'},
                {'param':'-out','delim':' ','value':self.data_dir+'IsolateA1_openSWATH.csv'},
            ]},
            #file 2
            {'ConvertTSVToTraML':[
                {'param':'-in','delim':' ','value':self.data_dir+'IsolateB1.csv'},
                {'param':'-out','delim':' ','value':self.data_dir+'IsolateB1.traML'}
            ]},{'MRMMapper':[
                {'param':'-in','delim':' ','value':self.data_dir+'IsolateB1.mzML'},
                {'param':'-tr','delim':' ','value':self.data_dir+'IsolateB1.traML'},
                {'param':'-out','delim':' ','value':self.data_dir+'IsolateB1_features.mzML'},
                {'param':'-precursor_tolerance','delim':' ','value':0.5},
                {'param':'-product_tolerance','delim':' ','value':0.5},
                {'param':'-no-strict','delim':' ','value':''},
            ]},{'OpenSwathAnalyzer':[
                {'param':'-in','delim':' ','value':self.data_dir+'IsolateB1_features.mzML'},
                {'param':'-tr','delim':' ','value':self.data_dir+'IsolateB1.traML'},
                {'param':'-out','delim':' ','value':self.data_dir+'IsolateB1_openSWATH.mzML'},
                {'param':'-no-strict','delim':' ','value':''},
                #TODO parameters
            ]},{'OpenSwathFeatureXMLToTSV':[
                {'param':'-in','delim':' ','value':self.data_dir+'IsolateB1_openSWATH.mzML'},
                {'param':'-tr','delim':' ','value':self.data_dir+'IsolateB1.traML'},
                {'param':'-out','delim':' ','value':self.data_dir+'IsolateB1_openSWATH.csv'},
            ]},

        ]

        self.main_params = [{
            'mzML_feature_i': 'IsolateA1_features.mzML',
            'traML_csv_i': 'IsolateA1.csv',
            'traML_i': 'IsolateA1.traML',
            'featureXML_o': 'IsolateA1.featureXML',
            'feature_csv_o': 'IsolateA1_feature.csv',
        }, {
            'mzML_feature_i': 'IsolateB1_features.mzML',
            'traML_csv_i': 'IsolateB1.csv',
            'traML_i': 'IsolateB1.traML',
            'featureXML_o': 'IsolateB1.featureXML',
            'feature_csv_o': 'IsolateB1_feature.csv',
        }]

    def openSWATH_cmd(self,verbose_I=False):
        """openSWATH command line workflow
        
        FUNCTION ORDER:
        ConvertTSVToTraML: convert csv list of target compounds to traML
        MRMMapper: annotate raw .mzML
        OpenSwathDecoyGenerator: make the decoys
        OpenSwathChromatogramExtractor: extraction out ms2 data
        OpenSwathRTNormalizer: normalize the retention times
        OpenSwathAnalyzer: pick peaks and score chromatograms
        OpenSwathFeatureXMLToTSV: convert to csv
        OpenSwathConfidenceScoring: score the picked peaks
        OpenSwathFeatureXMLToTSV: convert to csv
        """
        smartpeak = smartPeak();
        for line in self.cmd_params:
            for fnc,params in line.items():
                cmd = smartpeak.make_osCmd(params,fnc)
                smartpeak.run_osCmd(cmd,verbose_I=verbose_I)                
        

    def _main(main_params):
        for params in main_params:
            # variables
            mzML_feature_i = params['mzML_feature_i']
            traML_csv_i = params['traML_csv_i']
            featureXML_o = params['featureXML_o']
            feature_csv_o = params['feature_csv_o']

            # load chromatograms
            chromatograms = pyopenms.MSExperiment()
            fh = pyopenms.FileHandler()
            fh.loadExperiment(mzML_feature_i, chromatograms)

            # # load and make the transition file
            # targeted = pyopenms.TargetedExperiment();
            # tramlfile=TransitionTSVReader()
            # tramlfile.convertTSVToTargetedExperiment(traML_csv_i,'mrm',targeted)
            # load transitions file
            targeted = pyopenms.TargetedExperiment()
            tramlfile = pyopenms.TraMLFile()
            tramlfile.load(traML_i, targeted)

            #make the decoys
            #MRMDecoy

            # load in the DIA data
            empty_swath = pyopenms.MSExperiment()
            #ChromatogramExtractor

            # normalize the RTs
            trafo = pyopenms.TransformationDescription()
            #MRMRTNormalizer

            # Create empty output
            output = pyopenms.FeatureMap()

            # set up OpenSwath analyzer (featurefinder) and run
            #TODO: need to break into individual functions to create the GUI
            featurefinder = pyopenms.MRMFeatureFinderScoring()
            featurefinder.pickExperiment(chromatograms, output, targeted,
                                         trafo, empty_swath)

            # Store outfile
            featurexml = pyopenms.FeatureXMLFile()
            featurexml.store(featureXML_o, output)
            
            # write out for mProphet




# In[ ]:

# Quantification....

# In[ ]:

# MIsc...
#CachedmzML #read/write mzML

# In[ ]:

# # Tests

# In[26]:

#import pytest


class test_fastPeak():
    """tests for fastPeak"""

    def test_make_osCmd(self, verbose_I=False):
        """"Test make_osCmd function

        EXAMPLE:
        tests = test_fastPeak()
        tests.test_make_osCmd(verbose_I=True)

        """
        #         params = [{'param1':'value1'},
        #                   {'param2':'value2'}]
        params = [
            {
                'param': 'param1',
                'delim': ' ',
                'value': 'value1'
            },
            {
                'param': 'param2',
                'delim': ' ',
                'value': 'value2'
            },
        ]
        function = 'test'
        ans = 'test param1 value1 param2 value2'
        test = smartPeak.make_osCmd(params, function)
        if verbose_I: print(test)
        assert (test == ans)
