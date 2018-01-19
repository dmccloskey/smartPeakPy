# -*- coding: utf-8 -*-
try:
    import pyopenms
except ImportError as e:
    print(e)


class SequenceSegmentProcessor():

    def getSampleIndicesBySampleType(
        self,
        sequenceSegmentHandler_I,
        sequenceHandler_I,
        sample_type
    ):
        """Return all samples in that belong to a given sample type
        
        Args:
            sequenceSegmentHandler_I (SequenceSegmentHandler)
            sequenceHandler_I (SequenceHandler)
            sample_type (str)
            
        """

        sample_indices = []
        for index in sequenceSegmentHandler_I.sample_indices:
            if sequenceHandler_I.sequence[index].meta_data["sample_type"] == sample_type:
                sample_indices.append(index)
        return sample_indices

    def optimizeCalibrationCurves(self, sequenceSegmentHandler_IO, sequenceHandler_I):
        """Optimize the calibration curve for all components
        
        Args:
            sequenceSegmentHandler_I (SequenceSegmentHandler)
            sequenceHandler_I (SequenceHandler)
            
        """

        # get all standards
        standards_indices = self.getSampleIndicesBySampleType(
            sequenceSegmentHandler_IO, sequenceHandler_I,
            "Standard"
        )

        # check if there are any standards to calculate the calibrators from
        if not standards_indices:
            return

        standards_featureMaps = [
            sequenceHandler_I.sequence[index].featureMap for index in standards_indices]

        # map standards to features
        components_to_concentrations = {}       
        absoluteQuantitationStandards = pyopenms.AbsoluteQuantitationStandards()
        absoluteQuantitationStandards.mapConcentrationsToComponents(
            sequenceSegmentHandler_IO.standards_concentrations,
            standards_featureMaps,
            components_to_concentrations
        )        

        # find the optimal calibration curve for each component
        absoluteQuantitation = pyopenms.AbsoluteQuantitation()
        absoluteQuantitation.optimizeCalibrationCurves(components_to_concentrations)        

        sequenceSegmentHandler_IO.quanitation_methods = absoluteQuantitation.getQuantMethods()  # TODO!!!

    def processSequenceSegment(
        self, sequenceSegmentHandler_IO, 
        sequence_group_processing_methods
    ):
        """Apply processing methods to a raw data handler
        
        Args:
            sequenceSegmentHandler_IO (SequenceSegmentHandler)
            sequence_group_processing_methods (dict): map of sequence group
                processing methods
            
        """
        pass

    def getDefaultSequenceSegmentProcessingWorkflow(self, sample_type):
        """return the default workflow events for a given sequence
        
        Args:
            sample_type (str): the type of sample
            
        Returns:
            list: list of sequence group processing events"""
    
        default = []
        if sample_type == "Unknown":
            pass
        elif sample_type == "Standard":
            default = ["calculate_calibration"]
        elif sample_type == "QC":
            default = ["calculate_variability"]
        elif sample_type == "Blank":
            pass
        elif sample_type == "Double Blank":
            pass
        elif sample_type == "Solvent":
            default = ["calculate_carryover"]
        
        return default

    def checkSequenceSegmentProcessing(self, sequence_group_processing):
        """check the sequence processing steps

        Args:
            sequence_group_processing (list): list of sequence group processing events
            
        Returns:
            bool: True if all events are valid, False otherwise
        """

        valid_events = [
            "calculate_calibration",
            "calculate_carryover",
            "calculate_variability"]

        valid = True
        for event in sequence_group_processing:
            if event not in valid_events:
                print("Sequence group processing event " + event + " is not valid.")
                valid = False
                
        return valid