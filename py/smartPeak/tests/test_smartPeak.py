import pytest
from .smartPeak import smartPeak


class test_smartPeak():
    """tests for fastPeak"""

    #tests for smartPeak_openSWATH_cmd
    def test_make_osCmd(self, verbose_I=False):
        """"Test make_osCmd function

        EXAMPLE:
        tests = test_smartPeak()
        tests.test_make_osCmd(verbose_I=True)

        """
        #         params = [{'param1':'value1'},
        #                   {'param2':'value2'}]
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
        test = smartPeak.make_osCmd(params, function)
        if verbose_I: print(test)
        assert (test == ans)

    def test_convert_byte2String(self, verbose_I=False):
        """Test convert_byte2String function
        """
        str_test = 'a'.encode('utf-8')
        assert(smartPeak.convert_byte2String(str_test, encoding_I='utf-8')=='a')


    def test_convert_string2Byte(self, verbose_I=False):
        """Test convert_string2Byte function
        """
        str_test = 'a'.encode('utf-8')
        assert(smartPeak.convert_string2Byte('a', encoding_I='utf-8')==str_test)

    def test_convert_MQQMethod2Feature(self,verbose_I=False):
        """Test convert_MQQMethod2Feature function

        TODO:  load and run __main__ method and extract out test data
        """
        pass

    def test_parse_MQTransitionName(self,verbose_I=False):
        """Test parse_MQTransitionName function
        """
        heavy = 'atp.atp_1.Heavy'
        light = 'atp.atp_2.Light'
        component_group_name,quantifier,label_type = smartPeak.parse_MQTransitionName(heavy)
        assert(component_group_name=='atp')
        assert(quantifier==1)
        assert(label_type=='Heavy')
        component_group_name,quantifier,label_type = smartPeak.parse_MQTransitionName(light)
        assert(component_group_name=='atp')
        assert(quantifier==2)
        assert(label_type=='Light')

    

    def test_parseString(self, verbose_I=False):
        """Test parseString function
        
        """
        assert(smartPeak.parseString('1')==1)
        assert(smartPeak.parseString('-1')==-1)
        assert(smartPeak.parseString('1.0')==1.0)
        assert(smartPeak.parseString('0.005')==0.005)
        assert(smartPeak.parseString('-1.0')==-1.0)
        assert(smartPeak.parseString('[1]')==list('1'))
        assert(smartPeak.parseString('(1)')==tuple('1'))
        assert(smartPeak.parseString('{1}')==dict('1'))
        assert(smartPeak.parseString('a')=='a'.encode('utf-8'))
        assert(smartPeak.parseString('a',encode_str_I = False)=='a')
        assert(smartPeak.parseString("'a'")=='a'.encode('utf-8'))
        assert(smartPeak.parseString("['a','b','c']",encode_str_I = False)==['a','b','c'])
        assert(smartPeak.parseString("[1.0,2.0,3.0]")==[1.0,2.0,3.0])

    def test_castString(self, verbose_I=False):
        """Test castString function
        """
        assert(smartPeak.castString('1','int')==1)
        assert(smartPeak.castString('1.0','float')==1.0)
        assert(smartPeak.castString('TRUE','string')==True)
        assert(smartPeak.castString('FALSE','string')==True)
        assert(smartPeak.castString('a','string')=='a'.encode('utf-8'))

    def test_compareValues(self, verbose_I=False):
        """Test castString function
        """
        pass
        

    def runAllTests(self, verbose_I=False):
        """Run all unit tests"""
        self.test_make_osCmd(verbose_I=verbose_I)