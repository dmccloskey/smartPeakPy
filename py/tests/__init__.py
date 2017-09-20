#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_smartPeak
----------------------------------

Tests for `smartPeak` module.
"""

from __future__ import absolute_import

from os.path import abspath, dirname, join

try:
    import pytest
    import pytest_benchmark
except ImportError:
    pytest = None

smartPeak_directory = abspath(join(dirname(abspath(__file__)), ".."))
smartPeak_location = abspath(join(smartPeak_directory, "smartPeak"))
data_dir = join(smartPeak_directory, "tests/data", "")

# def test_all(args=None):
#     """ alias for running all unit-tests on installed smartPeak
#     """
#     if pytest:
#         args = args if args else []

#         return pytest.main(
#             ['--pyargs', 'smartPeak', '--benchmark-skip', '-v', '-rs'] + args
#         )
#     else:
#         raise ImportError('missing package pytest and pytest_benchmark'
#                           ' required for testing')