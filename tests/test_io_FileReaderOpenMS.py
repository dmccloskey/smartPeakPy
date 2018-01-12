# -*- coding: utf-8 -*-
# modules
from smartPeak.io.FileReader import FileReader
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS
from smartPeak.core.SampleHandler import SampleHandler
from . import data_dir
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class TestFileReaderOpenMS():
    """tests for FileReaderOpenMS
    """

    def load_data(self):
        filereader = FileReader()
        filename_params = '''%s%s''' % (data_dir, "params_1.csv")
        filereader.read_openMSParams(filename_params, ",")
        self.params_1 = filereader.getData()
        filereader.clear_data()
        filename_params = '''%s%s''' % (data_dir, "params_2.csv")
        filereader.read_openMSParams(filename_params, ",")
        self.params_2 = filereader.getData()
        filereader.clear_data()

    def test_load_traML(self):
        sampleHandler = SampleHandler()
        fileReaderOpenMS = FileReaderOpenMS()

        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(sampleHandler, {'traML_csv_i': traML_csv_i})
        assert(sampleHandler.targeted.getTransitions()[0].getPeptideRef() == b'arg-L')
        assert(sampleHandler.targeted.getTransitions()[0].getPrecursorMZ() == 179.0)
        assert(sampleHandler.targeted.getTransitions()[0].getProductMZ() == 136.0)
        assert(sampleHandler.targeted.getTransitions()[50].getPeptideRef() == b'ins')
        assert(sampleHandler.targeted.getTransitions()[50].getPrecursorMZ() == 267.0)
        assert(sampleHandler.targeted.getTransitions()[50].getProductMZ() == 108.0)

    def test_load_MSExperiment(self):
        self.load_data()
        sampleHandler = SampleHandler()
        fileReaderOpenMS = FileReaderOpenMS()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(sampleHandler, {'traML_csv_i': traML_csv_i})

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        fileReaderOpenMS.load_MSExperiment(sampleHandler, {
            'mzML_feature_i': mzML_i},
            MRMMapping_params_I=self.params_1['MRMMapping'])
        assert(sampleHandler.msExperiment.getChromatograms()[
            0].getProduct().getMZ() == 0.0)
        assert(sampleHandler.msExperiment.getChromatograms()[
            0].getPrecursor().getMZ() == 0.0)
        assert(sampleHandler.msExperiment.getChromatograms()[
            0].getNativeID() == b'TIC')
        assert(sampleHandler.chromatogram_map.getChromatograms()[
            0].getProduct().getMZ() == 136.0)
        assert(sampleHandler.chromatogram_map.getChromatograms()[
            0].getPrecursor().getMZ() == 179.0)
        assert(sampleHandler.chromatogram_map.getChromatograms()[
            0].getNativeID() == b'arg-L.arg-L_1.Heavy')

        # # Precursor chromatogramExtraction
        # # load traML
        # traML_csv_i = '''%s%s''' % (data_dir, "traML_2.csv")
        # fileReaderOpenMS.load_TraML({'traML_csv_i': traML_csv_i})

        # # load MSExperiment
        # mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_2.mzML")
        # # chromatogramExtraction_params = {
        # #     "extract_window": 0.5,
        # #     "ppm": False,
        # #     "rt_extraction_window": -1,
        # #     "filter": "tophat",
        # #     "extract_precursors": True
        # # }
        # fileReaderOpenMS.load_MSExperiment({
        #     'mzML_feature_i': mzML_i},
        #     MRMMapping_params_I=self.params_2['MRMMapping'],
        #     chromatogramExtractor_params_I=self.params_2['ChromatogramExtractor'])
        # assert()
        # assert()

    def test_load_Trafo(self):
        self.load_data()
        sampleHandler = SampleHandler()
        fileReaderOpenMS = FileReaderOpenMS()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(sampleHandler, {'traML_csv_i': traML_csv_i})

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        fileReaderOpenMS.load_MSExperiment(sampleHandler, {
            'mzML_feature_i': mzML_i},
            MRMMapping_params_I=self.params_1['MRMMapping'])

        # load trafo
        fileReaderOpenMS.load_Trafo(
            sampleHandler, 
            {},  # {'trafo_csv_i':trafo_csv_i},
            self.params_1['MRMFeatureFinderScoring'])
        assert(isinstance(sampleHandler.trafo, pyopenms.TransformationDescription))

    def test_load_featureMap(self):
        sampleHandler = SampleHandler()
        fileReaderOpenMS = FileReaderOpenMS()

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_1") 
        fileReaderOpenMS.load_featureMap(sampleHandler, {'featureXML_i': featureXML_o})

        assert(sampleHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 266403.0)
        assert(sampleHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
        assert(sampleHandler.featureMap[0].getSubordinates()[
            0].getRT() == 15.8944563381195)  # refactor to use pytest.approx
        assert(sampleHandler.featureMap[50].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 0.0)
        assert(sampleHandler.featureMap[50].getSubordinates()[
            0].getMetaValue("native_id") == b'acon-C.acon-C_1.Heavy')
        assert(sampleHandler.featureMap[50].getSubordinates()[
            0].getRT() == 14.0348804560343)

    def test_load_quantitationMethods(self):
        sampleHandler = SampleHandler()
        fileReaderOpenMS = FileReaderOpenMS()

        # load the quantitation method
        quantitationMethods_csv_i = '''%s%s''' % (
            data_dir, "quantitationMethods_1.csv")
        fileReaderOpenMS.load_quantitationMethods(
            sampleHandler, 
            {'quantitationMethods_csv_i': quantitationMethods_csv_i})
        assert(sampleHandler.quantitationMethods[0].getLLOQ() == 0.25)
        assert(sampleHandler.quantitationMethods[0].getULOQ() == 2.5)
        assert(sampleHandler.quantitationMethods[
            0].getComponentName() == b'23dpg.23dpg_1.Light')

    def test_load_standardsConcentrations(self):
        sampleHandler = SampleHandler()
        fileReaderOpenMS = FileReaderOpenMS()

        # load the quantitation method
        standardsConcentrations_csv_i = '''%s%s''' % (
            data_dir, "standardsConcentrations_1.csv")
        fileReaderOpenMS.load_standardsConcentrations(
            sampleHandler, 
            {'standardsConcentrations_csv_i': standardsConcentrations_csv_i})
        assert(sampleHandler.standardsConcentrations[0].getLLOQ() == 0.25)
        assert(sampleHandler.standardsConcentrations[0].getULOQ() == 2.5)
        assert(sampleHandler.standardsConcentrations[
            0].getComponentName() == b'23dpg.23dpg_1.Light')