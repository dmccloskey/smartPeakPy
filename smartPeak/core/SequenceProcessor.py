# -*- coding: utf-8 -*-


class SequenceProcessor():

    def groupSamplesInSequence(self, sequenceGroupHandler_IO, sequenceHandler_I):
        """group samples in a sequence"""

        groups_order = {}
        groups_dict = {}
        for cnt, sequence in enumerate(sequenceHandler_I):
            if sequence.meta_value["sequence_group_name"] not in groups_dict.keys():
                groups_dict[sequence.meta_value["sequence_group_name"]] = []
            groups_dict[sequence.meta_value["sequence_group_name"]].append(cnt)

            if sequence.meta_value["sequence_group_name"] not in groups_order.keys():
                groups_order[sequence.meta_value["sequence_group_name"]] = 0
            else:
                groups_order[sequence.meta_value["sequence_group_name"]] += 1
        
        groups = []
        for k, v in groups_dict.items():
            group = {}
            group[k] = v
            groups.append(group)

        sequenceGroupHandler_IO.sequence_groups_order = groups_order
        sequenceGroupHandler_IO.sequence_groups = groups

    def getSampleIndicesBySampleTypeAndSequenceGroupName(
        self,
        sequenceGroupHandler_I,
        sequenceHandler_I,
        sequence_group_name,
        sample_type
    ):
        """Return all samples in a group that belong to a given sample type
        
        Args:
            sequenceGroupHandler_I (SequenceGroupHandler)
            sequenceHandler_I (SequenceHandler)
            sequence_group_name (str)
            sample_type (str)
            
        """

        sample_indices = []
        for index in sequenceGroupHandler_I.sequence_groups[
            sequenceGroupHandler_I.sequence_groups_order[sequence_group_name]]:
            if sequenceHandler_I.sequence[index].meta_valu["sample_type"] == sample_type:
                sample_indices.append(index)
        return sample_indices

    def optimizeCalibrationCurves(self):
        pass

    def processSequence(self):
        """process a sequence of samples"""

        pass