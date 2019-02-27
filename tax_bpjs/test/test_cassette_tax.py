"""
    Cassette Test using JSON file
"""
import unittest
import sys
import json
import os

from tax_bpjs.tax import Tax

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class TestCasseteTax(unittest.TestCase):
    """ Tax Cassette test class"""

    def _match_dictionary(self, result, expected_result):
        for key, value in expected_result.items():
            calculated = result[key]
            expected = expected_result[key]
            self.assertEqual(calculated, expected)
        #end for

    def test_calculate_tax(self):
        fullpath = os.path.join(__location__, 'tax_case.json')
        with open(fullpath) as f:
            data = json.load(f)
            # load all case
            cases = data["case"]
            # load configuration for this test
            configuration = data["configuration"]

            first_annual_tax = 0
            last_annual_tax  = 0
            counter = 0
            for case in cases:
                tax= Tax(case["input"], configuration)
                calculated_tax, deduction = tax.calculate_tax(last_annual_tax,
                                                              first_annual_tax)
                if counter < 1:
                    first_annual_tax = calculated_tax["annual_tax"]
                #end if
                last_annual_tax = calculated_tax["annual_tax"]

                self._match_dictionary(deduction, case["output"])

                counter += 1

    def test_calculate_tax_outstanding(self):
        fullpath = os.path.join(__location__, 'tax_outstanding_case.json')
        with open(fullpath) as f:
            data = json.load(f)
            # load all case
            cases = data["case"]
            # load configuration for this test
            configuration = data["configuration"]

            first_annual_tax = 0
            last_annual_tax  = 0
            counter = 0
            for case in cases:
                tax= Tax(case["input"], configuration, False)
                calculated_tax, deduction = tax.calculate_tax(last_annual_tax,
                                                              first_annual_tax)
                print(json.dumps(calculated_tax))
                print(deduction)
                self._match_dictionary(deduction, case["output"])

                counter += 1

if __name__ ==  '__main__' :
    unittest.main()
