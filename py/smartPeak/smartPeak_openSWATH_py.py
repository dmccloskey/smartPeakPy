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

class smartPeak_openSWATH_py():
    def __init__(self):
        pass

    def openSWATH_py(self,
        filenames_I,
        MRMFeatureFinderScoring_params_I={},
        ):
        """Run the openSWATH workflow for a single sample
        
        Args
            filenames_I (list): list of filename strings
            MRMFeatureFinderScoring_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags
                
        """
        # variables
        mzML_feature_i = filenames_I['mzML_feature_i']
        traML_csv_i = filenames_I['traML_csv_i']
        traML_i = filenames_I['traML_i']
        featureXML_o = filenames_I['featureXML_o']
        feature_csv_o = filenames_I['feature_csv_o']
        # dia_csv_i = filenames_I['dia_csv_i']
        MRMFeatureFinderScoring_params = MRMFeatureFinderScoring_params_I

        #helper classes
        smartpeak = smartPeak()

        # load chromatograms
        chromatograms = pyopenms.MSExperiment()
        fh = pyopenms.FileHandler()
        fh.loadExperiment(mzML_feature_i.encode('utf-8'), chromatograms)

        # load and make the transition file
        targeted = pyopenms.TargetedExperiment()
        tramlfile = pyopenms.TransitionTSVReader()
        tramlfile.convertTSVToTargetedExperiment(traML_csv_i.encode('utf-8'),21,targeted)
        # #load transitions file
        # targeted = pyopenms.TargetedExperiment()
        # tramlfile = pyopenms.TraMLFile()
        # tramlfile.load(traML_i.encode('utf-8'), targeted)

        # map transitions to the chromatograms
        # BUG: loss of precision of transition
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

        # Normalize the RTs
        trafo = pyopenms.TransformationDescription()

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
        
        # set up MRMFeatureFinderScoring (featurefinder) and 
        # run
        featurefinder.pickExperiment(chromatograms, output, targeted, trafo, empty_swath)

        # Store outfile as featureXML
        featurexml = pyopenms.FeatureXMLFile()
        featurexml.store(featureXML_o.encode('utf-8'), output)

        # Store the outfile as csv
        #todo: https://github.com/sneumann/OpenMS/blob/master/pyOpenMS/pyTOPP/OpenSwathFeatureXMLToTSV.py

        # select features