#import pytest
from .smartPeak import smartPeak
from .smartPeak_openSWATH_py import smartPeak_openSWATH_py


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

    #tests for smartPeak_openSWATH_py
    def test_parseString(self, verbose_I=False):
        """Test parseString function
        
        """
        assert(smartPeak_openSWATH_py.parseString('1')==1)
        assert(smartPeak_openSWATH_py.parseString('-1')==-1)
        assert(smartPeak_openSWATH_py.parseString('1.0')==1.0)
        assert(smartPeak_openSWATH_py.parseString('0.005')==0.005)
        assert(smartPeak_openSWATH_py.parseString('-1.0')==-1.0)
        assert(smartPeak_openSWATH_py.parseString('[1]')==list('1'))
        assert(smartPeak_openSWATH_py.parseString('(1)')==tuple('1'))
        #assert(smartPeak_openSWATH_py.parseString('{1}')==dict('1'))
        assert(smartPeak_openSWATH_py.parseString('a')=='a'.encode('utf-8'))
        

    def runAllTests(self):
        """Run all unit tests"""
        self.test_make_osCmd(verbose_I=True)