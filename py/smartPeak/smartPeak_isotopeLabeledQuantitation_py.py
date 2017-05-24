# coding: utf-8
#modules
from .smartPeak import smartPeak
from .pyTOPP.MRMMapper import MRMMapper
from .pyTOPP.OpenSwathChromatogramExtractor import OpenSwathChromatogramExtractor
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class smartPeak_isotopeLabeledQuantitation_py():
    def __init__(self):
        pass

    def calculateConcentrations(self):
        """Calculate the concentrations 

        Args

        Returns

        """
        pass

    def isotopeLabeledQuantitation_py(self,
        filenames_I,):
        """Isotope labeled quantification workflow for a single sample
        
        Args
            filenames_I (list): list of filename strings
            MRMFeatureFinderScoring_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags
        
        Notes
            requires both heavy and light features in the same featureMap
        
        """

        # variables
        featureXML_i = filenames_I['featureXML_i']
        consensusXML_o = filenames_I['consensusXML_o']

        # load featureMap
        maps = pyopenms.FeatureMap();
        featurexml = pyopenms.FeatureXMLFile()
        featurexml.load(featureXML_i.encode('utf-8'), maps)

        # group the features
        output = pyopenms.ConsensusMap()
        # #some sort of configuration needs to be done?
        # ConsensusMap out;
        # out.getFileDescriptions()[0].filename = "data/Tutorial Labeled.featureXML";
        # out.getFileDescriptions()[0].size = maps[0].size();
        # out.getFileDescriptions()[0].label = "light";
        # out.getFileDescriptions()[1].filename = "data/Tutorial Labeled.featureXML";
        # out.getFileDescriptions()[1].size = maps[0].size();
        # out.getFileDescriptions()[1].label = "heavy";
        algorithm = pyopenms.FeatureGroupingAlgorithmLabeled()
        # set the parameters
        #params = pyopenms.Param()
        algorithm.group(maps,output)

        # store outfile
        consensus = pyopenms.ConsensusXMLFile();
        consensus_file.store(consensusXML_o.encode('utf-8'), output)
