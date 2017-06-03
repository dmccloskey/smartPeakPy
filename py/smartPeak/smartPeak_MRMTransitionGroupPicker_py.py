# coding: utf-8
#modules
from .smartPeak import smartPeak
from .pyTOPP.MRMMapper import MRMMapper
from .pyTOPP.OpenSwathChromatogramExtractor import OpenSwathChromatogramExtractor
from .pyTOPP.OpenSwathRTNormalizer import OpenSwathRTNormalizer
from .pyTOPP.OpenSwathFeatureXMLToTSV import OpenSwathFeatureXMLToTSV
# from .pyTOPP.MRMGroupMapper import MRMGroupMapper
from .pyTOPP.MRMTransitionGroupPicker import MRMTransitionGroupPicker
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class smartPeak_MRMTransitionGroupPicker_py():
    def __init__(self):
        pass

    def DIASpectrumExtractor_py(self,
        filenames_I,
        DIASpectrumExtractor_params_I={},
        ):
        """Isotope labeled quantification workflow for a single sample
        
        Args
            filenames_I (list): list of filename strings
            DIASpectrumExtractor_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags
                
        """
        # variables
        mzML_feature_i,traML_csv_i,traML_i,featureXML_o,feature_csv_o,dia_csv_i = None,None,None,None,None,None
        if 'mzML_feature_i'in filenames_I.keys(): mzML_feature_i = filenames_I['mzML_feature_i']
        if 'traML_csv_i'in filenames_I.keys(): traML_csv_i = filenames_I['traML_csv_i']
        if 'traML_i'in filenames_I.keys(): traML_i = filenames_I['traML_i']
        if 'featureXML_o'in filenames_I.keys(): featureXML_o = filenames_I['featureXML_o']
        if 'feature_csv_o'in filenames_I.keys(): feature_csv_o = filenames_I['feature_csv_o']
        if 'dia_csv_i'in filenames_I.keys(): dia_csv_i = filenames_I['dia_csv_i']
        DIASpectrumExtractor_params = DIASpectrumExtractor_params_I

        #helper classes
        smartpeak = smartPeak()

        # load spectrums
        spectrums = pyopenms.MSExperiment()
        fh = pyopenms.FileHandler()
        fh.loadExperiment(mzML_feature_i.encode('utf-8'), spectrums)

        # # apply a filter
        # filter = pyopenms.SavitzkyGolayFilter()
        # filter.filterExperiment(spectrums)
        # file = pyopenms.MzMLFile()
        # file.store('/home/user/openMS_MRMworkflow/QC1_p.mzML',spectrums)

        # load and make the transition file
        targeted = pyopenms.TargetedExperiment()
        tramlfile = pyopenms.TransitionTSVReader()
        tramlfile.convertTSVToTargetedExperiment(traML_csv_i.encode('utf-8'),21,targeted)
        # #load transitions file
        # targeted = pyopenms.TargetedExperiment()
        # tramlfile = pyopenms.TraMLFile()
        # tramlfile.load(traML_i.encode('utf-8'), targeted)

        # load in the DIA data
        empty_swath = pyopenms.MSExperiment()
        chromatogramExtractor = OpenSwathChromatogramExtractor()
        empty_swath=chromatogramExtractor.main(
            infiles=[diaXML_i.encode('utf-8')],
            targeted=targeted,
            extraction_window=0.05,
            min_upper_edge_dist=0.0,
            ppm=False,
            is_swath=False,
            rt_extraction_window=-1,
            extraction_function="tophat"
        )

    def MRMTransitionGroupPicker_py(self,
        filenames_I,
        MRMTransitionGroupPicker_params_I={},
        MRMFeatureFinderScoring_params_I={},
        ):
        """Isotope labeled quantification workflow for a single sample
        
        Args
            filenames_I (list): list of filename strings
            MRMTransitionGroupPicker_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags
                
        """
        # variables
        mzML_feature_i,traML_csv_i,traML_i,featureXML_o,feature_csv_o,dia_csv_i = None,None,None,None,None,None
        if 'mzML_feature_i'in filenames_I.keys(): mzML_feature_i = filenames_I['mzML_feature_i']
        if 'traML_csv_i'in filenames_I.keys(): traML_csv_i = filenames_I['traML_csv_i']
        if 'traML_i'in filenames_I.keys(): traML_i = filenames_I['traML_i']
        if 'featureXML_o'in filenames_I.keys(): featureXML_o = filenames_I['featureXML_o']
        if 'feature_csv_o'in filenames_I.keys(): feature_csv_o = filenames_I['feature_csv_o']
        if 'dia_csv_i'in filenames_I.keys(): dia_csv_i = filenames_I['dia_csv_i']
        if 'trafo_csv_i'in filenames_I.keys(): trafo_csv_i = filenames_I['trafo_csv_i']

        #helper classes
        smartpeak = smartPeak()

        # load chromatograms
        chromatograms = pyopenms.MSExperiment()
        fh = pyopenms.FileHandler()
        fh.loadExperiment(mzML_feature_i.encode('utf-8'), chromatograms)

        # # apply a filter
        # filter = pyopenms.SavitzkyGolayFilter()
        # filter.filterExperiment(chromatograms)
        # file = pyopenms.MzMLFile()
        # file.store('/home/user/openMS_MRMworkflow/QC1_p.mzML',chromatograms)

        # load and make the transition file
        # targeted = pyopenms.TargetedExperiment()
        targeted = pyopenms.LightTargetedExperiment() #must use "CompoundName"
        tramlfile = pyopenms.TransitionTSVReader()
        tramlfile.convertTSVToTargetedExperiment(traML_csv_i.encode('utf-8'),21,targeted)
        # #load transitions file
        # targeted = pyopenms.TargetedExperiment()
        # tramlfile = pyopenms.TraMLFile()
        # tramlfile.load(traML_i.encode('utf-8'), targeted)

        # map transitions to the chromatograms
        mrmmapper = MRMMapper()
        chromatograms_mapped = mrmmapper.algorithm(
            chromatogram_map=chromatograms,
            targeted=targeted, 
            precursor_tolerance=0.0005,
            product_tolerance=0.0005, 
            allow_unmapped=True,
            allow_double_mappings=True
        )

        
        # set up MRMFeatureFinderScoring (featurefinder) and
        # parse the MRMFeatureFinderScoring params
        featurefinder = pyopenms.MRMFeatureFinderScoring()
        parameters = featurefinder.getParameters()
        parameters = smartpeak.updateParameters(
            parameters,
            MRMFeatureFinderScoring_params_I,
            )
        featurefinder.setParameters(parameters)        

        # # prepare the model parameters for RTNormalization (interpolation)
        # model_params_list = [{'name':'interpolation_type','value':'linear','type':'string'},
        #     {'name':'extrapolation_type','value':'two-point-linear','type':'string'},
        # ]
        # model_params = pyopenms.Param()
        # model_params = smartpeak.setParameters(model_params_list,model_params)

        # load and make the transition file for RTNormalization 
        targeted_rt_norm = pyopenms.TargetedExperiment()
        tramlfile.convertTSVToTargetedExperiment(
            trafo_csv_i.encode('utf-8'),21,targeted_rt_norm
            )

        # Normalize the RTs
        # NOTE: same MRMFeatureFinderScoring params will be used to pickPeaks
        RTNormalizer = OpenSwathRTNormalizer()
        #trafo_out = pyopenms.TransformationDescription()
        trafo = RTNormalizer.main(
            chromatograms_mapped,
            targeted_rt_norm,
            model_params=None,
            # model_params=model_params,
            model_type="linear",
            # model_type="interpolated",
            min_rsq=0.95,
            min_coverage=0.6,
            estimateBestPeptides=True,
            MRMFeatureFinderScoring_params=parameters
            )
        
        # set up MRMTransitionGroupPicker (picker) and
        # parse the MRMTransitionGroupPicker params
        trgroup_picker = pyopenms.MRMTransitionGroupPicker()
        parameters = trgroup_picker.getParameters()
        parameters = smartpeak.updateParameters(
            parameters,
            MRMTransitionGroupPicker_params_I,
            )
        trgroup_picker.setParameters(parameters)

        # set up the MRMFeatureFinderScoring (feature finder) and
        # parse the MRMFeatureFinderScoring params
        featurefinder = pyopenms.MRMFeatureFinderScoring()
        parameters = featurefinder.getParameters()
        parameters = smartpeak.updateParameters(
            parameters,
            MRMFeatureFinderScoring_params_I,
            )
        featurefinder.setParameters(parameters) 

        # Create empty Swath
        empty_swath = pyopenms.MSExperiment()   

        # Create empty output
        output = pyopenms.FeatureMap()

        # set up MRMFeatureFinderScoring and MRMTransitionGroupPicker 
        # and pick/score for ms1
        mrmtrgroup_picker = MRMTransitionGroupPicker()
        # mrmtrgroup_picker.pickTransitionGroups(
        mrmtrgroup_picker.pickExperiment(
            chromatograms_mapped,targeted,
            trgroup_picker,
            featurefinder,
            trafo, [], output, True
            )

        # Store outfile as featureXML
        featurexml = pyopenms.FeatureXMLFile()
        featurexml.store(featureXML_o.encode('utf-8'), output)

        # Store the outfile as csv
        featurescsv = OpenSwathFeatureXMLToTSV()
        featurescsv.store(feature_csv_o, output, targeted, run_id = 'run0', filename = featureXML_o)