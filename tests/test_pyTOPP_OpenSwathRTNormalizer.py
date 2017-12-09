# -*- coding: utf-8 -*-
from smartPeak.core.smartPeak import smartPeak
from smartPeak.core.smartPeak_i import smartPeak_i
from . import data_dir
from smartPeak.pyTOPP.OpenSwathRTNormalizer import OpenSwathRTNormalizer
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class TestOpenSwathRTNormalizer():
    
    def load_data(
        self,
        mzML_feature_i="mzML/150601_0_BloodProject01_PLT_QC_Broth-1.mzML",
        trafo_csv_i="BloodProject01_SWATH_trafo.csv",
        traML_csv_i="BloodProject01_SWATH.csv",
        filename_params="BloodProject01_MRMFeatureFinderScoring_params.csv"
    ):
        """load the test data"""            

        # load and make the transition file for RTNormalization 
        trafo_csv_i = data_dir + "/" + trafo_csv_i
        self.targeted_rt_norm = pyopenms.TargetedExperiment()
        tramlfile = pyopenms.TransitionTSVReader()
        tramlfile.convertTSVToTargetedExperiment(
            trafo_csv_i.encode('utf-8'), 21, self.targeted_rt_norm
            )                  

        # load targeted experiment
        traML_csv_i = data_dir + "/" + traML_csv_i
        self.targeted = pyopenms.TargetedExperiment()  # must use "PeptideSequence"
        if traML_csv_i is not None:
            tramlfile = pyopenms.TransitionTSVReader()
            tramlfile.convertTSVToTargetedExperiment(
                traML_csv_i.encode('utf-8'), 21, self.targeted)

        # load chromatograms
        mzML_feature_i = data_dir + "/" + mzML_feature_i
        self.chromatograms = pyopenms.MSExperiment()
        if mzML_feature_i is not None:
            fh = pyopenms.FileHandler()
            fh.loadExperiment(mzML_feature_i.encode('utf-8'), self.chromatograms)

        # TODO: update to pyopenms.MRMMapping
        # # map transitions to the chromatograms
        # mrmmapper = MRMMapper()
        # self.chromatogram_map = mrmmapper.algorithm(
        #     chromatogram_map=self.chromatograms,
        #     targeted=self.targeted, 
        #     precursor_tolerance=0.0009,  # hard-coded for now
        #     product_tolerance=0.0009,  # hard-coded for now
        #     allow_unmapped=True,
        #     allow_double_mappings=True
        # )
        
        # load the parameters
        filename_params = data_dir + "/" + filename_params
        smartpeak_i = smartPeak_i()
        smartpeak_i.read_openMSParams(filename_params, ",")
        self.params = smartpeak_i.getData()
        smartpeak_i.clear_data()
    
    def test_algorithm(self):
        self.load_data()

        # set up MRMFeatureFinderScoring (featurefinder) and
        # parse the MRMFeatureFinderScoring params
        featurefinder = pyopenms.MRMFeatureFinderScoring()
        parameters = featurefinder.getParameters()
        smartpeak = smartPeak()
        parameters = smartpeak.updateParameters(
            parameters,
            self.params["MRMFeatureFinderScoring"],
            )
        featurefinder.setParameters(parameters)    

        RTNormalizer = OpenSwathRTNormalizer()
        trafo = RTNormalizer.main(
            self.chromatogram_map,
            self.targeted_rt_norm,
            model_params=None,
            model_type="linear",
            min_rsq=0.95,
            min_coverage=0.6,
            estimateBestPeptides=True,
            MRMFeatureFinderScoring_params=parameters
            )
        params = trafo.getModelParameters()
        assert(params.getValue("slope") == 6.254079466897194)
        assert(params.getValue("intercept") == -5.349869779072912)