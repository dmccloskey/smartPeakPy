# -*- coding: utf-8 -*-


class SequenceSegmentHandler():

    def __init__(self):
        """Sequence Group
        """

        self.sequence_segment_name = None
        self.sample_indices = None
        self.standards_concentrations = None
        self.quantitation_methods = None

    def clear_data(self):
        self.sequence_segment_name = None
        self.sample_indices = None
        self.standards_concentrations = None
        self.quantitation_methods = None

    # def getDefaultSampleOrder(self, sample_type):
    #     """Return the default order for each sample in a group
        
    #     Args:
    #         sample_type (str): type of sample

    #     Returns:
    #         int: order
            
    #     """

    #     order = -1
    #     if sample_type == "Standard":
    #         order = 0
    #     elif sample_type == "Unknown":
    #         order = 1 
    #     elif sample_type == "QC":
    #         order = 2 
    #     elif sample_type == "Blank":
    #         order = 3
    #     elif sample_type == "Double Blank":
    #         order = 3
    #     elif sample_type == "Solvent":
    #         pass

    #     return order