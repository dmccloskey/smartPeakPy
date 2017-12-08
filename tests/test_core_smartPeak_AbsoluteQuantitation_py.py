# -*- coding: utf-8 -*-
from smartPeak.core.smartPeak_i import smartPeak_i
from smartPeak.core.smartPeak_o import smartPeak_o
from smartPeak.core.smartPeak_openSWATH_py import smartPeak_openSWATH_py
from smartPeak.core.smartPeak_AbsoluteQuantitation_py import \
    smartPeak_AbsoluteQuantitation_py
from . import data_dir


class TestAbsoluteQuantitation_py():

    def test_load_quantitationMethods(self):
        AbsoluteQuantitation_py = smartPeak_AbsoluteQuantitation_py()

        # load the quantitation method
        quantitationMethods_csv_i = '''%s%s''' % (
            data_dir, "quantitationMethods_1.csv")
        AbsoluteQuantitation_py.load_quantitationMethods(
            {'quantitationMethods_csv_i': quantitationMethods_csv_i})
        assert(AbsoluteQuantitation_py.quantitationMethods[0].getLLOQ() == 0.0)

    def test_quantifyComponents(self):
        openSWATH_py = smartPeak_openSWATH_py()
        AbsoluteQuantitation_py = smartPeak_AbsoluteQuantitation_py()
        
        # load the quantitation method
        quantitationMethods_csv_i = '''%s%s''' % (
            data_dir, "quantitationMethods_1.csv")
        AbsoluteQuantitation_py.load_quantitationMethods(
            {'quantitationMethods_csv_i': quantitationMethods_csv_i})

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_2") 
        openSWATH_py.load_featureMap({'featureXML_i': featureXML_o})

        # quantify the components
        AbsoluteQuantitation_py.setUnknowns(openSWATH_py.featureMap)
        AbsoluteQuantitation_py.quantifyComponents()
        assert(AbsoluteQuantitation_py.unknowns[0].getSubordinates()[
                1].getMetaValue("native_id") == b'23dpg.23dpg_1.Light')
        assert(AbsoluteQuantitation_py.unknowns[0].getSubordinates()[
            1].getMetaValue("calculated_concentration") == 0.4422842478400926) 
        assert(AbsoluteQuantitation_py.unknowns[0].getSubordinates()[
            1].getMetaValue("concentration_units") == b'uM')
        assert(AbsoluteQuantitation_py.unknowns[15].getSubordinates()[
            1].getMetaValue("native_id") == b'amp.amp_1.Light')
        assert(AbsoluteQuantitation_py.unknowns[15].getSubordinates()[
            1].getMetaValue("calculated_concentration") == 5.516940577368133)
        assert(AbsoluteQuantitation_py.unknowns[15].getSubordinates()[
            1].getMetaValue("concentration_units") == b'uM')