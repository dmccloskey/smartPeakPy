# -*- coding: utf-8 -*-
try:
    import pyopenms
except ImportError as e:
    print(e)


class SequenceGroupProcessor():

    def getSampleIndicesBySampleType(
        self,
        sequenceGroupHandler_I,
        sequenceHandler_I,
        sample_type
    ):
        """Return all samples in that belong to a given sample type
        
        Args:
            sequenceGroupHandler_I (SequenceGroupHandler)
            sequenceHandler_I (SequenceHandler)
            sequence_group_name (str)
            sample_type (str)
            
        """

        sample_indices = []
        for index in sequenceGroupHandler_I.sample_indices:
            if sequenceHandler_I.sequence[index].meta_value["sample_type"] == sample_type:
                sample_indices.append(index)
        return sample_indices

    def optimizeCalibrationCurves(self, sequenceGroupHandler_IO, sequenceHandler_I):
        """ """

        # get all standards
        standards_indices = self.getSampleIndicesBySampleType(
            sequenceGroupHandler_IO, sequenceHandler_I,
            "Standard"
        )
        standards_featureMaps = [sequenceHandler_I.sequence[index].featureMap for index in standards_indices]

        # map standards to features
        components_to_concentrations = {}       
        absoluteQuantitationStandards = pyopenms.AbsoluteQuantitationStandards()
        absoluteQuantitationStandards.mapConcentrationsToComponents(
            sequenceGroupHandler_IO.standards_concentrations,
            standards_featureMaps,
            components_to_concentrations
        )        

        # find the optimal calibration curve for each component
        absoluteQuantitation = pyopenms.AbsoluteQuantitation()
        absoluteQuantitation.optimizeCalibrationCurves(components_to_concentrations)        

        sequenceGroupHandler_IO.quanitation_methods = absoluteQuantitation.getQuantMethods()  # TODO!!!