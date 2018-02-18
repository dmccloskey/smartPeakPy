# -*- coding: utf-8 -*-
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS
from smartPeak.io.FileWriterOpenMS import FileWriterOpenMS
from smartPeak.core.Utilities import Utilities
from smartPeak.ui.SequenceSegmentPlotter import SequenceSegmentPlotter
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

    def optimizeCalibrationCurves(
        self,
        sequenceSegmentHandler_IO,
        sequenceHandler_I,
        AbsoluteQuantitation_params_I={},
        verbose_I=False
    ):
        """Optimize the calibration curve for all components
        
        Args:
            sequenceSegmentHandler_I (SequenceSegmentHandler)
            sequenceHandler_I (SequenceHandler)
            
        """
        if verbose_I:
            print("optimizing calibrators")

        # get all standards
        standards_indices = self.getSampleIndicesBySampleType(
            sequenceSegmentHandler_IO, sequenceHandler_I,
            "Standard"
        )

        # check if there are any standards to calculate the calibrators from
        if not standards_indices:
            return

        standards_featureMaps = [
            sequenceHandler_I.sequence[index].getRawData().getFeatureMap() 
            for index in standards_indices]

        # add in the method parameters
        if AbsoluteQuantitation_params_I and AbsoluteQuantitation_params_I is not None:
            utilities = Utilities()
            absoluteQuantitation = pyopenms.AbsoluteQuantitation()
            parameters = absoluteQuantitation.getParameters()
            parameters = utilities.updateParameters(
                parameters,
                AbsoluteQuantitation_params_I,
                )
            absoluteQuantitation.setParameters(parameters) 

            absoluteQuantitation.setQuantMethods(
                sequenceSegmentHandler_IO.getQuantitationMethods())

            # use the python wrapper C++ methods to optimize each calibration curve
            components_to_concentrations = {}
            for row in sequenceSegmentHandler_IO.getQuantitationMethods():
                # map standards to features
                absoluteQuantitationStandards = pyopenms.AbsoluteQuantitationStandards()
                feature_concentrations = []
                absoluteQuantitationStandards.getComponentFeatureConcentrations(
                    sequenceSegmentHandler_IO.standards_concentrations,
                    standards_featureMaps,
                    row.getComponentName(),
                    feature_concentrations
                )

                # remove features with an actual concentration of 0.0 or less
                feature_concentrations_pruned = []
                for feature in feature_concentrations:
                    if feature.actual_concentration > 0.0:
                        feature_concentrations_pruned.append(feature)

                # remove components without any points
                if len(feature_concentrations_pruned) == 0:
                    continue

                # find the optimial calibration curve for each component
                absoluteQuantitation.optimizeSingleCalibrationCurve(
                    row.getComponentName(), feature_concentrations_pruned)

                components_to_concentrations.update({
                        row.getComponentName(): feature_concentrations_pruned})

            # store results
            sequenceSegmentHandler_IO.setComponentsToConcentrations(
                components_to_concentrations
            )
            sequenceSegmentHandler_IO.setQuantitationMethods(
                absoluteQuantitation.getQuantMethods()) 

    def calculateQCVariance(
        self,
        sequenceSegmentHandler_IO,
        sequenceHandler_I,
        _params_I={},
        verbose_I=False
    ):
        """Calculate the variance within the calibrators
        
        Args:
            sequenceSegmentHandler_I (SequenceSegmentHandler)
            sequenceHandler_I (SequenceHandler)
            
        """
        if verbose_I:
            print("calculating QCs")

        # get all QCs
        QC_indices = self.getSampleIndicesBySampleType(
            sequenceSegmentHandler_IO, sequenceHandler_I,
            "QC"
        )

        # check if there are any QCs to calculate the variance from
        if not QC_indices:
            return

        QC_featureMaps = [
            sequenceHandler_I.sequence[index].getRawData().getFeatureMap() 
            for index in QC_indices]

    def calculateBlanks(
        self,
        sequenceSegmentHandler_IO,
        sequenceHandler_I,
        _params_I={},
        verbose_I=False
    ):
        """Find background interference in the blanks
        
        Args:
            sequenceSegmentHandler_I (SequenceSegmentHandler)
            sequenceHandler_I (SequenceHandler)
            
        """
        if verbose_I:
            print("calculating Blanks")

        # get all Blanks
        Blank_indices = self.getSampleIndicesBySampleType(
            sequenceSegmentHandler_IO, sequenceHandler_I,
            "Blank"
        )

        # check if there are any Blanks to find background in
        if not Blank_indices:
            return

        Blank_featureMaps = [
            sequenceHandler_I.sequence[index].getRawData().getFeatureMap() 
            for index in Blank_indices]

    def plotCalibrators(
        self,     
        sequenceSegmentHandler_I,   
        calibrators_pdf_o,
        SequenceSegmentPlotter_params_I={},
        verbose_I=False
    ):
        """Export plots of peaks with features annotated

        Args:
            sequenceSegmentHandler_I (SequenceSegmentHandler): 
            calibrators_pdf_o (str): filename

        """
        if verbose_I:
            print("Plotting calibrators")

        # export diagnostic plots
        if SequenceSegmentPlotter_params_I and calibrators_pdf_o is not None:
            sequenceSegmentPlotter = SequenceSegmentPlotter()
            sequenceSegmentPlotter.setParameters(SequenceSegmentPlotter_params_I)
            sequenceSegmentPlotter.plotCalibrationPoints(
                filename_I=calibrators_pdf_o,
                sequenceSegmentHandler_I=sequenceSegmentHandler_I
            )

    def processSequenceSegment(
        self, sequenceSegmentHandler_IO,
        sequenceHandler_I,
        sequence_segment_processing_event,
        parameters,
        filenames={},
        verbose_I=False
    ):
        """Apply processing methods to a raw data handler
        
        Args:
            sequenceSegmentHandler_IO (SequenceSegmentHandler)
            sequence_segment_processing_methods (str): string representing a
                sequence group processing methods
            
        """
        fileReaderOpenMS = FileReaderOpenMS()
        fileWriterOpenMS = FileWriterOpenMS()

        try:
            if sequence_segment_processing_event == "calculate_calibration":
                # optimize the calibrators
                self.optimizeCalibrationCurves(
                    sequenceSegmentHandler_IO, sequenceHandler_I,
                    AbsoluteQuantitation_params_I=parameters["AbsoluteQuantitation"],
                    verbose_I=verbose_I
                )
                # update each sample in the sequence segment with the
                # updated quantitationMethods
                for index in sequenceSegmentHandler_IO.getSampleIndices(): 
                    sequenceHandler_I.getSequence()[
                        index].getRawData().setQuantitationMethods(
                            sequenceSegmentHandler_IO.getQuantitationMethods())
            elif sequence_segment_processing_event == "store_quantitation_methods":
                fileWriterOpenMS.store_quantitationMethods(
                    sequenceSegmentHandler_IO,
                    filenames["quantitationMethods_csv_o"],
                    verbose_I=verbose_I)
            elif sequence_segment_processing_event == "load_quantitation_methods":
                fileReaderOpenMS.load_quantitationMethods(
                    sequenceSegmentHandler_IO,
                    filenames["quantitationMethods_csv_i"],
                    verbose_I=verbose_I)
            # elif sequence_segment_processing_event == "store_components_to_concentrations":
            #     pass
            elif sequence_segment_processing_event == "plot_calibrators":
                self.plotCalibrators(
                    sequenceSegmentHandler_IO,  
                    filenames["calibrators_pdf_o"],
                    SequenceSegmentPlotter_params_I=parameters['SequenceSegmentPlotter'],
                    verbose_I=verbose_I
                )
            else:                
                print(
                    "Sequence group processing event " +
                    sequence_segment_processing_event +
                    " was not recognized.")
        except Exception as e:
            print(e)

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

    def checkSequenceSegmentProcessing(self, sequence_segment_processing):
        """check the sequence processing steps

        Args:
            sequence_segment_processing (list): list of sequence group processing events
            
        Returns:
            bool: True if all events are valid, False otherwise
        """

        valid_events = [
            "calculate_calibration",
            "calculate_carryover",
            "calculate_variability",
            "store_quantitation_methods",
            "load_quantitation_methods",
            "store_components_to_concentrations",
            "plot_calibrators"
            ]

        valid = True
        for event in sequence_segment_processing:
            if event not in valid_events:
                print("Sequence group processing event " + event + " is not valid.")
                valid = False
                
        return valid