# -*- coding: utf-8 -*-
from smartPeak.io.smartPeak_i import smartPeak_i
from smartPeak.io.smartPeak_o import smartPeak_o
from smartPeak.core.smartPeak_openSWATH import smartPeak_openSWATH
from smartPeak.core.smartPeak_AbsoluteQuantitation import \
    smartPeak_AbsoluteQuantitation
from . import data_dir


class TestAbsoluteQuantitation():

    def test_load_quantitationMethods(self):
        AbsoluteQuantitation = smartPeak_AbsoluteQuantitation()

        # load the quantitation method
        quantitationMethods_csv_i = '''%s%s''' % (
            data_dir, "quantitationMethods_1.csv")
        AbsoluteQuantitation.load_quantitationMethods(
            {'quantitationMethods_csv_i': quantitationMethods_csv_i})
        assert(AbsoluteQuantitation.quantitationMethods[0].getLLOQ() == 0.25)
        assert(AbsoluteQuantitation.quantitationMethods[0].getULOQ() == 2.5)
        assert(AbsoluteQuantitation.quantitationMethods[
            0].getComponentName() == b'23dpg.23dpg_1.Light')

    def test_quantifyComponents(self):
        openSWATH = smartPeak_openSWATH()
        AbsoluteQuantitation = smartPeak_AbsoluteQuantitation()
        
        # load the quantitation method
        quantitationMethods_csv_i = '''%s%s''' % (
            data_dir, "quantitationMethods_1.csv")
        AbsoluteQuantitation.load_quantitationMethods(
            {'quantitationMethods_csv_i': quantitationMethods_csv_i})

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_2") 
        openSWATH.load_featureMap({'featureXML_i': featureXML_o})

        # quantify the components
        AbsoluteQuantitation.setUnknowns(openSWATH.featureMap)
        AbsoluteQuantitation.quantifyComponents()
        assert(AbsoluteQuantitation.unknowns[0].getSubordinates()[
                1].getMetaValue("native_id") == b'23dpg.23dpg_1.Light')
        assert(AbsoluteQuantitation.unknowns[0].getSubordinates()[
            1].getMetaValue("calculated_concentration") == 0.44335812456518986) 
        assert(AbsoluteQuantitation.unknowns[0].getSubordinates()[
            1].getMetaValue("concentration_units") == b'uM')
