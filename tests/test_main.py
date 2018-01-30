# -*- coding: utf-8 -*-
from smartPeak.__main__ import __main__
from . import example_dir
import os
# import filecmp
from smartPeak.core.RawDataHandler import RawDataHandler
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS


class testMain():

    def test_main_LCMS_MRM_Unknown(self):
        """Test LCMS MRM example with Unknown sample types"""
        m = __main__()

        # m.main(
        #     filename_sequence=example_dir + 'LCMS_MRM/sequence.csv',
        #     filename_params=example_dir + 'LCMS_MRM/parameters.csv',
        #     delimiter=',',
        #     )
        # assert(~os.path.isfile(example_dir + 'LCMS_MRM/mzML/skippedSamples.csv'))
        
        m.main2(
            dir_I=example_dir + 'LCMS_MRM_Unknowns',
            delimiter=',',
            )

        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'LCMS_MRM/features/170808_Jonathan_yeast_Sacc1_1x.featureXML')
        fm1 = rawDataHandler.featureMap
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'LCMS_MRM/features/170808_Jonathan_yeast_Sacc1_1x_test.featureXML')
        fm2 = rawDataHandler.featureMap
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
        #     example_dir + 'LCMS_MRM/features/170808_Jonathan_yeast_Sacc1_1x.featureXML',
        #     example_dir + 'LCMS_MRM/features/170808_Jonathan_yeast_Sacc1_1x_test.featureXML',
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

        # m.main(
        #     filename_sequence=example_dir + 'GCMS_SIM/sequence.csv',
        #     filename_params=example_dir + 'GCMS_SIM/parameters.csv',
        #     delimiter=',',
        #     )
        # assert(~os.path.isfile(example_dir + 'GCMS_SIM/mzML/skippedSamples.csv'))

        m.main2(
            dir_I=example_dir + 'GCMS_SIM',
            delimiter=',',
            )

        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()

        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'GCMS_SIM/features/GCMS_SIM.featureXML')
        fm1 = rawDataHandler.featureMap
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'GCMS_SIM/features/GCMS_SIM_test.featureXML')
        fm2 = rawDataHandler.featureMap
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
        #     example_dir + 'GCMS_SIM/SequenceSummary.csv',
        #     example_dir + 'GCMS_SIM/SequenceSummary_test.csv',
        #     shallow=False
        #     ))

    def test_main_HPLC_UV(self):
        """Test HPLC UV example"""
        m = __main__()
        
        m.main2(
            dir_I=example_dir + 'HPLC_UV',
            delimiter=',',
            )

        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'HPLC_UV/features/20171013_HMP_C61_ISO_P1_GA1_UV_VIS_2.featureXML')
        fm1 = rawDataHandler.featureMap
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'HPLC_UV/features/20171013_HMP_C61_ISO_P1_GA1_UV_VIS_2_test.featureXML')
        fm2 = rawDataHandler.featureMap
        assert(
            fm1[0].getSubordinates()[0].getMetaValue("native_id") == 
            fm2[50].getSubordinates()[0].getMetaValue("native_id"))
        assert(
            fm1[0].getSubordinates()[0].getMetaValue("peak_apex_int") == 
            fm2[0].getSubordinates()[0].getMetaValue("peak_apex_int"))
        assert(
            fm1[0].getSubordinates()[0].getRT() == 
            fm2[0].getSubordinates()[0].getRT())

    def test_main_LCMS_MRM_Standards(self):
        """Test LCMS MRM example with standard sample types"""
        m = __main__()

        # m.main(
        #     filename_sequence=example_dir + 'LCMS_MRM/sequence.csv',
        #     filename_params=example_dir + 'LCMS_MRM/parameters.csv',
        #     delimiter=',',
        #     )
        # assert(~os.path.isfile(example_dir + 'LCMS_MRM/mzML/skippedSamples.csv'))
        
        m.main2(
            dir_I=example_dir + 'LCMS_MRM_Standards',
            delimiter=',',
            )

        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'LCMS_MRM/features/170808_Jonathan_yeast_Sacc1_1x.featureXML')
        fm1 = rawDataHandler.featureMap
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'LCMS_MRM/features/170808_Jonathan_yeast_Sacc1_1x_test.featureXML')
        fm2 = rawDataHandler.featureMap
        assert(
            fm1[50].getSubordinates()[0].getMetaValue("native_id") == 
            fm2[50].getSubordinates()[0].getMetaValue("native_id"))
        assert(
            fm1[50].getSubordinates()[0].getMetaValue("peak_apex_int") == 
            fm2[50].getSubordinates()[0].getMetaValue("peak_apex_int"))
        assert(
            fm1[50].getSubordinates()[0].getRT() == 
            fm2[50].getSubordinates()[0].getRT())