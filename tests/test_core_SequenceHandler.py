# -*- coding: utf-8 -*-
from smartPeak.io.smartPeak_i import smartPeak_i
from . import data_dir
from smartPeak.core.SequenceHandler import SequenceHandler
import copy
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class TestSequenceHandler():

    def test_addSampleToSequence(self):
        seqhandler = SequenceHandler()

        # test data
        meta_data_required = {h: None for h in seqhandler.getRequiredHeaders()}
        meta_data1 = copy.copy(meta_data_required)
        meta_data1.update({
            'filename': 'file1', 'sample_name': 'sample1', 'sample_type': 'Unknown'})
        featuremap1 = None
        
        meta_data2 = copy.copy(meta_data_required)
        meta_data2.update({
            'filename': 'file2', 'sample_name': 'sample2', 'sample_type': 'Unknown'})
        featuremap2 = None
        
        meta_data3 = copy.copy(meta_data_required)
        meta_data3.update({
            'filename': 'file3', 'sample_name': 'sample3', 'sample_type': 'Unknown'})
        featuremap3 = None

        # add the injections to the sequence
        seqhandler.addSampleToSequence(meta_data1, featuremap1)
        seqhandler.addSampleToSequence(meta_data2, featuremap2)
        seqhandler.addSampleToSequence(meta_data3, featuremap3)

        assert(len(seqhandler.sequence) == 3)
        assert(seqhandler.index_to_sample[1] == 'sample2')
        assert(seqhandler.sample_to_index['sample2'] == 1)

    def test_getMetaValue(self):  
        seqhandler = SequenceHandler()

        # make the test data
        feature = pyopenms.Feature()
        feature.setRT(16.0)
        subordinate = pyopenms.Feature()
        subordinate.setMetaValue("calculated_concentration", 10.0)

        result = seqhandler.getMetaValue(feature, subordinate, "RT")
        assert(result == 16.0)
        result = seqhandler.getMetaValue(feature, subordinate, "calculated_concentration")
        assert(result == 10.0)

    def test_makeDataMatrixFromMetaValue(self):  
        seqhandler = SequenceHandler()
        from smartPeak.core.smartPeak_openSWATH import smartPeak_openSWATH
        openSWATH = smartPeak_openSWATH()

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
                "sample_type": "Unknown"
            })
            seqhandler.addSampleToSequence(meta_data1, None)
        for sequence in seqhandler.sequence:
            try:
                # dynamically make the filenames
                featureXML_o = '''%s/quantitation/%s.featureXML''' % (
                    data_dir, sequence["meta_data"]["sample_name"]) 
                feature_csv_o = '''%s/quantitation/%s.csv''' % (
                    data_dir, sequence["meta_data"]["sample_name"])
                openSWATH.load_featureMap({'featureXML_i': featureXML_o})

                # record features
                seqhandler.addFeatureMapToSequence(
                    sequence["meta_data"]["sample_name"], openSWATH.featureMap)
            except Exception as e:
                print(e)
            # manual clear data for the next iteration
            openSWATH.clear_data()

        # Test:
        columns, rows, data = seqhandler.makeDataMatrixFromMetaValue(
            meta_values=["calculated_concentration"], sample_types=["Unknown"])
        
        assert(len(columns) == 6)
        assert(columns[0] == '170808_Jonathan_yeast_Sacc1_1x')
        assert(rows[0][0] == 'accoa')
        assert(data[0, 0] == 1.2847857900212101)
        assert(data[len(rows)-1, len(columns)-1] == 1.57220084379097)

    def test_parse_metaData(self):  
        seqhandler = SequenceHandler()

        meta_data = {}
        try:
            seqhandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data = {
            "sample_name": None, "sample_type": None,
            "comments": None, "acquisition_method": None, "processing_method": None,
            "rack_code": None, "plate_code": None, 
            "vial_position": None, "rack_position": None, 
            "plate_position": None,
            "injection_volume": None, "dilution_factor": None, 
            "weight_to_volume": None,
            "set_name": None, "filename": ""}
        try:
            seqhandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data["sample_name"] = ""
        meta_data["filename"] = None
        meta_data["sample_type"] = ""
        try:
            seqhandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data["filename"] = ""
        try:
            seqhandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data["sample_type"] = "Unknown"
        assert(seqhandler.parse_metaData(meta_data)["sample_type"] == "Unknown")

    def test_addFeatureMapToSequence(self):
        seqhandler = SequenceHandler()

        # test data
        meta_data_required = {h: None for h in seqhandler.getRequiredHeaders()}
        meta_data1 = copy.copy(meta_data_required)
        meta_data1.update({
            'filename': 'file1', 'sample_name': 'sample1', 'sample_type': 'Unknown'})
        featuremap1 = None
        
        meta_data2 = copy.copy(meta_data_required)
        meta_data2.update({
            'filename': 'file2', 'sample_name': 'sample2', 'sample_type': 'Unknown'})
        featuremap2 = None
        
        meta_data3 = copy.copy(meta_data_required)
        meta_data3.update({
            'filename': 'file3', 'sample_name': 'sample3', 'sample_type': 'Unknown'})
        featuremap3 = None

        # add the injections to the sequence
        seqhandler.addSampleToSequence(meta_data1, featuremap1)
        seqhandler.addSampleToSequence(meta_data2, featuremap2)
        seqhandler.addSampleToSequence(meta_data3, featuremap3)
        seqhandler.addFeatureMapToSequence("sample2", "DummyFeatureMap")

        injection = seqhandler.sequence[
            seqhandler.sample_to_index['sample2']]
        assert(injection["featureMap"] == "DummyFeatureMap")

    def test_read_sequenceFile(self):
        """No test"""
        pass

    def test_parse_sequenceFile(self):
        """No test"""
        pass


        