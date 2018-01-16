# -*- coding: utf-8 -*-
from smartPeak.io.OpenSwathFeatureXMLToTSV import OpenSwathFeatureXMLToTSV
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class FileWriterOpenMS():

    def store_quantitationMethods(
        self,
        sequenceGroupHandler_IO,
        filenames_I={},
        verbose_I=False
    ):
        """Store AbsoluteQuantitationMethods

        Args:
            sequenceGroupHandler_IO (SampleHandler)
            filenames_I (dict): dictionary of filename strings

        Internals:
            quantitationMethods (list): list of AbsoluteQuantitationMethod objects

        """
        if verbose_I:
            print("loading quantitation methods")

        quantitationMethods_csv_i = None
        if 'quantitationMethods_csv_i'in filenames_I.keys():
            quantitationMethods_csv_i = filenames_I['quantitationMethods_csv_i']

        quantitationMethods = []
        aqmf = pyopenms.AbsoluteQuantitationMethodFile()
        aqmf.store(quantitationMethods_csv_i, quantitationMethods)

    def store_featureMap(
        self,
        rawDataHandler_IO,
        filenames_I={},
        verbose_I=False
    ):
        """Store FeatureMap as .xml and .csv
        
        Args:
            rawDataHandler_IO (SampleHandler): sample object; updated in place
            filenames_I (list): list of filename strings
        """
        if verbose_I:
            print("Storing FeatureMap")

        # Handle the filenames
        featureXML_o, feature_csv_o = None, None
        if 'featureXML_o'in filenames_I.keys():
            featureXML_o = filenames_I['featureXML_o']
        if 'feature_csv_o'in filenames_I.keys():
            feature_csv_o = filenames_I['feature_csv_o']

        # Store outfile as featureXML    
        featurexml = pyopenms.FeatureXMLFile()
        if featureXML_o is not None:
            featurexml.store(featureXML_o.encode('utf-8'), rawDataHandler_IO.featureMap)
        
        # Store the outfile as csv     
        featurescsv = OpenSwathFeatureXMLToTSV()  
        if feature_csv_o is not None:
            featurescsv.store(
                feature_csv_o, rawDataHandler_IO.featureMap, rawDataHandler_IO.targeted,
                run_id=rawDataHandler_IO.meta_data['sample_name'],
                filename=rawDataHandler_IO.meta_data['filename']
                )

    def store_mzML(self, out, output):
        """
        Store as mzML File

        Args:
            out (str): out filename
            output (): chromatogram object
        """

        pyopenms.MzMLFile().store(out, output)