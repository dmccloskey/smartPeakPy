import pytest
from smartPeak import smartPeak


class test_fastPeak():
    """tests for fastPeak"""

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

    def runAllTests(self):
        """Run all unit tests"""
        self.test_make_osCmd(verbose_I=True)