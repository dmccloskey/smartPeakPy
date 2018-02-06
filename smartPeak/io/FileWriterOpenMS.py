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
        sequenceSegmentHandler_IO,
        quantitationMethods_csv_o,
        verbose_I=False
    ):
        """Store AbsoluteQuantitationMethods

        Args:
            sequenceSegmentHandler_IO (SampleHandler)
            quantitationMethods_csv_o (str): filename

        Internals:
            quantitationMethods (list): list of AbsoluteQuantitationMethod objects

        """
        if verbose_I:
            print("storing quantitation methods")

        if quantitationMethods_csv_o is not None:
            aqmf = pyopenms.AbsoluteQuantitationMethodFile()
            aqmf.store(
                quantitationMethods_csv_o, 
                sequenceSegmentHandler_IO.getQuantitationMethods())

    def store_featureMap(
        self,
        rawDataHandler_IO,
        featureXML_o,
        feature_csv_o,
        verbose_I=False
    ):
        """Store FeatureMap as .xml and .csv
        
        Args:
            rawDataHandler_IO (SampleHandler): sample object; updated in place
            featureXML_o (str): .FeatureXML filename
            feature_csv_o (str): .csv filename
        """
        if verbose_I:
            print("Storing FeatureMap")

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