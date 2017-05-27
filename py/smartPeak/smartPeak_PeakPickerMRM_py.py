# coding: utf-8
#modules
from .smartPeak import smartPeak
from .pyTOPP.MRMMapper import MRMMapper
from .pyTOPP.OpenSwathChromatogramExtractor import OpenSwathChromatogramExtractor
from .pyTOPP.MRMGroupMapper import MRMGroupMapper
from .pyTOPP.OpenSwathRTNormalizer import OpenSwathRTNormalizer
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class smartPeak_PeakPickerMRM_py():
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
        mzML_feature_i = filenames_I['mzML_feature_i']
        traML_csv_i = filenames_I['traML_csv_i']
        traML_i = filenames_I['traML_i']
        featureXML_o = filenames_I['featureXML_o']
        feature_csv_o = filenames_I['feature_csv_o']
        diaXML_i = filenames_I['diaXML_i']
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

    def PeakPickerMRM_py(self,
        filenames_I,
        PeakPickerMRM_params_I={},
        ):
        """Isotope labeled quantification workflow for a single sample
        
        Args
            filenames_I (list): list of filename strings
            PeakPickerMRM_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags
                
        """
        # variables
        mzML_feature_i = filenames_I['mzML_feature_i']
        traML_csv_i = filenames_I['traML_csv_i']
        traML_i = filenames_I['traML_i']
        featureXML_o = filenames_I['featureXML_o']
        feature_csv_o = filenames_I['feature_csv_o']
        PeakPickerMRM_params = PeakPickerMRM_params_I

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

        # normalize the RTs
        RTNormalizer = OpenSwathRTNormalizer()
        # parameters = pyopenms.TransformationDescription().getModelParameters()
        # parameters = smartpeak.updateParameters(
        #     parameters,
        #     RTNormalizer_params,
        #     )
        trafo = RTNormalizer.main(
            chromatograms,
            targeted,
            model_params=None,
            # model_params=parameters,
            model_type="lowess",
            min_rsq=0.95,
            min_coverage=0.6,
            estimateBestPeptides=True
            )
        trafo = pyopenms.TransformationDescription()

        # Create empty output
        output = pyopenms.FeatureMap()
        
        # set up PeakPickerMRM (featurefinder) and
        # parse the PeakPickerMRM params
        picker = pyopenms.PeakPickerMRM()
        parameters = picker.getParameters()
        parameters = smartpeak.updateParameters(
            parameters,
            PeakPickerMRM_params,
            )
        picker.setParameters(parameters)
        featurefinder = pyopenms.MRMTransitionGroupPicker()
        parameters = featurefinder.getParameters()
        parameters = smartpeak.updateParameters(
            parameters,
            PeakPickerMRM_params,
            )
        featurefinder.setParameters(parameters)
        
        # set up PeakPickerMRM (featurefinder) and 
        # run
        # testing MRMTransitionGroupPicker
        tgMapper = MRMGroupMapper()
        transitionGroup = tgMapper.main(chromatograms_mapped,targeted)
        featurefinder.pickTransitionGroup(transitionGroup)
        for feature in transitionGroup.getFeatures():
            output.push_back(feature)
        # testing PeakPickerMRM
        chromatograms_picked = pyopenms.MSExperiment()
        for cnt,chromatogram in enumerate(chromatograms.getChromatograms()):
            if cnt==0:
                continue
            chromatogram_picked = pyopenms.MSChromatogram()
            picker.pickChromatogram(chromatogram, chromatogram_picked)
            chromatograms_picked.addChromatogram(chromatogram_picked)
            if chromatogram_picked.size() > 0:
                print("Peaks found for " + str(chromatogram_picked.getNativeID()))
                for i in range(chromatogram_picked.size()):
                    floatDataArrays = '''Peak: %s, Intensity: %s, Left: %s, Right %s'''%(
                        i,chromatogram_picked.getFloatDataArrays()[0][i],
                        chromatogram_picked.getFloatDataArrays()[1][i],
                        chromatogram_picked.getFloatDataArrays()[2][i]
                    )
                    print(floatDataArrays)

        # find features
        #http://ftp.mi.fu-berlin.de/pub/OpenMS/release-documentation/html/classOpenMS_1_1FeatureFinderAlgorithmMRM.html#details
        #FeatureFinderAlgorithmMRM
        #SignalToNoiseEstimatorMedian

        # Store outfile as featureXML
        featurexml = pyopenms.FeatureXMLFile()
        featurexml.store(featureXML_o.encode('utf-8'), output)

        # Store the outfile as csv