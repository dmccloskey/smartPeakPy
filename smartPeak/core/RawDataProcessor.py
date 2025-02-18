# -*- coding: utf-8 -*-
# modules
from smartPeak.core.Utilities import Utilities
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS
from smartPeak.io.FileWriterOpenMS import FileWriterOpenMS
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


class RawDataProcessor():
    def __init__(self):
        self.parameters = None

    def clear_data(self):
        """Remove all data"""
        self.parameters = None

    def pickFeatures(
        self,
        rawDataHandler_IO,
        MRMFeatureFinderScoring_params_I={},
        verbose_I=False
    ):
        """Run the openSWATH workflow for a single raw data file
        
        Args:
            rawDataHandler_IO (RawDataHandler): raw data file class
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
        # parse the MRMFeatureFinderScoring parameters
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
            rawDataHandler_IO.chromatogram_map, 
            output, 
            rawDataHandler_IO.targeted, 
            rawDataHandler_IO.trafo,
            rawDataHandler_IO.swath)

        output.setPrimaryMSRunPath([rawDataHandler_IO.getMetaData()[
            "sample_name"].encode("utf-8")])
        rawDataHandler_IO.setFeatureMap(output)

    def filterFeatures(
        self,
        rawDataHandler_IO,
        MRMFeatureFilter_filter_params_I={},
        verbose_I=False
    ):
        """Filter features that do not pass the filter QCs
        
        Args:
            rawDataHandler_IO (RawDataHandler): raw data file class
            MRMFeatureFilter_filter_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags

        Internals:
            features (FeatureMap): output from SWATH workflow
            msExperiment (MSExperiment): 
            targeted (TargetedExperiment): 

        Returns:
            output_filtered (FeatureMap): filtered features
                
        """

        # filter features
        if verbose_I:
            print("Filtering picked features")
        if MRMFeatureFilter_filter_params_I:   
            # set up MRMFeatureFilter and parse the MRMFeatureFilter parameters
            featureFilter = pyopenms.MRMFeatureFilter()
            parameters = featureFilter.getParameters()
            utilities = Utilities()
            parameters = utilities.updateParameters(
                parameters,
                MRMFeatureFilter_filter_params_I,
                )
            featureFilter.setParameters(parameters)   

            # # 1: filter out components
            # feature_filter = copy.copy(rawDataHandler_IO.feature_filter)
            # feature_filter.component_group_qcs = []

            # output_filtered = copy.copy(rawDataHandler_IO.featureMap)
            # featureFilter.FilterFeatureMap(
            #     output_filtered,
            #     feature_filter,
            #     rawDataHandler_IO.targeted)

            # # 2: filter out component groups
            # feature_filter = copy.copy(rawDataHandler_IO.feature_filter)
            # feature_filter.component_qcs = []

            # output_filtered = copy.copy(rawDataHandler_IO.featureMap)
            # featureFilter.FilterFeatureMap(
            #     output_filtered,
            #     feature_filter,
            #     rawDataHandler_IO.targeted)

            output_filtered = copy.copy(rawDataHandler_IO.featureMap)
            featureFilter.FilterFeatureMap(
                output_filtered,
                rawDataHandler_IO.feature_filter,
                rawDataHandler_IO.targeted)

            output_filtered.setPrimaryMSRunPath([rawDataHandler_IO.getMetaData()[
                "sample_name"].encode("utf-8")])
            rawDataHandler_IO.setFeatureMap(output_filtered)

    def checkFeatures(
        self,
        rawDataHandler_IO,
        MRMFeatureFilter_qc_params_I={},
        verbose_I=False
    ):
        """Check that the features pass the QCs
        
        Args:
            rawDataHandler_IO (RawDataHandler): raw data file class
            MRMFeatureFilter_qc_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags

        Internals:
            features (FeatureMap): output from SWATH workflow
            msExperiment (MSExperiment): 
            targeted (TargetedExperiment): 

        Returns:
            output_filtered (FeatureMap): filtered features
                
        """

        # filter features
        if verbose_I:
            print("Checking picked features")
        if MRMFeatureFilter_qc_params_I:   
            # set up MRMFeatureFilter and parse the MRMFeatureFilter parameters
            featureFilter = pyopenms.MRMFeatureFilter()
            parameters = featureFilter.getParameters()
            utilities = Utilities()
            parameters = utilities.updateParameters(
                parameters,
                MRMFeatureFilter_qc_params_I,
                )
            featureFilter.setParameters(parameters)   

            output_filtered = copy.copy(rawDataHandler_IO.featureMap)
            featureFilter.FilterFeatureMap(
                output_filtered,
                rawDataHandler_IO.feature_qc,
                rawDataHandler_IO.targeted)

            output_filtered.setPrimaryMSRunPath([rawDataHandler_IO.getMetaData()[
                "sample_name"].encode("utf-8")])
            rawDataHandler_IO.setFeatureMap(output_filtered)

    def selectFeatures(
        self,
        rawDataHandler_IO,
        MRMFeatureSelector_select_params_I={},
        MRMFeatureSelector_schedule_params_I={},
        verbose_I=False
    ):
        """Run the openSWATH post processing filtering workflow for a single sample
        
        Args:
            rawDataHandler_IO (RawDataHandler): raw data file class
            MRMFeatureSelector_select_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags
            MRMFeatureSelector_schedule_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags

        Internals:
            features (FeatureMap): output from SWATH workflow
            msExperiment (MSExperiment): 
            targeted (TargetedExperiment): 

        Returns:
            output_selected (FeatureMap): selected features
                
        """

        # select features
        if verbose_I:
            print("Selecting picked features")
        featureSelector = MRMFeatureSelector()

        if MRMFeatureSelector_schedule_params_I:
            output_selected = featureSelector.schedule_MRMFeatures_qmip(
                features=rawDataHandler_IO.featureMap,
                targeted=rawDataHandler_IO.targeted,
                schedule_criteria=MRMFeatureSelector_schedule_params_I,                
                score_weights=MRMFeatureSelector_select_params_I
            )
            rawDataHandler_IO.featureMap = output_selected
        elif MRMFeatureSelector_select_params_I:
            output_selected = featureSelector.select_MRMFeatures_score(
                rawDataHandler_IO.featureMap,
                MRMFeatureSelector_select_params_I)
            # output_selected = featureSelector.select_MRMFeatures_qmip(
            #     features = rawDataHandler_IO.featureMap,
            #     tr_expected = calibrators,    
            #     select_criteria = MRMFeatureSelector_select_params_I,     
            # )

            output_selected.setPrimaryMSRunPath([rawDataHandler_IO.getMetaData()[
                "sample_name"].encode("utf-8")])
            rawDataHandler_IO.setFeatureMap(output_selected)

    def extract_metaData(self, rawDataHandler_IO, verbose_I=False):
        """Extracts metadata from the chromatogram

        Args:        
            rawDataHandler_IO (RawDataHandler): raw data file class

        """
        if verbose_I:
            print("Extracting metadata")

        # initialize output variables
        filename = ''
        samplename = ''
        instrument = ''
        software = ''

        # filename
        loaded_file_path = rawDataHandler_IO.chromatogram_map.getLoadedFilePath()
        if loaded_file_path is not None:
            filename = loaded_file_path.decode('utf-8').replace('file://', '')
        # filename = '''%s/%s''' %(
        #     chromatograms_mapped.getSourceFiles()[0].getPathToFile().decode('utf-8').replace('file://',''),
        #     chromatograms_mapped.getSourceFiles()[0].getNameOfFile().decode('utf-8'))

        # rawDataHandler_IO name
        mzml_id = rawDataHandler_IO.chromatogram_map.getMetaValue(b'mzml_id')
        if mzml_id is not None:
            samplename_list = mzml_id.decode('utf-8').split('-')
            samplename = '-'.join(samplename_list[1:])   

        # instrument
        instrument_name = rawDataHandler_IO.chromatogram_map.getInstrument().getName()
        if instrument_name is not None:
            instrument = instrument_name.decode('utf-8')
            # software
            software_name = rawDataHandler_IO.chromatogram_map.getInstrument().getSoftware().getName()
            if software_name is not None:
                software = software_name.decode('utf-8')

        rawDataHandler_IO.meta_data = {
            "filename": filename,
            "sample_name": samplename,
            "instrument": instrument,
            "software": software
        }

    def validateFeatures(
        self,
        rawDataHandler_IO,
        MRMRFeatureValidator_params_I={},
        verbose_I=False
    ):
        """Validate the selected peaks against reference data

        Args:
            rawDataHandler_IO (RawDataHandler): raw data file class

        """
        if verbose_I:
            print("Validating features")

        # map the reference data
        if MRMRFeatureValidator_params_I:
            featureValidator = MRMFeatureValidator()
            features_mapped, validation_metrics = featureValidator.validate_MRMFeatures(
                reference_data=rawDataHandler_IO.reference_data,
                features=rawDataHandler_IO.featureMap,
                Tr_window=float(MRMRFeatureValidator_params_I[0]['value'])
                )

            features_mapped.setPrimaryMSRunPath([rawDataHandler_IO.getMetaData()[
                "sample_name"].encode("utf-8")])
            rawDataHandler_IO.setFeatureMap(features_mapped)
            rawDataHandler_IO.validation_metrics = validation_metrics

    def plotFeatures(
        self,     
        rawDataHandler_IO,   
        features_pdf_o,
        FeaturePlotter_params_I={},
        verbose_I=False
    ):
        """Export plots of peaks with features annotated

        Args:
            rawDataHandler_IO (RawDataHandler): raw data file class
            features_pdf_o (str): filename

        """
        if verbose_I:
            print("Plotting peaks with features")

        # export diagnostic plots
        if FeaturePlotter_params_I and features_pdf_o is not None:
            featurePlotter = FeaturePlotter()
            featurePlotter.setParameters(FeaturePlotter_params_I)
            featurePlotter.plot_peaks(
                filename_I=features_pdf_o,
                transitions=rawDataHandler_IO.targeted,
                chromatograms=rawDataHandler_IO.chromatogram_map,
                features=rawDataHandler_IO.featureMap
            )

    def quantifyComponents(self, rawDataHandler_IO, verbose_I=False):
        """Quantify all unknown samples based on the quantitationMethod
        
        Args:
            rawDataHandler_IO (RawDataHandler)
            
        """        
        if verbose_I:
            print("Quantifying features")

        try:
            aq = pyopenms.AbsoluteQuantitation()
            aq.setQuantMethods(rawDataHandler_IO.quantitation_methods)
            aq.quantifyComponents(rawDataHandler_IO.featureMap)
        except Exception as e:
            print(e)

    def processRawData(
        self, 
        rawDataHandler_IO, 
        raw_data_processing_event,
        parameters,
        filenames={},
        verbose_I=False
    ):
        """Apply processing event to a raw data handler
        
        Args:
            rawDataHandler_IO (RawDataHandler)
            raw_data_processing_event (str): string representation of
                a raw data processing event
            
        """
        fileWriterOpenMS = FileWriterOpenMS()
        fileReaderOpenMS = FileReaderOpenMS()  
        
        try:
            if raw_data_processing_event == "load_raw_data":
                # load dynamic assets            
                fileReaderOpenMS.load_SWATHorDIA(rawDataHandler_IO, {})
                fileReaderOpenMS.load_MSExperiment(
                    rawDataHandler_IO, 
                    filenames["mzML_i"],
                    MRMMapping_params_I=parameters['MRMMapping'],
                    chromatogramExtractor_params_I=parameters['ChromatogramExtractor'],                    
                    mzML_params_I=parameters['mzML'],
                    verbose_I=verbose_I)
                fileReaderOpenMS.load_Trafo(  # skip, no transformation of RT
                    rawDataHandler_IO, 
                    None,
                    MRMFeatureFinderScoring_params_I=parameters['MRMFeatureFinderScoring'])
            elif raw_data_processing_event == "load_features":
                fileReaderOpenMS.load_featureMap(
                    rawDataHandler_IO,
                    filenames["featureXML_i"],
                    verbose_I=verbose_I)
            elif raw_data_processing_event == "pick_features":
                self.pickFeatures(
                    rawDataHandler_IO,
                    parameters['MRMFeatureFinderScoring'],
                    verbose_I=verbose_I)
            elif raw_data_processing_event == "filter_features":
                self.filterFeatures(
                    rawDataHandler_IO,
                    parameters['MRMFeatureFilter.filter_MRMFeatures'],
                    verbose_I=verbose_I)
            elif raw_data_processing_event == "select_features":
                self.selectFeatures(
                    rawDataHandler_IO,
                    # qmip algorithm
                    MRMFeatureSelector_select_params_I=parameters[
                        'MRMFeatureSelector.select_MRMFeatures_qmip'],
                    MRMFeatureSelector_schedule_params_I=parameters[
                        'MRMFeatureSelector.schedule_MRMFeatures_qmip'],
                    # score algorithm
                    # MRMFeatureSelector_select_params_I=parameters[
                    #     'MRMFeatureSelector.select_MRMFeatures_score'],
                    # MRMFeatureSelector_schedule_params_I={},
                    verbose_I=verbose_I)
            elif raw_data_processing_event == "validate_features":
                # load in the validation data 
                # (if no data is found, continue to the next sample)
                ReferenceDataMethods_params_I = []
                ReferenceDataMethods_params_I.extend(
                    parameters['ReferenceDataMethods.getAndProcess_referenceData_samples']
                    )
                sample_names_I = '''['%s']''' % (
                    rawDataHandler_IO.meta_data["sample_name"])
                ReferenceDataMethods_params_I.append({
                    'description': '', 'name': 'sample_names_I', 
                    'type': 'list', 'value': sample_names_I})
                fileReaderOpenMS.load_validationData(
                    rawDataHandler_IO,
                    filenames,
                    ReferenceDataMethods_params_I,
                    verbose_I=verbose_I
                    )
                # TODO: add error class
                # if not rawDataHandler.reference_data:
                #     skipped_samples.append({
                #         'sample_name': rawDataHandler_IO.meta_data["sample_name"],
                #         'error_message': 'no reference data found'})
                #     print(
                #         'Reference data not found for sample ' +
                #         rawDataHandler_IO.meta_data["sample_name"] + '.')
                self.validateFeatures(
                    rawDataHandler_IO,
                    parameters['MRMFeatureValidator.validate_MRMFeatures'],
                    verbose_I=verbose_I)
            elif raw_data_processing_event == "quantify_features":
                self.quantifyComponents(rawDataHandler_IO, verbose_I=verbose_I)
            elif raw_data_processing_event == "check_features":
                self.checkFeatures(
                    rawDataHandler_IO,
                    MRMFeatureFilter_qc_params_I=parameters[
                        'MRMFeatureFilter.filter_MRMFeatures.qc'],
                    verbose_I=verbose_I)
            elif raw_data_processing_event == "store_features":
                fileWriterOpenMS.store_featureMap(
                    rawDataHandler_IO, 
                    filenames["featureXML_o"], 
                    filenames["feature_csv_o"],
                    verbose_I=verbose_I)
            elif raw_data_processing_event == "plot_features":
                self.plotFeatures(
                    rawDataHandler_IO,
                    filenames["features_pdf_o"],
                    FeaturePlotter_params_I=parameters[
                        'FeaturePlotter'],
                    verbose_I=verbose_I)
            elif raw_data_processing_event == "save_features":
                self.saveCurrentFeatureMapToHistory(
                    rawDataHandler_IO,
                    verbose_I=verbose_I)
            elif raw_data_processing_event == "annotate_used_features":
                self.annotateUsedFeatures(
                    rawDataHandler_IO,
                    verbose_I=verbose_I)
            elif raw_data_processing_event == "clear_feature_history":
                rawDataHandler_IO.featureMapHistory = []
            else:
                print(
                    "Raw data processing event " +
                    raw_data_processing_event +
                    " was not recognized.")
        except Exception as e:
            print(e)
            # TODO: add error class
            # skipped_samples.append({
            #     'sample_name': sequence.meta_data["sample_name"],
            #     'error_message': e})

    def checkRawDataProcessingWorkflow(self, raw_data_processing_I):
        """check if all events in the workflow are valid 
        
        Args:
            raw_data_processing_I (list)
            
        Returns:
            bool: True if all events are valid, False otherwise
        """

        valid_events = [
            "load_raw_data",
            "load_features",
            "pick_features",
            "filter_features",
            "select_features",
            "validate_features",
            "quantify_features",
            "check_features",
            "plot_features",
            "store_features",
            "save_features",
            "annotate_used_features",
            "clear_feature_history"]
        valid = True
        for event in raw_data_processing_I:
            if event not in valid_events:
                print("Raw data processing event " + event + " is not valid.")
                valid = False
                
        return valid

    def getDefaultRawDataProcessingWorkflow(self, sample_type):
        """return the default workflow parameters for a given raw data
        
        Args:
            sample_type (str): the type of sample
            
        Returns:
            dict: dictionary of workflow_parameters"""

        default = []
        if sample_type == "Unknown":
            default = [
                "load_raw_data",
                "pick_features",
                "filter_features",
                "select_features",
                "quantify_features",
                "check_features"]
        elif sample_type == "Standard":
            default = [
                "load_raw_data",
                "pick_features",
                "filter_features",
                "select_features",
                "quantify_features",
                "check_features"]
        elif sample_type == "QC":
            default = [
                "load_raw_data",
                "pick_features",
                "filter_features",
                "select_features",
                "quantify_features",
                "check_features"]
        elif sample_type == "Blank":
            default = [
                "load_raw_data",
                "pick_features",
                "filter_features",
                "select_features",
                "quantify_features",
                "check_features"]
        elif sample_type == "Double Blank":
            default = [
                "load_raw_data",
                "pick_features",
                "filter_features",
                "select_features",
                "check_features"]
        elif sample_type == "Solvent":
            default = [
                "load_raw_data",
                "pick_features",
                "filter_features",
                "select_features",
                "check_features"]
        
        return default   

    def annotateUsedFeatures(
        self,
        rawDataHandler_IO,
        verbose_I=False
    ):
        """Annotate the most recent featureMap in the history with the
        filtered/selected features of the current featureMap
        and then replace the current featureMap with the annotated one
        
        Args:
            rawDataHandler_IO (RawDataHandler): raw data file class
                
        """

        # select features
        if verbose_I:
            print("Annotating used features")
        
        features_annotated = pyopenms.FeatureMap()
        for feature_copy in rawDataHandler_IO.getFeatureMapHistory()[-1]:    
            subordinates_annotated = []
            for subordinate_copy in feature_copy.getSubordinates():
                subordinate_copy.setMetaValue("used_".encode('utf-8'), "false".encode('utf-8'))
                subordinates_annotated.append(subordinate_copy)
            for feature_select in rawDataHandler_IO.getFeatureMap(): 
                if feature_select.getUniqueId() == feature_copy.getUniqueId():
                    for subordinate_copy in subordinates_annotated:
                        # for subordinate_select in feature_select.getSubordinates():
                        #     if subordinate_select.getMetaValue("native_id") == subordinate_copy.getMetaValue("native_id"):
                        #         subordinate_copy.setMetaValue("used_".encode('utf-8'), "true".encode('utf-8'))
                        subordinate_copy.setMetaValue("used_".encode('utf-8'), "true".encode('utf-8'))
                    break        
            feature_copy.setSubordinates(subordinates_annotated)
            features_annotated.push_back(feature_copy)

        rawDataHandler_IO.setFeatureMap(features_annotated)

    def saveCurrentFeatureMapToHistory(
        self,
        rawDataHandler_IO,
        verbose_I=False
    ):
        """Save the current featureMap to the history
        
        Args:
            rawDataHandler_IO (RawDataHandler): raw data file class
                
        """

        # select features
        if verbose_I:
            print("Saving features")
        
        features_annotated = pyopenms.FeatureMap()
        for feature_copy in rawDataHandler_IO.getFeatureMap():    
            subordinates_annotated = []
            for subordinate_copy in feature_copy.getSubordinates():
                subordinates_annotated.append(subordinate_copy)
            feature_copy.setSubordinates(subordinates_annotated)
            features_annotated.push_back(feature_copy)

        rawDataHandler_IO.featureMapHistory.append(features_annotated)