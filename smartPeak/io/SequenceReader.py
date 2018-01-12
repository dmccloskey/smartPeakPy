# -*- coding: utf-8 -*-
from smartPeak.io.FileReader import FileReader


class SequenceReader():
    """A class to write SequenceHandlers"""

    def read_sequenceFile(self, sequence_IO, filename, delimiter=','):
        """Import a sequence file
        
        Args:
            sequence_IO (SequenceHandler)
            
        """

        # read in the data
        fileReader = FileReader()
        fileReader.read_csv(filename, delimiter)
        self.parse_sequenceFile(sequence_IO, fileReader.getData())
        fileReader.clear_data()

    def parse_sequenceFile(self, sequence_IO, sequence_file):
        """Parse a sequence file to ensure all headers are present
        
        Args:
            sequence_IO (SequenceHandler)
            sequenceFile (list): list of dictionaries of sequence information
        """

        for seq in sequence_file:
            sequence_IO.addSampleToSequence(seq, None)

