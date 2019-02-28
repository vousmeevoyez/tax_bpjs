from tax_bpjs.bpjs import Bpjs
from tax_bpjs.tax import Tax

"""
    Case 1: Calculate BPJS Only
"""
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

BPJS = Bpjs(employee_info, configuration)
monthly_bpjs_fee = BPJS.monthly_fee()
print(monthly_bpjs_fee)

"""
    Case 2: Calculate Tax Only
"""
employee_info = {
    "base_salary"          : 5750000,
    "fixed_allowances"     : 0,
    "non_fixed_allowances" : 0,
    "overtime_allowances"  : 0,
    "bonus_allowances"     : 0,
    "start_work_date"      : "01/01/2018",
    "end_work_date"        : "01/12/2018",
    "tax_method"           : "GROSS",
    "npwp_status"          : True,
    "marital_status"       : "MARRIED", #SINGLE / MARRIED / MARRIED_CI
    "dependents"           : 0,
    "is_salary_allowances"      : False,
    "accident_insurance_status" : False,
    "pension_insurance_status"  : False,
    "old_age_insurance_status"  : False,
    "death_insurance_status"    : False,
    "health_insurance_status"   : False,
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
tax = Tax(employee_info, configuration, False) # False means no BPJS
last_calculated_tax = 0 # zero beacause it is calculation for the first
first_calculated_tax = 0 # set zero too
calculated_tax, deduction = tax.calculate_tax(0, 0)
print(calculated_tax)
print(deduction)

"""
    Case 3: Calculate Tax + BPJS
"""
employee_info = {
    "base_salary"          : 8000000,
    "fixed_allowances"     : 0,
    "non_fixed_allowances" : 0,
    "overtime_allowances"  : 0,
    "bonus_allowances"     : 0,
    "start_work_date"      : "01/01/2018",
    "end_work_date"        : "01/12/2018",
    "tax_method"           : "GROSS",
    "npwp_status"          : True,
    "marital_status"       : "SINGLE", #SINGLE / MARRIED / MARRIED_CI
    "dependents"           : 0,
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
tax = Tax(employee_info, configuration)
last_calculated_tax = 0 # zero beacause it is calculation for the first
first_calculated_tax = 0 # set zero too
calculated_tax, deduction = tax.calculate_tax(0, 0)
print(calculated_tax)
print(deduction)
