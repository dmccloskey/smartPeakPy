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
        # from smartPeak.io.FileWriter import FileWriter
        # fileWriter = FileWriter()
        # raw_data = []
        # for id_f,fm in enumerate(fm1): 
        #     for id_sub,sub in enumerate(fm.getSubordinates()):
        # #         if sub.getMetaValue("native_id").decode("utf-8") == "glu-L.glu-L_1.Heavy": # 150601_0_BloodProject01_PLT_QC_Broth-1
        # #         if sub.getMetaValue("native_id").decode("utf-8") == "adp.adp_2.Light": # 150601_0_BloodProject01_PLT_QC_Broth-1
        # #         if sub.getMetaValue("native_id").decode("utf-8") == "fad.fad_1.Light": # 150601_0_BloodProject01_PLT_QC_Broth-1-10.0x
        #         component_name = sub.getMetaValue("native_id").decode("utf-8")
        #         hull_points = sub.getConvexHull().getHullPoints()
        #         for hull_point in hull_points:
        #             tmp = {
        #                 "component_name": component_name,
        #                 "time": hull_point[0],
        #                 "intensity": hull_point[1]
        #             }
        #             raw_data.append(tmp)
        # fileWriter.add_data(raw_data)
        # fileWriter.write_dict2csv(
        #      example_dir + 
        #     "LCMS_MRM_QCs/features/150601_0_BloodProject01_PLT_QC_Broth-1-rawData.csv")

        assert(
            fm1[50].getSubordinates()[0].getMetaValue("native_id") == 
            fm2[50].getSubordinates()[0].getMetaValue("native_id"))
        assert(
            fm1[50].getSubordinates()[0].getMetaValue("peak_apex_int") == 
            fm2[50].getSubordinates()[0].getMetaValue("peak_apex_int"))
        assert(
            fm1[50].getSubordinates()[0].getRT() == 
            fm2[50].getSubordinates()[0].getRT())

    def test_main_HPLC_FLD_Unknowns(self):
        """Test HPLC_FLD example with standard and unknown sample types"""
        print("running test_main_HPLC_FLD_Unknowns")
        m = __main__()
        
        m.example_LCMS_MRM_Standards(
            dir_I=example_dir + 'HPLC_FLD_Unknowns',
            delimiter=',',
            )

        # [TODO: update]
        # rawDataHandler = RawDataHandler()
        # fileReaderOpenMS = FileReaderOpenMS()
        # fileReaderOpenMS.load_featureMap(
        #     rawDataHandler, example_dir + 
        #     'HPLC_UV_Standards/features/100ug.featureXML')
        # fm1 = rawDataHandler.featureMap
        # fileReaderOpenMS.load_featureMap(
        #     rawDataHandler, example_dir + 
        #     'HPLC_UV_Standards/features/100ug_test.featureXML')
        # fm2 = rawDataHandler.featureMap
        # assert(
        #     fm1[0].getSubordinates()[0].getMetaValue("native_id") == 
        #     fm2[0].getSubordinates()[0].getMetaValue("native_id"))
        # assert(
        #     fm1[0].getSubordinates()[0].getMetaValue("peak_apex_int") == 
        #     fm2[0].getSubordinates()[0].getMetaValue("peak_apex_int"))
        # assert(
        #     fm1[0].getSubordinates()[0].getRT() == 
        #     fm2[0].getSubordinates()[0].getRT())