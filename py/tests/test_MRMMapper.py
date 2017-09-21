# -*- coding: utf-8 -*-
from smartPeak.core.smartPeak import smartPeak
from . import data_dir
from smartPeak.pyTOPP.MRMMapper import MRMMapper
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class TestMRMMapper():
    
    def load_data(self,
        mzML_feature_i = "150601_0_BloodProject01_PLT_QC_Broth-1.mzML",
        traML_csv_i = "BloodProject01_SWATH.csv"):
        """load the test data"""            

        # load targeted experiment
        traML_csv_i = data_dir + "/" + traML_csv_i
        self.targeted = pyopenms.TargetedExperiment() #must use "PeptideSequence"
        if not traML_csv_i is None:
            tramlfile = pyopenms.TransitionTSVReader()
            tramlfile.convertTSVToTargetedExperiment(traML_csv_i.encode('utf-8'),21,self.targeted)

        # load chromatograms
        mzML_feature_i = data_dir + "/" + mzML_feature_i
        self.chromatograms = pyopenms.MSExperiment()
        if not mzML_feature_i is None:
            fh = pyopenms.FileHandler()
            fh.loadExperiment(mzML_feature_i.encode('utf-8'), self.chromatograms)
    
    def test_algorithm(self):
        self.load_data()
        mrmmapper = MRMMapper()
        chromatogram_map = mrmmapper.algorithm(
            chromatogram_map=self.chromatograms,
            targeted=self.targeted, 
            precursor_tolerance=0.0009, #hard-coded for now
            product_tolerance=0.0009, #hard-coded for now
            allow_unmapped=True,
            allow_double_mappings=True)
        assert(chromatogram_map.getChromatograms()[0].getNativeID() == b'arg-L.arg-L_1.Heavy')
        assert(chromatogram_map.getChromatograms()[0].getPrecursor().getMZ() == 179.0)
        assert(chromatogram_map.getChromatograms()[0].getProduct().getMZ() == 136.0)
        assert(chromatogram_map.getChromatograms()[50].getNativeID() == b'ins.ins_2.Light')
        assert(chromatogram_map.getChromatograms()[50].getPrecursor().getMZ() == 267.0)
        assert(chromatogram_map.getChromatograms()[50].getProduct().getMZ() == 108.0)