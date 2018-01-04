# -*- coding: utf-8 -*-
from smartPeak.__main__ import __main__
from . import example_dir
import os
# import filecmp
from smartPeak.core.SampleHandler import SampleHandler
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS


class testMain():

    def test_main_LCMS_MRM(self):
        """Test LCMS MRM example"""
        m = __main__()

        m.main(
            filename_sequence=example_dir + 'LCMS_MRM/sequence.csv',
            filename_params=example_dir + 'LCMS_MRM/parameters.csv',
            delimiter=',',
            )
        assert(~os.path.isfile(example_dir + 'LCMS_MRM/mzML/skippedSamples.csv'))

        sampleHandler = SampleHandler()
        fileReaderOpenMS = FileReaderOpenMS()
        fileReaderOpenMS.load_featureMap(
            sampleHandler, {
                'featureXML_i': 
                example_dir + 
                'LCMS_MRM/quantitation/170808_Jonathan_yeast_Sacc1_1x.featureXML'})
        fm1 = sampleHandler.featureMap
        fileReaderOpenMS.load_featureMap({
            'featureXML_i': 
            example_dir + 
            'LCMS_MRM/quantitation/170808_Jonathan_yeast_Sacc1_1x_test.featureXML'})
        fm2 = sampleHandler.featureMap
        assert(
            fm1[50].getSubordinates()[0].getMetaValue("native_id") == 
            fm2[50].getSubordinates()[0].getMetaValue("native_id"))
        assert(
            fm1[50].getSubordinates()[0].getMetaValue("peak_apex_int") == 
            fm2[50].getSubordinates()[0].getMetaValue("peak_apex_int"))
        assert(
            fm1[50].getSubordinates()[0].getRT() == 
            fm2[50].getSubordinates()[0].getRT())

        # # TODO: why is this not working?
        # assert(filecmp.cmp(
        #     example_dir + 'LCMS_MRM/quantitation/170808_Jonathan_yeast_Sacc1_1x.featureXML',
        #     example_dir + 'LCMS_MRM/quantitation/170808_Jonathan_yeast_Sacc1_1x_test.featureXML',
        #     shallow=False
        #     ))
        # assert(filecmp.cmp(
        #     example_dir + 'LCMS_MRM/features/170808_Jonathan_yeast_Sacc1_1x.featureXML',
        #     example_dir + 'LCMS_MRM/features/170808_Jonathan_yeast_Sacc1_1x_test.featureXML',
        #     shallow=False
        #     ))
        # assert(filecmp.cmp(
        #     example_dir + 'LCMS_MRM/features_tmp/170808_Jonathan_yeast_Sacc1_1x.featureXML',
        #     example_dir + 'LCMS_MRM/features_tmp/170808_Jonathan_yeast_Sacc1_1x_test.featureXML',
        #     shallow=False
        #     ))
        # assert(filecmp.cmp(
        #     example_dir + 'LCMS_MRM/SequenceSummary.csv',
        #     example_dir + 'LCMS_MRM/SequenceSummary_test.csv',
        #     shallow=False
        #     ))

    def test_main_GCMS_SIM(self):
        """Test GCMS SIM example"""
        m = __main__()

        m.main(
            filename_sequence=example_dir + 'GCMS_SIM/sequence.csv',
            filename_params=example_dir + 'GCMS_SIM/parameters.csv',
            delimiter=',',
            )
        assert(~os.path.isfile(example_dir + 'GCMS_SIM/mzML/skippedSamples.csv'))

        sampleHandler = SampleHandler()
        fileReaderOpenMS = FileReaderOpenMS()

        fileReaderOpenMS.load_featureMap(sampleHandler, {
                'featureXML_i': 
                example_dir + 
                'GCMS_SIM/features/GCMS_SIM.featureXML'})
        fm1 = sampleHandler.featureMap
        fileReaderOpenMS.load_featureMap(SampleHandler, {
            'featureXML_i': 
            example_dir + 
            'GCMS_SIM/features/GCMS_SIM_test.featureXML'})
        fm2 = sampleHandler.featureMap
        assert(
            fm1[15].getSubordinates()[0].getMetaValue("native_id") == 
            fm2[15].getSubordinates()[0].getMetaValue("native_id"))
        assert(
            fm1[15].getSubordinates()[0].getMetaValue("peak_apex_int") == 
            fm2[15].getSubordinates()[0].getMetaValue("peak_apex_int"))
        assert(
            fm1[15].getSubordinates()[0].getRT() == 
            fm2[15].getSubordinates()[0].getRT())
        
        # # TODO: why is this not working?
        # assert(filecmp.cmp(
        #     example_dir + 'GCMS_SIM/features/GCMS_SIM.featureXML',
        #     example_dir + 'GCMS_SIM/features/GCMS_SIM_test.featureXML',
        #     shallow=False
        #     ))
        # assert(filecmp.cmp(
        #     example_dir + 'GCMS_SIM/features_tmp/GCMS_SIM.featureXML',
        #     example_dir + 'GCMS_SIM/features_tmp/GCMS_SIM_test.featureXML',
        #     shallow=False
        #     ))
        # assert(filecmp.cmp(
        #     example_dir + 'GCMS_SIM/SequenceSummary.csv',
        #     example_dir + 'GCMS_SIM/SequenceSummary_test.csv',
        #     shallow=False
        #     ))