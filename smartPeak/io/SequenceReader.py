# -*- coding: utf-8 -*-
from smartPeak.io.FileReader import FileReader


class SequenceReader():
    """A class to write SequenceHandlers"""

    def read_sequenceFile(self, sequenceHandler_IO, filename, delimiter=','):
        """Import a sequence file

        the sample metadata is read in from a .csv file.  The raw_data_processing and
        sequencing_processing steps are autogenerated based on the sample type.
        The featureMap is left as null.
        
        Args:
            sequenceHandler_IO (SequenceHandler)
            
        """

        # read in the data
        if filename is not None:
            fileReader = FileReader()
            fileReader.read_csv(filename, delimiter)
            self.parse_sequenceFile(sequenceHandler_IO, fileReader.getData())
            fileReader.clear_data()

    def parse_sequenceFile(self, sequenceHandler_IO, sequence_file):
        """Parse a sequence file to ensure all headers are present
        
        Args:
            sequenceHandler_IO (SequenceHandler)
            sequence_file (list): list of dictionaries of sequence information
        """

        for seq in sequence_file:
            sequenceHandler_IO.addSampleToSequence(seq, None)

