# -*- coding: utf-8 -*-
# modules
from smartPeak.core.Utilities import Utilities
from smartPeak.io.FileReader import FileReader
from smartPeak.algorithm.MRMFeatureSelector import MRMFeatureSelector
from smartPeak.algorithm.MRMFeatureValidator import MRMFeatureValidator
from smartPeak.ui.FeaturePlotter import FeaturePlotter
# external
import copy
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class SampleProcessor():
    def __init__(self):
        self.parameters = None

    def clear_data(self):
        """Remove all data"""
        self.parameters = None

    def openSWATH(
        self,
        sample_IO,
        MRMFeatureFinderScoring_params_I={},
        verbose_I=False
    ):
        """Run the openSWATH workflow for a single sample
        
        Args:
            sample_IO (SampleHandler): sample class
            MRMFeatureFinderScoring_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags
                
        """
        if verbose_I:
            print("Picking peaks using OpenSWATH")

        # helper classes
        utilities = Utilities()

        # make the decoys
        # MRMDecoy
        # How are the decoys added into the experiment?

        # Create empty output
        output = pyopenms.FeatureMap()
        
        # set up MRMFeatureFinderScoring (featurefinder) and
        # parse the MRMFeatureFinderScoring params
        featurefinder = pyopenms.MRMFeatureFinderScoring()
        parameters = featurefinder.getParameters()
        parameters = utilities.updateParameters(
            parameters,
            MRMFeatureFinderScoring_params_I,
            )
        featurefinder.setParameters(parameters)    
        
        # set up MRMFeatureFinderScoring (featurefinder) and 
        # run
        featurefinder.pickExperiment(
            sample_IO.chromatogram_map, 
            output, 
            sample_IO.targeted, 
            sample_IO.trafo,
            sample_IO.swath)
        
        sample_IO.featureMap = output

    def filterAndSelect_py(
        self,
        sample_IO,
        filenames_I,
        MRMFeatureFilter_filter_params_I={},
        MRMFeatureSelector_select_params_I={},
        MRMFeatureSelector_schedule_params_I={},
        verbose_I=False
    ):
        """Run the openSWATH post processing filtering workflow for a single sample
        
        Args:
            sample_IO (SampleHandler): sample class
            filenames_I (list): list of filename strings
            MRMFeatureFilter_filter_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags
            MRMFeatureSelector_select_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags
            MRMFeatureSelector_schedule_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags

        Internals:
            features (FeatureMap): output from SWATH workflow
            msExperiment (MSExperiment): 
            targeted (TargetedExperiment): 

        Returns:
            output_selected (FeatureMap): filtered and/or selected features
                
        """
        # variables
        calibrators_csv_i = None
        mrmfeatureqcs_csv_i = None
        if 'calibrators_csv_i'in filenames_I.keys():
            calibrators_csv_i = filenames_I['calibrators_csv_i']
        if 'mrmfeatureqcs_csv_i'in filenames_I.keys():
            mrmfeatureqcs_csv_i = filenames_I['mrmfeatureqcs_csv_i']

        # filter features
        if verbose_I:
            print("Filtering picked features")
        if MRMFeatureFilter_filter_params_I:   
            # set up MRMFeatureFilter and parse the MRMFeatureFilter params
            featureFilter = pyopenms.MRMFeatureFilter()
            parameters = featureFilter.getParameters()
            utilities = Utilities()
            parameters = utilities.updateParameters(
                parameters,
                MRMFeatureFilter_filter_params_I,
                )
            featureFilter.setParameters(parameters) 

            # read in the parameters for the MRMFeatureQC
            featureQC = pyopenms.MRMFeatureQC()
            featureQCFile = pyopenms.MRMFeatureQCFile()
            featureQCFile.load(mrmfeatureqcs_csv_i.encode('utf-8'), featureQC)  

            output_filtered = copy.copy(sample_IO.featureMap)
            featureFilter.FilterFeatureMap(
                output_filtered,
                featureQC,
                sample_IO.targeted)
        else:
            output_filtered = sample_IO.featureMap

        # select features
        if verbose_I:
            print("Selecting picked features")
        featureSelector = MRMFeatureSelector()
        if calibrators_csv_i is not None:
            smartpeak_i = FileReader()
            smartpeak_i.read_csv(calibrators_csv_i, delimiter=',')
            calibrators = smartpeak_i.getData()
            smartpeak_i.clear_data()
        else: 
            calibrators = []
        if MRMFeatureSelector_schedule_params_I:
            output_selected = featureSelector.schedule_MRMFeatures_qmip(
                features=output_filtered,
                tr_expected=calibrators,    
                targeted=sample_IO.targeted,
                schedule_criteria=MRMFeatureSelector_schedule_params_I,                
                score_weights=MRMFeatureSelector_select_params_I
            )
        elif MRMFeatureSelector_select_params_I:
            output_selected = featureSelector.select_MRMFeatures_score(
                output_filtered,
                MRMFeatureSelector_select_params_I)
            # output_selected = featureSelector.select_MRMFeatures_qmip(
            #     features = output_filtered,
            #     tr_expected = calibrators,    
            #     select_criteria = MRMFeatureSelector_select_params_I,     
            # )
        else:
            output_selected = output_filtered

        sample_IO.featureMap = output_selected

    def extract_metaData(self, sample_IO, verbose_I=False):
        """Extracts metadata from the chromatogram

        Args:        
            sample_IO (SampleHandler): sample class

        """
        if verbose_I:
            print("Extracting metadata")

        # initialize output variables
        filename = ''
        samplename = ''
        instrument = ''
        software = ''

        # filename
        loaded_file_path = sample_IO.chromatogram_map.getLoadedFilePath()
        if loaded_file_path is not None:
            filename = loaded_file_path.decode('utf-8').replace('file://', '')
        # filename = '''%s/%s''' %(
        #     chromatograms_mapped.getSourceFiles()[0].getPathToFile().decode('utf-8').replace('file://',''),
        #     chromatograms_mapped.getSourceFiles()[0].getNameOfFile().decode('utf-8'))

        # sample_IO name
        mzml_id = sample_IO.chromatogram_map.getMetaValue(b'mzml_id')
        if mzml_id is not None:
            samplename_list = mzml_id.decode('utf-8').split('-')
            samplename = '-'.join(samplename_list[1:])   

        # instrument
        instrument_name = sample_IO.chromatogram_map.getInstrument().getName()
        if instrument_name is not None:
            instrument = instrument_name.decode('utf-8')
            # software
            software_name = sample_IO.chromatogram_map.getInstrument().getSoftware().getName()
            if software_name is not None:
                software = software_name.decode('utf-8')

        sample_IO.meta_data = {
            "filename": filename,
            "sample_name": samplename,
            "instrument": instrument,
            "software": software
        }

    def validate(
        self,
        sample_IO,
        MRMRFeatureValidator_params_I={},
        verbose_I=False
    ):
        """Validate the selected peaks agains reference data

        Args:
            sample_IO (SampleHandler): sample class

        """
        if verbose_I:
            print("Validating features")

        # map the reference data
        if MRMRFeatureValidator_params_I:
            featureValidator = MRMFeatureValidator()
            features_mapped, validation_metrics = featureValidator.validate_MRMFeatures(
                reference_data=sample_IO.reference_data,
                features=sample_IO.featureMap,
                Tr_window=float(MRMRFeatureValidator_params_I[0]['value'])
                )
            sample_IO.featureMap = features_mapped
            sample_IO.validation_metrics = validation_metrics

    def export_featurePlots(
        self,     
        sample_IO,   
        filenames_I,
        FeaturePlotter_params_I={},
        verbose_I=False
    ):
        """Export plots of peaks with features annotated

        Args:
            sample_IO (SampleHandler): sample class

        """
        if verbose_I:
            print("Plotting peaks with features")
        
        # Handle the filenames
        features_pdf_o = None
        if 'features_pdf_o'in filenames_I.keys():
            features_pdf_o = filenames_I['features_pdf_o']  

        # export diagnostic plots
        if FeaturePlotter_params_I:
            featurePlotter = FeaturePlotter()
            featurePlotter.setParameters(FeaturePlotter_params_I)
            featurePlotter.plot_peaks(
                filename_I=features_pdf_o,
                transitions=sample_IO.targeted,
                chromatograms=sample_IO.chromatogram_map,
                features=sample_IO.featureMap
            )

    def quantifyComponents(self, sample_IO, verbose_I=False):
        """Quantify all unknown samples based on the quantitationMethod
        
        Args:
            sample_IO (SampleHandler)
            
        """        
        if verbose_I:
            print("Quantifying features")

        aq = pyopenms.AbsoluteQuantitation()
        aq.setQuantMethods(sample_IO.quantitationMethods)
        aq.quantifyComponents(sample_IO.featureMap)