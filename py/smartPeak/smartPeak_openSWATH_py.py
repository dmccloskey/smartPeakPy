# coding: utf-8
#utilities
import copy
#modules
from .smartPeak import smartPeak
from .pyTOPP.MRMMapper import MRMMapper
from .pyTOPP.OpenSwathChromatogramExtractor import OpenSwathChromatogramExtractor
from .pyTOPP.OpenSwathRTNormalizer import OpenSwathRTNormalizer
from .pyTOPP.OpenSwathFeatureXMLToTSV import OpenSwathFeatureXMLToTSV
from .pyTOPP.MRMFeatureFilter import MRMFeatureFilter
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class smartPeak_openSWATH_py():
    def __init__(self):
        pass

    def openSWATH_py(self,
        filenames_I,
        MRMFeatureFinderScoring_params_I={},
        MRMFeatureFilter_filter_params_I={},
        MRMFeatureFilter_select_params_I={},
        ):
        """Run the openSWATH workflow for a single sample
        
        Args
            filenames_I (list): list of filename strings
            MRMFeatureFinderScoring_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags
                
        """
        # variables
        mzML_feature_i,traML_csv_i,traML_i,\
            featureXML_o,feature_csv_o,dia_csv_i,\
            trafo_csv_i = None,None,None,\
            None,None,None,\
            None
        if 'mzML_feature_i'in filenames_I.keys(): mzML_feature_i = filenames_I['mzML_feature_i']
        if 'traML_csv_i'in filenames_I.keys(): traML_csv_i = filenames_I['traML_csv_i']
        if 'traML_i'in filenames_I.keys(): traML_i = filenames_I['traML_i']
        if 'featureXML_o'in filenames_I.keys(): featureXML_o = filenames_I['featureXML_o']
        if 'feature_csv_o'in filenames_I.keys(): feature_csv_o = filenames_I['feature_csv_o']
        if 'dia_csv_i'in filenames_I.keys(): dia_csv_i = filenames_I['dia_csv_i']
        if 'trafo_csv_i'in filenames_I.keys(): trafo_csv_i = filenames_I['trafo_csv_i']
        if 'calibrators_csv_i'in filenames_I.keys(): calibrators_csv_i = filenames_I['calibrators_csv_i']
        MRMFeatureFinderScoring_params = MRMFeatureFinderScoring_params_I

        #helper classes
        smartpeak = smartPeak()

        # load chromatograms
        chromatograms = pyopenms.MSExperiment()
        fh = pyopenms.FileHandler()
        fh.loadExperiment(mzML_feature_i.encode('utf-8'), chromatograms)

        # load and make the transition file
        targeted = pyopenms.TargetedExperiment() #must use "PeptideSequence"
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

        #make the decoys
        #MRMDecoy
        #How are the decoys added into the experiment?

        # load in the DIA data
        empty_swath = pyopenms.MSExperiment()
        # chromatogramExtractor = OpenSwathChromatogramExtractor()
        # #read in the DIA data files:
        # #dia_files_i = ...(dia_csv_i)
        # empty_swath=chromatogramExtractor.main(
        #     infiles=[],
        #     targeted=targeted,
        #     extraction_window=0.05,
        #     min_upper_edge_dist=0.0,
        #     ppm=False,
        #     is_swath=False,
        #     rt_extraction_window=-1,
        #     extraction_function="tophat"
        # )

        # Create empty output
        output = pyopenms.FeatureMap()
        
        # set up MRMFeatureFinderScoring (featurefinder) and
        # parse the MRMFeatureFinderScoring params
        featurefinder = pyopenms.MRMFeatureFinderScoring()
        parameters = featurefinder.getParameters()
        parameters = smartpeak.updateParameters(
            parameters,
            MRMFeatureFinderScoring_params,
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
        # trafo = pyopenms.TransformationDescription()
        
        # set up MRMFeatureFinderScoring (featurefinder) and 
        # run
        featurefinder.pickExperiment(chromatograms_mapped, output, targeted, trafo, empty_swath)

        # # Store outfile as featureXML
        # featurexml = pyopenms.FeatureXMLFile()
        # featurexml.store(featureXML_o.encode('utf-8'), output)

        # # Store the outfile as csv
        # featurescsv = OpenSwathFeatureXMLToTSV()
        # featurescsv.store(feature_csv_o, output, targeted, run_id = 'run0', filename = featureXML_o)

        # filter and select features
        featureFilter = MRMFeatureFilter()
        output_filtered = featureFilter.filter_MRMFeatures(
            output,
            MRMFeatureFilter_filter_params_I)
        # output_filtered = featureFilter.select_MRMFeatures(
        #     output_filtered,
        #     MRMFeatureFilter_select_params_I)
        from .smartPeak_i import smartPeak_i
        smartpeak_i = smartPeak_i()
        smartpeak_i.read_csv(calibrators_csv_i,delimiter=',')
        calibrators = smartpeak_i.getData()
        smartpeak_i.clear_data()
        output_filtered = featureFilter.align_MRMFeatures(
            features = output_filtered,
            tr_expected = calibrators,            
        )

        # Store outfile as featureXML
        featurexml = pyopenms.FeatureXMLFile()
        featurexml.store(featureXML_o.encode('utf-8'), output_filtered)
        
        # Store the outfile as csv
        featurescsv = OpenSwathFeatureXMLToTSV()
        filename = chromatograms_mapped.getLoadedFilePath().decode('utf-8').replace('file://','')
        samplename_list = chromatograms_mapped.getMetaValue(b'mzml_id').decode('utf-8').split('-')
        samplename = '-'.join(samplename_list[1:])
        featurescsv.store(feature_csv_o, output_filtered, targeted,
            run_id = samplename,
            filename = filename
            )

        # calculate peak intensity and area

        # # other metadata
        # chromatograms_mapped.getInstrument().getName()
        # chromatograms_mapped.getInstrument().getSoftware().getName()
        # filename = '''%s/%s''' %(
        #     chromatograms_mapped.getSourceFiles()[0].getPathToFile().decode('utf-8').replace('file://',''),
        #     chromatograms_mapped.getSourceFiles()[0].getNameOfFile().decode('utf-8'))

