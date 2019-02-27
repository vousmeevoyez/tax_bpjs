import unittest
import sys
import json

from tax_bpjs.tax import Tax

class TestTax(unittest.TestCase):
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
            "overtime_allowances"  : 0,
            "bonus_allowances"     : 0,
            "start_work_date"      : "01/01/2018",
            "end_work_date"        : "01/12/2018",
            "tax_method"           : "GROSS",
            "npwp_status"          : True,
            "marital_status"       : "SINGLE", #SINGLE / MARRIED / MARRIED_CI
            "dependents"           : 0,
            "tax_status"           : True, # true it means NPWP false means no NPWP
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
            "max_occupation_support" : 6000000,
            "occupation_support_rate": 0.05,
            "tax_exemption_grade"    : {
                "SINGLE"    : 54000000,
                "MARRIED"   : 58500000,
                "MARRIED_CI": 112500000,
                "PERSON"    : 4500000
            },
            "pph_grade_rate" : {
                "first" : 0.05,
                "second": 0.15,
                "third" : 0.25,
                "fourth": 0.30
            },
            "pph_grade_range" : {
                "first" : 50000000,
                "second": 250000000,
                "third" : 500000000
            }
        }

        self.tax = Tax(employee_info, configuration)

    def test_calc_occupation_support(self):
        """ Calculate occupation support """
        result = self.tax._occupation_support(100358400)
        self.assertEqual(result, 5017920)

        result = self.tax._occupation_support(117119400)
        self.assertEqual(result, 5855970)

    def calc_taxable_income_yearly(self):
        """ taxable income yearly """
        result = self.tax._taxable_income_yearly(71156700, "MARRIED", 1)
        self.assertEqual(result,8156700)

        result = self.tax._taxable_income_yearly(58500000, "MARRIED", 0)
        self.assertEqual(result,4650000)

        result = self.tax._taxable_income_yearly(88809600, "MARRIED", 0)
        self.assertEqual(result,30309000)

        result = self.tax._taxable_income_yearly(119100000, "MARRIED", 0)
        self.assertEqual(result,60600000)

        result = self.tax._taxable_income_yearly(78741000, "SINGLE", 0)
        self.assertEqual(result,24741000)

        result = self.tax._taxable_income_yearly(231600000, "MARRIED", 3)
        self.assertEqual(result,159600000)

        result = self.tax._taxable_income_yearly(67249200, "MARRIED", 1)
        self.assertEqual(result,4249200)

        result = self.tax._taxable_income_yearly(71156700, "MARRIED", 1)
        self.assertEqual(result,8156700)

        result = self.tax._taxable_income_yearly(74550000, "MARRIED", 0)
        self.assertEqual(result,16050000)

        result = self.tax._taxable_income_yearly(234000000, "MARRIED", 3)
        self.assertEqual(result,162000000)

    def test_classify_tax_exemption(self):
        """ classify tax exemption """
        result = self.tax._classify_tax_exemption("MARRIED", 3)
        self.assertEqual(result,72000000)

        result = self.tax._classify_tax_exemption("SINGLE", 0)
        self.assertEqual(result,54000000)

        result = self.tax._classify_tax_exemption("MARRIED", 1)
        self.assertEqual(result,63000000)

        result = self.tax._classify_tax_exemption("MARRIED", 2)
        self.assertEqual(result,67500000)

    def test_calc_tax_on_taxable_income_yearly(self):
        """ tax on taxable income yearly """
        result = self.tax._tax_on_taxable_income_yearly(4650000)
        self.assertEqual(result, 232500)

        result = self.tax._tax_on_taxable_income_yearly(30309000)
        self.assertEqual(result, 1515450)

        result = self.tax._tax_on_taxable_income_yearly(60600000)
        self.assertEqual(result, 4090000)

        result = self.tax._tax_on_taxable_income_yearly(159600000)
        self.assertEqual(result, 18940000)

        result = self.tax._tax_on_taxable_income_yearly(8156000)
        self.assertEqual(result, 407800)

        result = self.tax._tax_on_taxable_income_yearly(16050000)
        self.assertEqual(result, 802500)

        result = self.tax._tax_on_taxable_income_yearly(261384000)
        self.assertEqual(result, 35346000)

        result = self.tax._tax_on_taxable_income_yearly(38466000)
        self.assertEqual(result,  1923300 )

    def test_calc_tax_monthly(self):
        """ calculate _monthly tax """
        result = self.tax._monthly(407800 , 12)
        self.assertEqual(result,33983)

        result = self.tax._monthly(802500, 12)
        self.assertEqual(result,66875)

        result = self.tax._monthly(45000, 4)
        self.assertEqual(result,11250)

        result = self.tax._monthly(10300000, 12)
        self.assertEqual(result,858333)

    def test_calc_working_months(self):
        """ calculate working months """
        result = self.tax.working_months("01/01/2018", "01/12/2018")
        expected_result = 12,2018
        self.assertEqual(result, expected_result)

        result = self.tax.working_months("01/06/2018", "01/12/2018")
        expected_result = 7,2018
        self.assertEqual(result, expected_result)

        result = self.tax.working_months("01/01/2018", "01/10/2018")
        expected_result = 10,2018
        self.assertEqual(result, expected_result)

        result = self.tax.working_months("01/01/2018", "01/12/2018")
        expected_result = 12,2018
        self.assertEqual(result, expected_result)

        with self.assertRaises(ValueError):
            result = self.tax.working_months("01/02/2018", "01/02/2020")

        result = self.tax.working_months("01/11/2018", "01/12/2018")
        expected_result = 2,2018
        self.assertEqual(result, expected_result)

    def test_calc_non_tax_charge(self):
        """ calculate non tax charge"""
        result = self.tax._non_tax_charge(True, 35346000)
        self.assertEqual(result,0)

        result = self.tax._non_tax_charge(False, 232500)
        self.assertEqual(result,46500)

    def test_total_year_income(self):
        annual_bpjs = self.tax.annual_fee(12, 2018)

        employee_info = {
            "base_salary"         : 8000000,
            "fixed_allowances"     : 0,
            "non_fixed_allowances" : 0,
            "overtime_allowances"  : 0,
            "bonus_allowances"     : 0,
        }

        annual_bruto_income = self.tax.total_year_income(employee_info["base_salary"],
                                                         employee_info["overtime_allowances"],
                                                         employee_info["non_fixed_allowances"],
                                                         employee_info["bonus_allowances"],
                                                         annual_bpjs, 12)
        self.assertEqual(annual_bruto_income["annual_bruto_income"],  100358400)

        annual_bpjs = self.tax.annual_fee(12, 2018)

        employee_info2 = {
            "base_salary"          : 8000000,
            "fixed_allowances"     : 0,
            "non_fixed_allowances" : 8000000,
            "overtime_allowances"  : 560000,
            "bonus_allowances"     : 0,
        }
        annual_bruto_income2 = self.tax.total_year_income(employee_info2["base_salary"],
                                                          employee_info2["overtime_allowances"],
                                                          employee_info2["non_fixed_allowances"],
                                                          employee_info2["bonus_allowances"],
                                                          annual_bpjs, 12)
        self.assertEqual(annual_bruto_income2["annual_bruto_income"], 108918400)

    def test_annual_net_income(self):
        annual_bpjs = self.tax.annual_fee(12, 2018)

        employee_info = {
            "base_salary"         : 8000000,
            "fixed_allowances"     : 0,
            "non_fixed_allowances" : 0,
            "overtime_allowances"  : 0,
            "bonus_allowances"     : 0,
        }

        annual_bruto_income = self.tax.total_year_income(employee_info["base_salary"],
                                                         employee_info["overtime_allowances"],
                                                         employee_info["non_fixed_allowances"],
                                                         employee_info["bonus_allowances"],
                                                         annual_bpjs, 12)
        self.assertEqual(annual_bruto_income["annual_bruto_income"],  100358400)
        annual_net_income = self.tax.annual_net_income(annual_bruto_income["annual_bruto_income"],
                                                       employee_info["bonus_allowances"],
                                                       annual_bpjs)
        self.assertEqual(annual_net_income["annual_net_income"],  92466410 )

        annual_bpjs = self.tax.annual_fee(12, 2018)

        employee_info2 = {
            "base_salary"          : 8000000,
            "fixed_allowances"     : 0,
            "non_fixed_allowances" : 8000000,
            "overtime_allowances"  : 560000,
            "bonus_allowances"     : 0,
        }
        annual_bruto_income2 = self.tax.total_year_income(employee_info2["base_salary"],
                                                          employee_info2["overtime_allowances"],
                                                          employee_info2["non_fixed_allowances"],
                                                          employee_info2["bonus_allowances"],
                                                          annual_bpjs, 12)
        self.assertEqual(annual_bruto_income2["annual_bruto_income"], 108918400)

        annual_net_income = self.tax.annual_net_income(annual_bruto_income2["annual_bruto_income"],
                                                       employee_info2["bonus_allowances"],
                                                       annual_bpjs)
        self.assertEqual(annual_net_income["annual_net_income"], 100598410)

    def test_annual_tax(self):
        employee_info = {
            "base_salary"          : 8000000,
            "fixed_allowances"     : 0,
            "non_fixed_allowances" : 8000000,
            "overtime_allowances"  : 560000,
            "bonus_allowances"     : 0,
        }
        result = self.tax.annual_tax(8000000, employee_info["overtime_allowances"],
                                     employee_info["non_fixed_allowances"],
                                     employee_info["bonus_allowances"])

        self.assertTrue(result["working_months"])
        self.assertTrue(result["annual_taxable_income"])
        self.assertTrue(result["tax_exemption"])
        self.assertTrue(result["annual_tax"])
        self.assertTrue(result["annual_bpjs"])

if __name__ ==  '__main__' :
    unittest.main()
