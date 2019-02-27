import unittest
import sys
import json

from tax_bpjs.bpjs import Bpjs

class TestBpjs(unittest.TestCase):
    """ "test class for BPJS """

    def setUp(self):
        employee_info = {
            "base_salary" : 8000000, #gaji pokok + tunjangan tetap
            "fixed_allowances" : {
                "other" : 0
            },
            "non_fixed_allowances": {
                "living": 0
            },
            "is_salary_allowances"      : True,
            "accident_insurance_status" : True,
            "pension_insurance_status"  : True,
            "old_age_insurance_status"  : True,
            "death_insurance_status"    : True,
            "health_insurance_status"   : True,
            "industry_risk_rate"        : 0.24
        }

        configuration = {
            "health_max_fee"                    : 8000000,
            "pension_max_fee"                   : 8094000,
            "old_pension_max_fee"               : 7703500,
            "individual_health_insurance_rate"  : 0.01,
            "company_health_insurance_rate"     : 0.04,
            "death_insurance_rate"              : 0.003,
            "individual_old_age_insurance_rate" : 0.02,
            "company_old_age_insurance_rate"    : 0.037,
            "individual_pension_insurance_rate" : 0.01,
            "company_pension_insurance_rate"    : 0.02,
        }

        self.bpjs = Bpjs(employee_info, configuration)

    def test_calc_company_old_age_insurance(self):
        """ test method to calculation company bpjs old age insurance """
        result = self.bpjs._company_old_age_insurance(8000000)
        self.assertEqual(result, 296000)

        result = self.bpjs._company_old_age_insurance(8500000)
        self.assertEqual(result, 314500)

        result = self.bpjs._company_old_age_insurance(4500000)
        self.assertEqual(result, 166500)

        result = self.bpjs._company_old_age_insurance(3700000)
        self.assertEqual(result, 136900)

        result = self.bpjs._company_old_age_insurance(6000000)
        self.assertEqual(result, 222000)

    def test_calc_individual_old_age_insurance(self):
        """ test method to calculation individual bpjs old age insurance """
        result = self.bpjs._individual_old_age_insurance(8000000)
        self.assertEqual(result, 160000)

        result = self.bpjs._individual_old_age_insurance(8500000)
        self.assertEqual(result, 170000)

        result = self.bpjs._individual_old_age_insurance(4500000)
        self.assertEqual(result, 90000)

        result = self.bpjs._individual_old_age_insurance(3700000)
        self.assertEqual(result, 74000)

        result = self.bpjs._individual_old_age_insurance(6000000)
        self.assertEqual(result, 120000)

    def test_calc_company_pension_insurance(self):
        """ test method to calculation company bpjs pension insurance """
        """ calculate bpjs pension insurance for 2019 """
        result = self.bpjs._company_pension_insurance(8000000)
        self.assertEqual(result, 160000)

        # january february 2018
        result = self.bpjs._company_pension_insurance(8500000, 2, 2018)
        self.assertEqual(result, 154070)

        result = self.bpjs._company_pension_insurance(8500000, 3, 2018)
        self.assertEqual(result, 161880)

        # january february 2018
        result = self.bpjs._company_pension_insurance(4500000, 2, 2018)
        self.assertEqual(result, 90000)

        result = self.bpjs._company_pension_insurance(4500000, 3, 2018)
        self.assertEqual(result, 90000)

        # january february 2018
        result = self.bpjs._company_pension_insurance(3700000, 2, 2018)
        self.assertEqual(result, 74000)

        result = self.bpjs._company_pension_insurance(3700000, 3, 2018)
        self.assertEqual(result, 74000)

    def test_calc_individual_pension_insurance(self):
        """ test method to calculation individual bpjs pension insurance """
        result = self.bpjs._individual_pension_insurance(8000000, 1, 2018)
        self.assertEqual(result, 77035)

        result = self.bpjs._individual_pension_insurance(8000000, 3, 2018)
        self.assertEqual(result, 80000)

        result = self.bpjs._individual_pension_insurance(8500000, 4, 2018)
        self.assertEqual(result, 80940)

    def test_calc_individual_health_insurance(self):
        """ test method to calculation individual bpjs health insurance """
        result = self.bpjs._individual_health_insurance(8000000)
        self.assertEqual(result, 80000)

        result = self.bpjs._individual_health_insurance(8500000)
        self.assertEqual(result, 80000)

        result = self.bpjs._individual_health_insurance(4500000)
        self.assertEqual(result, 45000)

        result = self.bpjs._individual_health_insurance(3700000)
        self.assertEqual(result, 37000)

        result = self.bpjs._individual_health_insurance(6000000)
        self.assertEqual(result, 60000)
    #end def

    def test_calc_company_health_insurance(self):
        """ test method to calculation company bpjs health insurance """
        result = self.bpjs._company_health_insurance(8000000)
        self.assertEqual(result, 320000)

        result = self.bpjs._company_health_insurance(8500000)
        self.assertEqual(result, 320000)

        result = self.bpjs._company_health_insurance(4500000)
        self.assertEqual(result, 180000)

        result = self.bpjs._company_health_insurance(3700000)
        self.assertEqual(result, 148000)

        result = self.bpjs._company_health_insurance(6000000)
        self.assertEqual(result, 240000)
    #end def

    def test_calc_accident_insurance(self):
        """ test method to calculation accident insurance """
        result = self.bpjs._accident_insurance(8000000, 0.24)
        self.assertEqual(result, 19200)

        result = self.bpjs._accident_insurance(8500000, 0.24)
        self.assertEqual(result, 20400)

        result = self.bpjs._accident_insurance(4500000, 0.24)
        self.assertEqual(result, 10800)

        result = self.bpjs._accident_insurance(3700000, 0.24)
        self.assertEqual(result, 8880)

        result = self.bpjs._accident_insurance(6000000, 0.24)
        self.assertEqual(result, 14400)
    #end def

    def test_calc_death_insurance(self):
        """ test method to calculation death insurance """
        result = self.bpjs._death_insurance(8000000)
        self.assertEqual(result, 24000)

        result = self.bpjs._death_insurance(8500000)
        self.assertEqual(result, 25500)

        result = self.bpjs._death_insurance(4500000)
        self.assertEqual(result, 13500)

        result = self.bpjs._death_insurance(3700000)
        self.assertEqual(result, 11100)

        result = self.bpjs._death_insurance(6000000)
        self.assertEqual(result, 18000)
    #end def

    def test_calc_monthly_fee(self):
        """ calculating monthly bpjs fee"""
        monthly_fee = self.bpjs.monthly_fee()
        self.assertEqual(monthly_fee["health_insurance"]["company"], 320000)
        self.assertEqual(monthly_fee["health_insurance"]["individual"], 80000)
        self.assertEqual(monthly_fee["old_age_insurance"]["company"], 296000)
        self.assertEqual(monthly_fee["old_age_insurance"]["individual"], 160000)
        self.assertEqual(monthly_fee["pension_insurance"]["company"], 160000)
        self.assertEqual(monthly_fee["pension_insurance"]["individual"],  80000)
        self.assertEqual(monthly_fee["accident_insurance"], 19200)
        self.assertEqual(monthly_fee["death_insurance"], 24000)

    def test_calc_annual_fee(self):
        """ calculating annual and monthly bpjs"""
        annually = self.bpjs.annual_fee(12, 2018)
        self.assertEqual(annually["health_insurance"]["company"], 3840000)
        self.assertEqual(annually["health_insurance"]["individual"], 960000)
        self.assertEqual(annually["old_age_insurance"]["company"], 3552000)
        self.assertEqual(annually["old_age_insurance"]["individual"], 1920000)
        self.assertEqual(annually["pension_insurance"]["company"], 1908140)
        self.assertEqual(annually["pension_insurance"]["individual"],  954070)
        self.assertEqual(annually["accident_insurance"], 230400)
        self.assertEqual(annually["death_insurance"], 288000)

    def test_summarize(self):
        """ calculating fixed allowances """
        fixed_allowances = {
            "thr" : 1000000
        }
        result = self.bpjs.summarize(fixed_allowances)
        self.assertEqual(result, 1000000)

if __name__ ==  '__main__' :
    unittest.main()
