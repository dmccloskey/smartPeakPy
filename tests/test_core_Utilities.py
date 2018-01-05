# -*- coding: utf-8 -*-
from smartPeak.core.Utilities import Utilities


class testUtilities():
    """tests for Utilities"""

    # tests for smartPeak_openSWATH_cmd
    def test_make_osCmd(self, verbose_I=False):
        """Test make_osCmd function

        """

        params = [
            {
                'param': 'param1',
                'delim': ' ',
                'value': 'value1'
            },
            {
                'param': 'param2',
                'delim': ' ',
                'value': 'value2'
            },
        ]
        function = 'test'
        ans = 'test param1 value1 param2 value2'
        test = Utilities.make_osCmd(params, function)
        if verbose_I: 
            print(test)
        assert (test == ans)

    def test_convert_byte2String(self, verbose_I=False):
        """Test convert_byte2String function
        """
        str_test = 'a'.encode('utf-8')
        assert(Utilities.convert_byte2String(str_test, encoding_I='utf-8') == 'a')

    def test_convert_string2Byte(self, verbose_I=False):
        """Test convert_string2Byte function
        """
        str_test = 'a'.encode('utf-8')
        assert(Utilities.convert_string2Byte('a', encoding_I='utf-8') == str_test)

    # def test_convert_MQQMethod2Feature(self, verbose_I=False):
    #     """Test convert_MQQMethod2Feature function
    #     """
        
    #     filename_I = '/home/user/openMS_MRMworkflow/BloodProject01/BloodProject01_qmethod.csv'
    #     filename_O = '/home/user/openMS_MRMworkflow/BloodProject01/BloodProject01_SWATH_feature.csv'     
    #     self.convert_MQQMethod2Feature(filename_I, filename_O) 

    #     # TODO: re-read in resulting file and compare to test file

    def test_parse_MQTransitionName(self, verbose_I=False):
        """Test parse_MQTransitionName function
        """
        heavy = 'atp.atp_1.Heavy'
        light = 'atp.atp_2.Light'
        component_group_name, quantifier, label_type = \
            Utilities.parse_MQTransitionName(heavy)
        assert(component_group_name == 'atp')
        assert(quantifier == 1)
        assert(label_type == 'Heavy')
        component_group_name, quantifier, label_type = \
            Utilities.parse_MQTransitionName(light)
        assert(component_group_name == 'atp')
        assert(quantifier == 2)
        assert(label_type == 'Light')    

    def test_parseString(self, verbose_I=False):
        """Test parseString function
        
        """
        utilities = Utilities()
        assert(utilities.parseString('1') == 1)
        assert(utilities.parseString('-1') == -1)
        assert(utilities.parseString('1.0') == 1.0)
        assert(utilities.parseString('0.005') == 0.005)
        assert(utilities.parseString('-1.0') == -1.0)
        assert(utilities.parseString('[1]') == [1])
        assert(utilities.parseString('(1)') == ('1',))
        # assert(utilities.parseString('{"a":1}') == {"a": 1})
        assert(utilities.parseString('a') == 'a'.encode('utf-8'))
        assert(utilities.parseString("'a'", encode_str_I=False) == 'a')
        assert(utilities.parseString("'a'") == "'a'".encode('utf-8'))
        assert(utilities.parseString(
            "['a','b','c']", encode_str_I=False) == ['a', 'b', 'c'])
        assert(utilities.parseString("[1.0,2.0,3.0]") == [1.0, 2.0, 3.0])

    def test_castString(self, verbose_I=False):
        """Test castString function
        """
        assert(Utilities.castString('1', 'int') == 1)
        assert(Utilities.castString('1.0', 'float') == 1.0)
        assert(Utilities.castString('TRUE', 'string'))
        assert(Utilities.castString('FALSE', 'string'))
        assert(Utilities.castString('a', 'string') == 'a'.encode('utf-8'))
   
    # def test_updateParameters(self, verbose_I=False):
    #     """Test updateParameters function

    #     TODO: 
    #     1. make a test "update_parameters.csv"
    #     2. read in "update_parameters"
    #     """
    #     utilities = Utilities()
    #     featurefinder = pyopenms.MRMFeatureFinderScoring()
    #     ff_parameters = featurefinder.getParameters()
    #     ff_parameters = utilities.updateParameters(
    #         ff_parameters,
    #         test_parameters,
    #         )
    #     featurefinder.setParameters(ff_parameters)
    #     test_parameters = featurefinder.getParameters()
    #     assert(test_parameters == ff_parameters)

    def test_setParameters(self, verbose_I=False):
        """Test setParameters function

        TODO: 
        1. make a test "update_parameters.csv"
        2. read in "update_parameters"
        """
        pass

    def compareValues(self, verbose_I=False):
        """Test castString function
        """
        assert(Utilities.compareValues(1, 2, '<'))
        assert(~Utilities.compareValues(1, 2, '>'))
        assert(Utilities.compareValues(-1, 2, '<abs'))
        assert(Utilities.compareValues(-3, 2, '>abs'))