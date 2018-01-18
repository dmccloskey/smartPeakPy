# -*- coding: utf-8 -*-
from .SampleHandler import SampleHandler
from .SequenceGroupHandler import SequenceGroupHandler


class SequenceHandler():
    """A class to manage the mapping of metadata and FeatureMaps
        (i.e., multiple samples in a run batch/sequence)"""

    def __init__(self):
        """Sequence

        A sequence is a list of sample

        sequence (list): list of SampleHandlers
        index_to_sample (dict): index to sample_name
        index_to_sample (dict): sample_name to index
        sequence_groups (list): list of SequenceGroupHandlers

        """
        self.sequence = []
        self.index_to_sample = {}
        self.sample_to_index = {}
        self.sequence_groups = []

    def getSequence(self):
        """Return sequence"""
        return self.sequence

    def addSampleToSequence(
        self, meta_data_I, featureMap_I, 
        raw_data_processing_I=None, sequence_group_processing_I=None
    ):
        """add meta_data and featureMap to a sequence list

        Args:
            meta_data_I (dict): dictionary of meta data (e.g., sample_name)
            featureMap_I (FeatureMap): processed data in a FeatureMap
            raw_data_processing_I (dict): dictionary of sample processing steps
            sequence_group_processing_I (dict): dictionary of sequence processing steps for the
                sample

        Returns:
            dict: injection: dictionary of meta_data and FeatureMap
        """

        meta_data = self.parse_metaData(meta_data_I)
        
        if raw_data_processing_I is not None:
            raw_data_processing = self.parse_rawDataProcessing(
                raw_data_processing_I, meta_data["sample_type"])
        else:
            raw_data_processing = raw_data_processing_I

        if sequence_group_processing_I is not None:
            sequence_group_processing = self.parse_sequenceGroupProcessing(
                sequence_group_processing_I, meta_data["sample_type"])
        else:
            sequence_group_processing = sequence_group_processing_I

        sample = SampleHandler()
        sample.meta_data = meta_data
        sample.featureMap = featureMap_I
        sample.raw_data_processing = raw_data_processing
        sample.sequence_group_processing = sequence_group_processing

        self.sequence.append(sample)
        self.index_to_sample[len(self.sequence)-1] = meta_data["sample_name"]
        self.sample_to_index[meta_data["sample_name"]] = len(self.sequence)-1

    def getMetaValue(self, feature, subordinate, meta_value):
        """Returns the metaValue
        
        Args:
            feature (Feature): OpenMS::Feature corresponding to transition_group
            subordinate (Feature): OPENMS::Feature corresponding to transition

        Returns:
            float: datum: metaValue extraction from feature or subordinate
            
        """
        datum = None
        if meta_value == "RT":
            datum = feature.getRT()
        else:
            datum = feature.getMetaValue(meta_value)
            if datum is None:
                datum = subordinate.getMetaValue(meta_value)
        return datum

    def getRequiredHeaders(self):
        """Return required headers in a sequence file"""

        # # MultiQuant Example
        # required_headers = [
        #     "SampleName","SampleID",
        #     "Comments","AcqMethod",
        #     "ProcMethod","RackCode","PlateCode","VialPos","SmplInjVol",
        #     "DilutFact","WghtToVol","Type","RackPos","PlatePos",
        #     "SetName","OutputFile"
        #     ]

        # optional_headers = [
        #     "comments", "acquisition_method", "processing_method",
        #     "rack_code", "plate_code", "vial_position", "rack_position", 
        #     "plate_position",
        #     "injection_volume", "dilution_factor", "weight_to_volume",
        #     "set_name"]

        required_headers = [
            "sample_name", "sample_group_name", "sample_type", "filename",
            "sequence_group_name"
            ]

        return required_headers

    def parse_metaData(self, meta_data):
        """Parse a sequence file to ensure all headers are present
        
        Args:
            meta_data (dict): a dictionary of sample information

        Returns:
            dict: meta_data
        """

        sample_types = ["Unknown", "Standard", "QC", "Blank", "Double Blank", "Solvent"]
        sample_types_str = ",".join(sample_types)

        # check for required headers
        for header in self.getRequiredHeaders():
            if header not in meta_data:
                print(
                    'SequenceFile Error: required header in sequence list "' +
                    header + '" not found.')
                raise NameError("sequenceFile header")
                # meta_data[header] = None  # not needed
            
        # check for correctness of data
        if meta_data["sample_name"] is None:
            print(
                "SequenceFile Error: sample_name must be specified.")
            raise NameError("sample name")
        if meta_data["sample_group_name"] is None:
            print(
                "SequenceFile Error: sample_group_name must be specified.")
            raise NameError("sample group name")
        if meta_data["sequence_group_name"] is None:
            print(
                "SequenceFile Error: sequence_group_name must be specified.")
            raise NameError("sequence group name")
        if meta_data["filename"] is None:
            print(
                "SequenceFile Error: filename must be specified.")
            raise NameError("filename name")
        if meta_data["filename"] is None:
            print(
                "SequenceFile Error: filename must be specified.")
            raise NameError("filename name")

        if meta_data["sample_type"] is None or\
            meta_data["sample_type"] not in sample_types:
            print(
                "SequenceFile Error: sample_type for sample_name " +
                meta_data["sample_name"] + " is not correct.")
            print(
                "Supported samples types are the following: " +
                sample_types_str)
            raise NameError("sample type")

        # other checks...

        return meta_data

    def addFeatureMapToSequence(self, sample_name, featureMap):
        """add a featureMap to an existing sequence

        Args:
            sample_name (str): name of the sample (must be unique!)
            featureMap (FeatureMap): processed data in a FeatureMap

        Returns:
            dict: injection: dictionary of meta_data and FeatureMap
        """

        if sample_name not in self.sample_to_index.keys():
            print(
                "Sample name " + sample_name + " not found in sequence.")
            raise NameError("sample_name")
        else:
            self.sequence[self.sample_to_index[sample_name]].featureMap = featureMap

    def getDefaultRawDataProcessingWorkflow(self, sample_type):
        """return the default workflow parameters for a given raw data
        
        Args:
            sample_type (str): the type of sample
            
        Returns:
            dict: dictionary of workflow_parameters"""
    
        default = {
            "pick_peaks": True,
            "filter_peaks": True,
            "select_peaks": True,
            "validate_peaks": False,
            "quantify_peaks": False,
            "check_peaks": True,
            "plot_peaks": False}
        if sample_type == "Unknown":
            default["quantify_peaks"] = True
        elif sample_type == "Standard":
            default["quantify_peaks"] = True
        elif sample_type == "QC":
            default["quantify_peaks"] = True
        elif sample_type == "Blank":
            default["quantify_peaks"] = True
        elif sample_type == "Double Blank":
            pass
        elif sample_type == "Solvent":
            pass
        
        return default

    def parse_rawDataProcessing(self, raw_data_processing, sample_type):
        """parse the sample processing steps

        Args:
            raw_data_processing (dict): dictionary of sample processing steps
            sample_type (str): type of the sample

        """

        required_headers = [
            "pick_peaks",
            "filter_peaks",
            "select_peaks",
            "validate_peaks",
            "quantify_peaks",
            "check_peaks"]

        # ensure supplied values are of the right type
        for k, v in raw_data_processing.items():
            if k in required_headers and ~isinstance(v, bool):
                print("Wrong value provided for key " + k + " in raw_data_processing.")
                raise NameError("raw_data_processing")

        # ensure all headers are present
        for k in required_headers:
            if k not in raw_data_processing.keys():
                raw_data_processing[k] = self.getDefaultRawDataProcessingWorkflow(
                    sample_type)[k]            

    def getDefaultSequenceGroupProcessingWorkflow(self, sample_type):
        """return the default workflow parameters for a given sequence
        
        Args:
            sample_type (str): the type of sample
            
        Returns:
            dict: dictionary of workflow_parameters"""
    
        default = {
            "calculate_calibration": False,
            "calculate_carryover": False,
            "calculate_variability": False}
        if sample_type == "Unknown":
            pass
        elif sample_type == "Standard":
            default["calculate_calibration"] = True
        elif sample_type == "QC":
            default["calculate_variability"] = True
        elif sample_type == "Blank":
            pass
        elif sample_type == "Double Blank":
            pass
        elif sample_type == "Solvent":
            default["calculate_carryover"] = True
        
        return default

    def parse_sequenceGroupProcessing(self, sequence_group_processing, sample_type):
        """parse the sequence processing steps

        Args:
            sequence_group_processing (dict): dictionary of sequence processing steps for the sample
            sample_type (str): type of the sample

        """

        required_headers = [
            "calculate_calibration",
            "calculate_carryover",
            "calculate_variability"]

        # ensure supplied values are of the right type
        for k, v in sequence_group_processing.items():
            if k in required_headers and ~isinstance(v, bool):
                print("Wrong value provided for key " + k + " in sequence_group_processing.")
                raise NameError("sequence_group_processing")

        # ensure all headers are present
        for k in required_headers:
            if k not in sequence_group_processing.keys():
                sequence_group_processing[k] = self.getDefaultSequenceGroupProcessingWorkflow(
                    sample_type)[k]