"""
    Tax Calculation modules
"""
from datetime import datetime
from dateutil import relativedelta

from tax_bpjs.bpjs import Bpjs

class Tax(Bpjs):
    """ tax configuration """
    def __init__(self, employee_information, configuration, with_bpjs=True):
        self.base_salary         = employee_information["base_salary"         ]
        self.non_fixed_allowances= employee_information["non_fixed_allowances"]
        self.overtime_allowances = employee_information["overtime_allowances" ]
        self.bonus_allowances    = employee_information["bonus_allowances"    ]
        """
        self.honorarium          = employee_information["honorarium"         ]
        self.natura              = employee_information["natura"             ]
        self.other_allowances    = employee_information["other_allowances"   ]
        self.other_deduction     = employee_information["other_deduction"    ]
        """
        # personal information
        self.start_work_date     = employee_information["start_work_date"    ]
        self.end_work_date       = employee_information["end_work_date"      ]
        self.tax_method          = employee_information["tax_method"         ]
        self.npwp_status         = employee_information["npwp_status"        ]
        self.marital_status      = employee_information["marital_status"     ]
        self.dependents          = employee_information["dependents"         ]

        self.max_occupation_support   = configuration["max_occupation_support"]
        self.occupation_support_rate  = configuration["occupation_support_rate"]
        self.tax_exemption_grade      = configuration["tax_exemption_grade"]
        self.pph_grade_rate           = configuration["pph_grade_rate"]
        self.pph_grade_range          = configuration["pph_grade_range"]

        self.with_bpjs = with_bpjs

        super().__init__(employee_information, configuration)

    @staticmethod
    def _round_down(num, divisor):
        """
            Function to round down the number that calculated to near thousand

            Args:
                num (int): The amount that going to be rounded.
                divisor (int):

            Returns:
                rounded num (int) : The number that has been rounded.
        """
        if divisor <= 0:
            raise Exception('Divisor cannot be less than zero. Current divisor value was : {}'.format(divisor) )
        return num - (num % divisor)
    #end def

    def _occupation_support(self, annual_bruto_income):
        """
            Function to calculate person occupation support

            Args:
                monthly_gross_income (int) : total_salary + work_insurance +\
                                             health_insurance + allowance + insurance_premium
            Returns:
                occupation_support_deduction (int) : amount of person occupation support fee.
        """
        annual_taxable_occupation_income = annual_bruto_income * \
        self.occupation_support_rate

        if annual_taxable_occupation_income > self.max_occupation_support:
            occupation_support_deduction = self.max_occupation_support
        else:
            occupation_support_deduction = annual_taxable_occupation_income
        #endif
        return occupation_support_deduction
    #end def

    def _taxable_income_yearly(self, yearly_net_income, marital_status, dependents):
        """
            Function to calculate someone gross income annually

            Args:
                yearly_net_income(int) : monthly_net_income * working_months.
                marital_status(string) : the person marital status (SINGLE/MARRIED/MARRIED_CI).
                dependents(int) : amount of how many person have.

            Returns:
                annual_taxable_income (int) : The annual taxable net income.
        """
        annual_taxable_net_income = 0

        tax_exemption = self._classify_tax_exemption(marital_status, dependents)

        if yearly_net_income > tax_exemption:
            annual_taxable_net_income = yearly_net_income - tax_exemption
        #end if
        return self._round_down(annual_taxable_net_income, 1000)
    #end def

    def _classify_tax_exemption(self, marital_status, dependents):
        """
            Function to determine a person tax exemption amount

            Args:
                marital_status (string): The marital status of a person
                dependents(int) : How many dependents that person have.

            Returns:
                tax_exemption(int) : The tax exemption amount for a person\
                                     based on marital status and dependents.
        """
        try:
            base_tax_grade = self.tax_exemption_grade[marital_status]
        except KeyError:
            return 0

        if dependents > 3:
            # if dependents more than 3 it considered 3
            total_person_grade = self.tax_exemption_grade["PERSON"] * 3
        else:
            #if dependents <= 3
            total_person_grade = self.tax_exemption_grade["PERSON"] * dependents
        #end if
        return base_tax_grade + total_person_grade
    #end def

    def _tax_on_taxable_income_yearly(self, annual_taxable_income):
        """
            Function to calculate person tax on income

            Args:
                annual_taxable_income (int): The amount of person annual taxable income.

            Returns:
                tax_on_income (int) : The amount of tax that person have to pay annually.
        """
        tax_on_income = 0

        if annual_taxable_income > self.pph_grade_range["first"]:
            tax_on_income = self.pph_grade_rate["first"] *\
            self.pph_grade_range["first"]
        else:
            return self.pph_grade_rate["first"] * annual_taxable_income
        #end if

        if annual_taxable_income - self.pph_grade_range["first"] > 0:
            if annual_taxable_income > self.pph_grade_range["second"]:
                tax_on_income += self.pph_grade_rate["second"] * \
                        (self.pph_grade_range["second"] -
                         self.pph_grade_range["first"])
            else:
                tax_on_income += (annual_taxable_income -
                                  self.pph_grade_range["first"]) \
                                  * self.pph_grade_rate["second"]
            #end if
        #end if

        if annual_taxable_income - self.pph_grade_range["second"] > 0:
            if annual_taxable_income > self.pph_grade_range["third"]:
                tax_on_income += self.pph_grade_rate["third"]\
                * self.pph_grade_range["second"]
            else:
                tax_on_income += (annual_taxable_income - \
                                  self.pph_grade_range["second"]) *\
                                  self.pph_grade_rate["third"]
            #end if
        #end if

        if annual_taxable_income - self.pph_grade_range["third"] > 0:
            tax_on_income += (annual_taxable_income -
                              self.pph_grade_range["third"]) * \
                              self.pph_grade_rate["fourth"]
        #end if
        return tax_on_income
    #end def

    @staticmethod
    def _monthly(annual_net_income, working_months):
        """
            Function to calculate tax that person have to pay every month

            Args:
                annual_net_income(int) : annual_taxable_income - tax_on_annual_taxable_income .
                working_months (int): how many month that person has been working

            Returns:
                _monthly_tax(int) : The amount that person have to pay monthly.
        """
        monthly_tax = annual_net_income / working_months
        return int(monthly_tax)
    #end def

    @staticmethod
    def take_home_pay(tax_method, total_salary, monthly_tax, bpjs_fee):
        """
            Function to calculate how much money the person take home

            Args:
                tax_method(string) :  GROSS / NETT
                total_salary(int) : base_salary + allowance.
                monthly_tax(int) : The amount that person have to pay monthly.

            Returns:
                take_home_pay (int) : total_salary - monthly_tax.
        """
        take_home_pay = 0

        if tax_method == "GROSS":
            take_home_pay = total_salary - ( monthly_tax + bpjs_fee )
        elif tax_method == "NETT":
            take_home_pay = total_salary

        return take_home_pay
    #end if

    @staticmethod
    def _non_tax_charge(npwp_status, annual_taxable_income):
        """
            Function to calculate someone additional tax charge

            Args:
                npwp_status (string) : the person npwp status (A/NA).
                annual_taxable_income(int) the amount of tax that person have to pay annually

            Returns:
                additional_charge (int) : The amount of tax additional charge.
        """
        additional_charge = 0
        # add 20% if is not NPWP
        if npwp_status is not True:
            additional_charge = annual_taxable_income * 0.2
        #end if
        return additional_charge
    #end def

    @staticmethod
    def working_months(start_work_date, end_work_date):
        """ working motnh """
        # start date , start month , start year
        start = datetime.strptime(start_work_date, '%d/%m/%Y').date()
        end = datetime.strptime(end_work_date, '%d/%m/%Y').date()
        date_diff = relativedelta.relativedelta(start, end)
        months = date_diff.months
        years = date_diff.years
        if abs(years) > 0:
            raise ValueError("Only can calculate in a year period")

        start_year = start.year
        return abs(months) + 1, abs(start_year)
    #end def

    def total_year_income(self, base_salary, overtime_allowances, non_fixed_allowances, bonus_allowances, bpjs_calculation, working_months):
        """ total year income"""
        annual_salary    = base_salary * working_months # monthly salary * working months
        annual_allowances= overtime_allowances + \
        self.summarize(non_fixed_allowances) # monthly allowances
        annual_work      = bpjs_calculation["death_insurance"] \
                         + bpjs_calculation["accident_insurance"] #monthly bpjs work
        annual_health   = bpjs_calculation["health_insurance"]["company"] # monthly bpjs health
        bonus           = bonus_allowances # thr

        result = {
            "annual_salary"      : annual_salary,
            "annual_allowances"  : annual_allowances,
            "annual_bpjs_work"   : annual_work,
            "annual_bpjs_health" : annual_health,
            "bonus"              : bonus,
            "annual_bruto_income": annual_salary + annual_allowances \
                                   + annual_work + annual_health + bonus
        }

        return result
    #end def

    def annual_net_income(self, annual_bruto_income, bonus, bpjs_calculation):
        """ annual net income """
        occupation_support     = self._occupation_support(annual_bruto_income-bonus)
        thr_occupation_support = self._occupation_support(bonus)

        bpjs_pension_insurance = bpjs_calculation["pension_insurance"]["individual"]
        bpjs_old_age_insurance = bpjs_calculation["old_age_insurance"]["individual"]

        annual_net_income = annual_bruto_income - \
                            (occupation_support + thr_occupation_support + \
                             bpjs_pension_insurance + bpjs_old_age_insurance)
        result = {
            "occupation_support"     : occupation_support,
            "thr_occupation_support" : thr_occupation_support,
            "bpjs_pension_insurance" : bpjs_pension_insurance,
            "bpjs_old_age_insurance" : bpjs_old_age_insurance,
            "annual_net_income"      : annual_net_income
        }
        return result
    #end def

    def annual_tax(self, total_salary, overtime_allowances, non_fixed_allowances, bonus_allowances):
        """ calculate annual tax """

        #calculate working months and working year
        working_months, working_year = self.working_months(self.start_work_date, self.end_work_date)

        # calculate annual bpjs
        annual_bpjs = self.annual_fee(working_months, working_year,
                                      self.with_bpjs)

        # annual bruto income
        total_income_result = self.total_year_income(total_salary, overtime_allowances,
                                                     non_fixed_allowances, bonus_allowances,
                                                     annual_bpjs, working_months)
        # abbyak net income
        net_income_result = self.annual_net_income(total_income_result["annual_bruto_income"],
                                                   bonus_allowances,
                                                   annual_bpjs)

        # annual taxable income
        annual_taxable_income = self._taxable_income_yearly(net_income_result["annual_net_income"],
                                                           self.marital_status, self.dependents)

        # tax exemption
        tax_exemption = self._classify_tax_exemption( self.marital_status, self.dependents )

        # annual tax
        annual_tax = self._tax_on_taxable_income_yearly(annual_taxable_income)

        # only calculated when the employee doesn't have NPWP
        additional_charge =  self._non_tax_charge(self.npwp_status, annual_tax)
        annual_tax = annual_tax + additional_charge

        result = {
            "working_months"       : working_months,
            "total_income_result"  : total_income_result,
            "net_income_result"    : net_income_result,
            "annual_taxable_income": annual_taxable_income,
            "tax_exemption"        : tax_exemption,
            "annual_tax"           : annual_tax,
            "annual_bpjs"          : annual_bpjs
        }
        return result
    #end def

    def calculate_tax(self, last_annual_tax, first_annual_tax):
        """ calculate tax """
        # calculate annual tax without bonus
        annual_tax_without_bonus = self.annual_tax(self.base_salary, self.overtime_allowances,
                                                   self.non_fixed_allowances, 0 )
        # calculate monthly tax
        if first_annual_tax > 0:
            monthly_tax = self._monthly(first_annual_tax,
                                       annual_tax_without_bonus["working_months"])
        else:
            monthly_tax = self._monthly(annual_tax_without_bonus["annual_tax"],
                                       annual_tax_without_bonus["working_months"])
        #end if

        calculated_tax = annual_tax_without_bonus
        # calculate differences using last calculated annual tax
        if last_annual_tax > 0:
            # calculate bonus tax
            if self.bonus_allowances > 0:
                annual_tax_with_bonus = self.annual_tax(self.base_salary,
                                                        self.overtime_allowances,
                                                        self.non_fixed_allowances,
                                                        self.bonus_allowances)
                calculated_tax = annual_tax_with_bonus
            #end if
            differences = calculated_tax["annual_tax"] - last_annual_tax
        else:
            differences = 0
        #end if

        working_months = calculated_tax["working_months"]
        # convert calculation from annual to monthly
        annual_bpjs = calculated_tax["annual_bpjs"]

        annual_old_age_insurance = annual_bpjs["old_age_insurance"]["individual"]
        annual_pension_insurance = annual_bpjs["pension_insurance"]["individual"]
        annual_health_insurance = annual_bpjs["health_insurance"]["individual"]

        # new response
        deduction = {
            "monthly_tax" : monthly_tax + differences,
            "old_age_insurance" : int(annual_old_age_insurance/working_months),
            "pension_insurance" : int(annual_pension_insurance/working_months),
            "health_insurance"  : int(annual_health_insurance/working_months)
        }
        return calculated_tax, deduction
    #end def
#end class
