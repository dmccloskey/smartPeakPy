# -*- coding: utf-8 -*-
from smartPeak.io.SequenceWriter import SequenceWriter
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS
from . import data_dir
from smartPeak.core.RawDataHandler import RawDataHandler
from smartPeak.core.SequenceHandler import SequenceHandler
import copy


class TestSequenceWriter():

    def test_makeDataMatrixFromMetaValue(self):  
        seqhandler = SequenceHandler()
        seqWriter = SequenceWriter()
        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()

        # make the data
        sample_names = [
            "170808_Jonathan_yeast_Sacc1_1x",
            "170808_Jonathan_yeast_Sacc2_1x",
            "170808_Jonathan_yeast_Sacc3_1x",
            "170808_Jonathan_yeast_Yarr1_1x",
            "170808_Jonathan_yeast_Yarr2_1x",
            "170808_Jonathan_yeast_Yarr3_1x"]
        meta_data_required = {h: None for h in seqhandler.getRequiredHeaders()}        
        for sample in sample_names:
            meta_data1 = copy.copy(meta_data_required)
            meta_data1.update({
                "sample_name": sample,
                "filename": sample + ".mzML",
                "sample_type": "Unknown",
                "sample_group_name": "sample_group",
                "sequence_group_name": "sequence_group"
            })
            seqhandler.addSampleToSequence(meta_data1, None)
        for sequence in seqhandler.sequence:
            # dynamically make the filenames
            featureXML_o = '''%s/quantitation/%s.featureXML''' % (
                data_dir, sequence.meta_data["sample_name"])
            fileReaderOpenMS.load_featureMap(
                rawDataHandler, {'featureXML_i': featureXML_o})

            # record features
            seqhandler.addFeatureMapToSequence(
                sequence.meta_data["sample_name"], rawDataHandler.featureMap)
            # manual clear data for the next iteration
            rawDataHandler.clear_data()

        # Test:
        columns, rows, data = seqWriter.makeDataMatrixFromMetaValue(
            seqhandler,
            meta_values=["calculated_concentration"], sample_types=["Unknown"])
        
        assert(len(columns) == 6)
        assert(columns[0] == '170808_Jonathan_yeast_Sacc1_1x')
        assert(rows[0][0] == 'accoa')
        assert(data[0, 0] == 1.2847857900212101)
        assert(data[len(rows)-1, len(columns)-1] == 1.57220084379097)