# coding: utf-8
#modules
from .smartPeak import smartPeak
#3rd part libraries
import pyopenms

class smartPeak_openSWATH_py():
    def __init__(self,data_dir_I=None):
        if data_dir_I and not data_dir_I is None:
            self.data_dir = data_dir_I
        else:
            self.data_dir = '/home/user/openMS_MRMworkflow/'

        self.openSWATH_py_params = [{
            'mzML_feature_i': self.data_dir+'IsolateA1_features.mzML',
            'traML_csv_i': self.data_dir+'IsolateA1.csv',
            'traML_i': self.data_dir+'IsolateA1.traML',
            'featureXML_o': self.data_dir+'IsolateA1.featureXML',
            'feature_csv_o': self.data_dir+'IsolateA1_feature.csv',
        }, {
            'mzML_feature_i': self.data_dir+'IsolateB1_features.mzML',
            'traML_csv_i': self.data_dir+'IsolateB1.csv',
            'traML_i': self.data_dir+'IsolateB1.traML',
            'featureXML_o': self.data_dir+'IsolateB1.featureXML',
            'feature_csv_o': self.data_dir+'IsolateB1_feature.csv',
        }]

    def openSWATH_py(self):
        for params in self.openSWATH_py_params:
            # variables
            mzML_feature_i = params['mzML_feature_i']
            traML_csv_i = params['traML_csv_i']
            traML_i = params['traML_i']
            featureXML_o = params['featureXML_o']
            feature_csv_o = params['feature_csv_o']

            # load chromatograms
            chromatograms = pyopenms.MSExperiment()
            fh = pyopenms.FileHandler()
            fh.loadExperiment(mzML_feature_i.encode('utf-8'), chromatograms)

            # # load and make the transition file
            # targeted = pyopenms.TargetedExperiment();
            # tramlfile=TransitionTSVReader()
            # tramlfile.convertTSVToTargetedExperiment(traML_csv_i.encode('utf-8'),'mrm',targeted)
            # load transitions file
            targeted = pyopenms.TargetedExperiment()
            tramlfile = pyopenms.TraMLFile()
            tramlfile.load(traML_i.encode('utf-8'), targeted)

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
            featurexml.store(featureXML_o.encode('utf-8'), output)
            
            # write out for mProphet