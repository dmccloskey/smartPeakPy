# -*- coding: utf-8 -*-
from smartPeak.data.DBio import DBio


class TestDBio():

    def test_convert_list2string(self):
        db_io = DBio()

        test = ["a","b","c"]
        test_str = db_io.convert_list2string(test)
        assert(test_str == "a,b,c")

        test = "a,b,c"
        test_str = db_io.convert_list2string(test)
        assert(test_str == "a,b,c")