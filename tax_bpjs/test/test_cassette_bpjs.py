"""
    Cassette Test using JSON file
"""
import unittest
import sys
import json
import os

from tax_bpjs.bpjs import Bpjs

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class TestCasseteBpjs(unittest.TestCase):
    """ BPJS Cassette test class"""

    def _match_dictionary(self, result, expected_result):
        for key, value in result.items():
            current_key = key
            # check whether it is nested or not
            try:
                for key, value in value.items():
                    sub_key = key
                    calculated = result[current_key][sub_key]
                    expected = expected_result[current_key][sub_key]
                    self.assertEqual(calculated, expected)
            except:
                calculated = result[current_key]
                expected = expected_result[current_key]
                self.assertEqual(calculated, expected)
            #end try
        #end for

    def test_monthly_fee(self):
        fullpath = os.path.join(__location__, 'monthly_bpjs_case.json')
        with open(fullpath) as f:
            data = json.load(f)
            # load all case
            cases = data["case"]
            # load configuration for this test
            configuration = data["configuration"]
            for case in cases:
                bpjs = Bpjs(case["input"], configuration)
                monthly_fee = bpjs.monthly_fee()
                self._match_dictionary(monthly_fee, case["output"])

    '''
    def test_annual_fee(self):
        fullpath = os.path.join(__location__, 'annual_bpjs_case.json')
        with open(fullpath) as f:
            data = json.load(f)
            # load all case
            cases = data["case"]
            # load configuration for this test
            configuration = data["configuration"]
            for case in cases:
                bpjs = Bpjs(case["input"], configuration)
                monthly_fee = bpjs.monthly_fee()
                self._match_dictionary(monthly_fee, case["output"])
    '''

if __name__ ==  '__main__' :
    unittest.main()
