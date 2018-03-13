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
        print("running test_main_LCMS_MRM_Unknown")
        m = __main__()
        
        m.example_LCMS_MRM_Unknowns(
            dir_I=example_dir + 'LCMS_MRM_Unknowns',
            delimiter=',',
            )

        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'LCMS_MRM_Unknowns/features/170808_Jonathan_yeast_Sacc1_1x.featureXML')
        fm1 = rawDataHandler.featureMap
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'LCMS_MRM_Unknowns/features/170808_Jonathan_yeast_Sacc1_1x_test.featureXML')
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
        #     example_dir + 'LCMS_MRM_Unknowns/features/170808_Jonathan_yeast_Sacc1_1x.featureXML',
        #     example_dir + 'LCMS_MRM_Unknowns/features/170808_Jonathan_yeast_Sacc1_1x_test.featureXML',
        #     shallow=False
        #     ))
        # assert(filecmp.cmp(
        #     example_dir + 'LCMS_MRM_Unknowns/SequenceSummary.csv',
        #     example_dir + 'LCMS_MRM_Unknowns/SequenceSummary_test.csv',
        #     shallow=False
        #     ))

    def test_main_GCMS_SIM_Unknown(self):
        """Test GCMS SIM Unknowns example"""
        print("running test_main_GCMS_SIM_Unknown")
        m = __main__()

        m.example_LCMS_MRM_Unknowns(
            dir_I=example_dir + 'GCMS_SIM_Unknowns',
            delimiter=',',
            )

        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()

        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'GCMS_SIM_Unknowns/features/GCMS_SIM.featureXML')
        fm1 = rawDataHandler.featureMap
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'GCMS_SIM_Unknowns/features/GCMS_SIM_test.featureXML')
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

    def test_main_GCMS_FullScan_Unknown(self):
        """Test GCMS FullScan Unknowns example"""
        print("running test_main_GCMS_FullScan_Unknown")
        m = __main__()

        m.example_LCMS_MRM_Unknowns(
            dir_I=example_dir + 'GCMS_FullScan_Unknowns',
            delimiter=',',
            )

        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()

        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'GCMS_FullScan_Unknowns/features/GCMS_FullScan.featureXML')
        fm1 = rawDataHandler.featureMap
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'GCMS_FullScan_Unknowns/features/GCMS_FullScan_test.featureXML')
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

    def test_main_HPLC_UV_Unknown(self):
        """Test HPLC UV Unknown example"""
        print("running test_main_HPLC_UV_Unknown")
        m = __main__()
        
        m.example_LCMS_MRM_Unknowns(
            dir_I=example_dir + 'HPLC_UV_Unknowns',
            delimiter=',',
            )

        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'HPLC_UV_Unknowns/features/20171013_HMP_C61_ISO_P1_GA1_UV_VIS_2.featureXML')
        fm1 = rawDataHandler.featureMap
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'HPLC_UV_Unknowns/features/20171013_HMP_C61_ISO_P1_GA1_UV_VIS_2_test.featureXML')
        fm2 = rawDataHandler.featureMap
        assert(
            fm1[0].getSubordinates()[0].getMetaValue("native_id") == 
            fm2[0].getSubordinates()[0].getMetaValue("native_id"))
        assert(
            fm1[0].getSubordinates()[0].getMetaValue("peak_apex_int") == 
            fm2[0].getSubordinates()[0].getMetaValue("peak_apex_int"))
        assert(
            fm1[0].getSubordinates()[0].getRT() == 
            fm2[0].getSubordinates()[0].getRT())

    def test_main_HPLC_UV_Standards(self):
        """Test HPLC_UV example with standard sample types"""
        print("running test_main_HPLC_UV_Standards")
        m = __main__()
        
        m.example_LCMS_MRM_Standards(
            dir_I=example_dir + 'HPLC_UV_Standards',
            delimiter=',',
            )

        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'HPLC_UV_Standards/features/100ug.featureXML')
        fm1 = rawDataHandler.featureMap
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'HPLC_UV_Standards/features/100ug_test.featureXML')
        fm2 = rawDataHandler.featureMap
        assert(
            fm1[0].getSubordinates()[0].getMetaValue("native_id") == 
            fm2[0].getSubordinates()[0].getMetaValue("native_id"))
        assert(
            fm1[0].getSubordinates()[0].getMetaValue("peak_apex_int") == 
            fm2[0].getSubordinates()[0].getMetaValue("peak_apex_int"))
        assert(
            fm1[0].getSubordinates()[0].getRT() == 
            fm2[0].getSubordinates()[0].getRT())

    def test_main_LCMS_MRM_Standards(self):
        """Test LCMS MRM example with standard sample types"""
        print("running test_main_LCMS_MRM_Standards")
        m = __main__()
        
        m.example_LCMS_MRM_Standards(
            dir_I=example_dir + 'LCMS_MRM_Standards',
            delimiter=',',
            )

        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'LCMS_MRM_Standards/features/150516_CM1_Level1.featureXML')
        fm1 = rawDataHandler.featureMap
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'LCMS_MRM_Standards/features/150516_CM1_Level1_test.featureXML')
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

    def test_main_LCMS_MRM_QCs(self):
        """Test LCMS MRM example with quality control sample types"""
        print("running test_main_LCMS_MRM_QCs")
        m = __main__()
        
        m.example_LCMS_MRM_Unknowns(
            dir_I=example_dir + 'LCMS_MRM_QCs',
            delimiter=',',
            )

        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            'LCMS_MRM_QCs/features/150601_0_BloodProject01_PLT_QC_Broth-1.featureXML')
        fm1 = rawDataHandler.featureMap
        fileReaderOpenMS.load_featureMap(
            rawDataHandler, example_dir + 
            # 'LCMS_MRM_QCs/features/150601_0_BloodProject01_PLT_QC_Broth-1-10.0x.featureXML')
            'LCMS_MRM_QCs/features/150601_0_BloodProject01_PLT_QC_Broth-1_test.featureXML')
        fm2 = rawDataHandler.featureMap

        # # Script to extract out hull points from features of interest
        # # -----
        # id1 = None
        # id2 = None
        # for id_f,fm in enumerate(fm1): 
        #     for id_sub,sub in enumerate(fm.getSubordinates()): 
        #         if sub.getMetaValue("native_id").decode("utf-8") == "glu-L.glu-L_1.Heavy": 
        #             id1 = (id_f, id_sub)
        #         if sub.getMetaValue("native_id").decode("utf-8") == "adp.adp_2.Light": 
        #             id2 = (id_f, id_sub)
        # glu = fm1[id1[0]].getSubordinates()[id1[1]]
        # print(glu.getConvexHull().getHullPoints())
        # adp = fm1[id2[0]].getSubordinates()[id2[1]]
        # print(adp.getConvexHull().getHullPoints())
        # id3 = None
        # for id_f, fm in enumerate(fm2): 
        #     for id_sub, sub in enumerate(fm.getSubordinates()): 
        #         if sub.getMetaValue("native_id").decode("utf-8") == "fad.fad_1.Light": 
        #             id3 = (id_f, id_sub)                    
        # fad = fm2[id3[0]].getSubordinates()[id3[1]]
        # print(fad.getConvexHull().getHullPoints())
        # # -----

        assert(
            fm1[50].getSubordinates()[0].getMetaValue("native_id") == 
            fm2[50].getSubordinates()[0].getMetaValue("native_id"))
        assert(
            fm1[50].getSubordinates()[0].getMetaValue("peak_apex_int") == 
            fm2[50].getSubordinates()[0].getMetaValue("peak_apex_int"))
        assert(
            fm1[50].getSubordinates()[0].getRT() == 
            fm2[50].getSubordinates()[0].getRT())