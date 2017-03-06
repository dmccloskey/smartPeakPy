# coding: utf-8
from .smartPeak import smartPeak

class smartPeak_openSWATH_py():
    def __init__(self,data_dir_I=None):
        if data_dir_I and not data_dir_I is None:
            self.data_dir = data_dir_I
        else:
            self.data_dir = '/home/user/openMS_MRMworkflow/'

        self.openSWATH_py_params = [{
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

    def openSWATH_py(self):
        for params in openSWATH_py_params:
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