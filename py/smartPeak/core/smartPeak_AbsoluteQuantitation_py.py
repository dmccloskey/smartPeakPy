# -*- coding: utf-8 -*-
# #modules
from smartPeak.pyTOPP.OpenSwathFeatureXMLToTSV import OpenSwathFeatureXMLToTSV
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class smartPeak_AbsoluteQuantitation_py():
    def __init__(self):
        self.unknowns = None
        self.quantitationMethods = None
        self.quantitationStandards = None

    def clear_data(self):
        self.unknowns = None
        self.quantitationMethods = None
        self.quantitationStandards = None

    def load_quantitationMethods(self,
        filenames_I):
        """Load AbsoluteQuantitationMethods

        Args:
            filenames_I (dict): dictionary of filename strings

        Internals:
            quantitationMethods (list): list of AbsoluteQuantitationMethod objects

        """
        quantitationMethods_csv_i = None
        if 'quantitationMethods_csv_i'in filenames_I.keys(): quantitationMethods_csv_i = filenames_I['quantitationMethods_csv_i']

        quantitationMethods = []
        aqmf = pyopenms.AbsoluteQuantitationMethodFile()
        aqmf.load(quantitationMethods_csv_i, quantitationMethods)
        self.quantitationMethods = quantitationMethods

    def store_quantitationMethods(self,
        filenames_I):
        """ """
        pass

    def load_quantitationStandards(self,
        filenames_I):
        """Load AbsoluteQuantitationStandardss

        Args:
            filenames_I (dict): dictionary of filename strings

        Internals:
            quantitationStandards (list): list of AbsoluteQuantitationStandards objects

        """
        quantitationStandards_csv_i = None
        if 'quantitationStandards_csv_i'in filenames_I.keys(): quantitationStandards_csv_i = filenames_I['quantitationStandards_csv_i']

        pass

    def quantifyComponents(self):
        """Quantify all unknown samples based on the quantitationMethod
        
        Args:
            unknowns (list): list of FeatureMaps to quantify
            
        """
        aq = pyopenms.AbsoluteQuantitation()
        aq.setQuantMethods(self.quantitationMethods)
        aq.quantifyComponents(self.unknowns)

    # def load_unknowns(self,
    #     filenames_I):
    #     """Load FeatureMaps to quantify

    #     Args:
    #         filenames_I (dict): dictionary of filename strings

    #     Internals:
    #         unknowns (list): list of FeatureMaps to quantify

    #     """
    #     featureXML_i = None
    #     if 'featureXML_i'in filenames_I.keys(): featureXML_i = filenames_I['featureXML_i']

    #     unknowns = []
    #     for filename in featureXML_i:
    #         featurexml = pyopenms.FeatureXMLFile()
    #         output = pyopenms.FeatureMap()
    #         featurexml.load(filename.encode('utf-8'), output)
    #         unknowns.append(output)

    #     self.setUnknowns(unknowns)

    # def store_unknowns(self,
    #     filenames_I):
    #     """Store quantified FeatureMaps

    #     Args:
    #         filenames_I (dict): dictionary of filename strings
    #     Internals:
    #         unknowns (list): list of FeatureMaps to quantify

    #     """
    #     featureXML_o,feature_csv_o = None,None
    #     if 'featureXML_o'in filenames_I.keys(): featureXML_o = filenames_I['featureXML_o']
    #     if 'feature_csv_o'in filenames_I.keys(): feature_csv_o = filenames_I['feature_csv_o']

    #     mzML_feature_i = None
    #     if 'mzML_feature_i'in filenames_I.keys(): mzML_feature_i = filenames_I['mzML_feature_i']  

    #     traML_csv_i,traML_i = None,None
    #     if 'traML_csv_i'in filenames_I.keys(): traML_csv_i = filenames_I['traML_csv_i']
    #     if 'traML_i'in filenames_I.keys(): traML_i = filenames_I['traML_i']

    #     if not featureXML_o is None and len(featureXML_o)!=len(self.unknowns):
    #         print("The number of filenames (.FeatureXML) and the number of unknowns do not match.")
    #         print("Check that the number and names of the files match the unknowns.")
    #         return

    #     if not feature_csv_o is None and len(feature_csv_o)!=len(self.unknowns):
    #         print("The number of filenames (.csv) and the number of unknowns do not match.")
    #         print("Check that the number and names of the files match the unknowns.")
    #         return

    #     for i in range(len(self.unknowns)):
    #         if not featureXML_o is None:
    #             featurexml = pyopenms.FeatureXMLFile()
    #             featurexml.store(featureXML_o[i].encode('utf-8'), self.unknowns[i])
    #         if not feature_csv_o is None:
    #             openswath = smartPeak_openSWATH_py()
    #             openswath.load_TraML({
    #                 'traML_csv_i':traML_csv_i,
    #                 'traML_i':traML_i
    #                 })
    #             openswath.load_MSExperiment({'mzML_feature_i':mzML_feature_i})
    #             featurescsv = OpenSwathFeatureXMLToTSV()
    #             filename = openswath.chromatogram_map.getLoadedFilePath().decode('utf-8').replace('file://','')
    #             samplename_list = openswath.chromatogram_map.getMetaValue(b'mzml_id').decode('utf-8').split('-')
    #             samplename = '-'.join(samplename_list[1:])   
    #             featurescsv.store(feature_csv_o[i], self.unknowns[i], openswath.targeted,
    #                 run_id = samplename,
    #                 filename = filename
    #                 )

    def setUnknowns(self, unknowns):
        """Set unknown featureMaps
        
        Args:
            unknowns (FeatureMap): FeatureMap to quantify
            
        """
        self.unknowns = [unknowns] #tmp fix until new docker image is ready

    def getUnknowns(self):
        """Set unknown featureMaps
        
        Returns:
            FeatureMap: unknowns: FeatureMaps that was quantified
            
        """
        return self.unknowns[0] #tmp fix until new docker image is ready
