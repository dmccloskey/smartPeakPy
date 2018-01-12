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
        filenames_I
    ):
        """ """
        pass

    def store_featureMap(
        self,
        sample_IO,
        filenames_I={},
        verbose_I=False
    ):
        """Store FeatureMap as .xml and .csv
        
        Args:
            sample_IO (SampleHandler): sample object; updated in place
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
            featurexml.store(featureXML_o.encode('utf-8'), sample_IO.featureMap)
        
        # Store the outfile as csv     
        featurescsv = OpenSwathFeatureXMLToTSV()  
        if feature_csv_o is not None:
            featurescsv.store(
                feature_csv_o, sample_IO.featureMap, sample_IO.targeted,
                run_id=sample_IO.meta_data['sample_name'],
                filename=sample_IO.meta_data['filename']
                )

    def store_mzML(self, out, output):
        """
        Store as mzML File

        Args:
            out (str): out filename
            output (): chromatogram object
        """

        pyopenms.MzMLFile().store(out, output)