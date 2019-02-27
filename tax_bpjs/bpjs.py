"""
    BPJS Calculator
"""
class Bpjs:
    """ BPJS Class """

    def __init__(self, employee_information, configuration):
        """
        Parameters:
            employee_information (dictionary):
                base_salary -- (Integer) Gaji Pokok
                fixed_allowances -- (Integer) Tunjangan Tetap
                non_fixed_allowances -- (Integer) Tunjangan Tidak Tetap
                is_salary_allowances -- (Boolean), True it means we calculate SALARY +
                ALLOWANCE , False it means we calculate SALARY ONLY
                accident_insurance_status -- (Boolean) BPJS Jaminan Kecelakaan
                Enrollment Status
                pension_insurance_status -- (Boolean) BPJS Jaminan Pensiun
                Enrollment Status
                death_insurance_status -- (Boolean) BPJS Jaminan Kematian
                Enrollment Status
                health_insurance_status -- (Boolean) BPJS Jaminan Kesehatan
                Enrollment Status
                industry_risk_rate -- (Float) Industry Risk Rate (ex : 0.24)

            configuration -- (optional)(dictionary):
                pension_max_fee -- (Integer) Jumlah Maksimal BPJS
                health_max_fee -- (Integer) Jumlah Maksimal BPJS
                pension_max_fee -- (Integer) Jumlah Maksimal BPJS
                pension_max_fee -- (Integer) Jumlah Maksimal BPJS
        """
        self.base_salary               = employee_information["base_salary"]
        self.fixed_allowances          = employee_information["fixed_allowances"]
        self.non_fixed_allowances      = employee_information["non_fixed_allowances"]
        self.is_salary_allowances      = employee_information["is_salary_allowances"]
        self.accident_insurance_status = employee_information["accident_insurance_status"]
        self.pension_insurance_status  = employee_information["pension_insurance_status"]
        self.old_age_insurance_status  = employee_information["old_age_insurance_status"]
        self.death_insurance_status    = employee_information["death_insurance_status"]
        self.health_insurance_status   = employee_information["health_insurance_status"]
        self.industry_risk_rate        = employee_information["industry_risk_rate"]

        self.health_max_fee  = configuration["health_max_fee"]
        self.pension_max_fee = configuration["pension_max_fee"]
        self.old_pension_max_fee = configuration["old_pension_max_fee"]

        self.individual_health_insurance_rate =\
        configuration["individual_health_insurance_rate"]
        self.company_health_insurance_rate =\
        configuration["company_health_insurance_rate"]

        self.death_insurance_rate =\
        configuration["death_insurance_rate"]

        self.individual_old_age_insurance_rate=\
        configuration["individual_old_age_insurance_rate"]
        self.company_old_age_insurance_rate=\
        configuration["company_old_age_insurance_rate"]

        self.individual_pension_insurance_rate =\
        configuration["individual_pension_insurance_rate"]
        self.company_pension_insurance_rate =\
        configuration["company_pension_insurance_rate"]
    #end def

    def summarize(self, allowances):
        """
            Function to summarize allowances

            Args:
                allowances (dictionary): { }

            Returns:
                allowances(int) : total allowances
        """
        total_allowances = 0
        if isinstance(allowances, dict):
            for key, value in allowances.items():
                total_allowances = total_allowances + int(value)
            #end for
        else:
            total_allowances = allowances
        return total_allowances
    #end def

    def _individual_health_insurance(self, total_salary):
        """
            Function to calculate bpjs health individual

            Args:
                total_salary (int): The amount of base salary that person receive each month.

            Returns:
                individual_health_insurance(int) : the amount of bpjs
                health insurance that person have to pay monthly
        """
        individual_health_insurance = 0

        if total_salary <= self.health_max_fee:
            individual_health_insurance = total_salary \
            *  self.individual_health_insurance_rate
        else:
            individual_health_insurance = self.health_max_fee\
            * self.individual_health_insurance_rate
        #end if
        return individual_health_insurance
    #end def

    def _company_health_insurance(self, total_salary):
        """
            Function to calculate bpjs health that paid by company

            Args:
                total_salary (int): The amount of base salary that person receive each month.

            Returns:
                company_health_insurance (int) : the amount of \
                        bpjs health insurance that person have to pay monthly
        """
        company_health_insurance = 0

        if total_salary <= self.health_max_fee:
            company_health_insurance = total_salary *\
            self.company_health_insurance_rate
        else:
            company_health_insurance = self.health_max_fee\
            * self.company_health_insurance_rate
        #end if
        return company_health_insurance
    #end def

    @staticmethod
    def _accident_insurance(total_salary, industry_risk_rate):
        """
            Function to calculate bpjs work + death insurance

            Args:
                total_salary (int): The amount of base salary that person receive each month.
                industry_risk_rate (float) : the risk percentage amout\
                        based on industry that person work on

            Returns:
                accident_insurance(int) : the amount of bpjs work\
                        insurance that person have to pay monthly
        """

        industry_type_rate = industry_risk_rate / 100

        accident_insurance_rate = industry_type_rate
        accident_insurance = accident_insurance_rate * total_salary

        return round(accident_insurance, 1)
    #end def

    def _death_insurance(self, total_salary):
        """
            Function to calculate death insurance

            Args:
                total_salary (int): The amount of base salary that person receive each month.
            Returns:
                death_insurance(int) : amount of accident insurance that person have to pay
        """
        return int(total_salary * self.death_insurance_rate)
    #end def

    def _company_old_age_insurance(self, total_salary):
        """
            Function to calculate company old age insurance

            Args:
                total_salary (int): The amount of base salary that person receive each month.

            Returns:
                company_old_age_insurance(int) : \
                        amount of individual person old age insurance fee.
        """
        return self.company_old_age_insurance_rate * total_salary
    #end def

    def _individual_old_age_insurance(self, total_salary):
        """
            Function to calculate person old age insurance

            Args:
                total_salary (int): The amount of base salary that person receive each month.

            Returns:
                individual_health_insurance (int) :\
                        amount of company person old age insurance fee.
        """
        return self.individual_old_age_insurance_rate * total_salary
    #end def

    def _individual_pension_insurance(self, total_salary, month=None, year=None):
        """
            Function to calculate person pension contribution fee

            Args:
                base_salary (int): The amount of base salary that person receive each month.

            Returns:
                individual_pension_insurance(int) : amount of person tht contribution fee.
        """
        individual_pension_insurance = 0

        pension_max_fee = self.pension_max_fee
        # special case in 2018
        if year == 2018:
            if month <= 2:
                pension_max_fee = self.old_pension_max_fee
            #end if
        #end if

        if total_salary > pension_max_fee:
            individual_pension_insurance = pension_max_fee \
            * self.individual_pension_insurance_rate
        else:
            individual_pension_insurance = total_salary \
            * self.individual_pension_insurance_rate
        #end if
        return individual_pension_insurance
    #end def

    def _company_pension_insurance(self, total_salary, month=None, year=None):
        """
            Function to calculate person pension contribution fee

            Args:
                base_salary (int): The amount of base salary that person receive each month.

            Returns:
                company_pension_insurance (int) : amount of person tht contribution fee.
        """
        company_pension_insurance = 0

        pension_max_fee = self.pension_max_fee
        # special case in 2018
        if year == 2018:
            if month <= 2:
                pension_max_fee = self.old_pension_max_fee
            #end if
        #end if

        if total_salary > pension_max_fee:
            company_pension_insurance = pension_max_fee *\
            self.company_pension_insurance_rate
        else:
            company_pension_insurance = total_salary * \
            self.company_pension_insurance_rate
        #end if
        return company_pension_insurance
    #end def

    def monthly_fee(self):
        """ calculate monthly bpjs """
        total_salary = self.base_salary
        if self.is_salary_allowances is True:
            fixed_allowances = self.summarize( self.fixed_allowances )
            non_fixed_allowances = self.summarize( self.non_fixed_allowances )
            total_salary = total_salary + non_fixed_allowances + fixed_allowances
        #end if

        company_old_age_insurance = 0
        individual_old_age_insurance = 0
        if self.old_age_insurance_status is True:
            company_old_age_insurance = \
            self._company_old_age_insurance(total_salary)

            individual_old_age_insurance = \
            self._individual_old_age_insurance(total_salary)
        #end if

        company_pension_insurance    = 0
        individual_pension_insurance = 0
        if self.pension_insurance_status is True:
            company_pension_insurance = \
            self._company_pension_insurance(total_salary)

            individual_pension_insurance = \
            self._individual_pension_insurance(total_salary)
        #end if

        company_health_insurance    = 0
        individual_health_insurance = 0
        if self.health_insurance_status is True:
            company_health_insurance = \
            self._company_health_insurance(total_salary)

            individual_health_insurance = \
            self._individual_health_insurance(total_salary)
        #end if

        death_insurance = 0
        if self.death_insurance_status is True:
            death_insurance = self._death_insurance(total_salary)
        #end if

        accident_insurance = 0
        if self.accident_insurance_status is True:
            accident_insurance = \
            self._accident_insurance(total_salary, \
                                          self.industry_risk_rate)
        #end if

        monthly = {
            "old_age_insurance" : {
                "company"    : company_old_age_insurance,
                "individual" : individual_old_age_insurance,
            },
            "pension_insurance" : {
                "company"    : company_pension_insurance,
                "individual" : individual_pension_insurance,
            },
            "health_insurance" : {
                "company"    : company_health_insurance,
                "individual" : individual_health_insurance,
            },
            "death_insurance" : death_insurance,
            "accident_insurance" : accident_insurance
        }
        return monthly
    #end def

    def annual_fee(self, working_months, year, with_bpjs=True):
        """
            calculate annual bpjs fee
            parameter:
                working_months -- working_months
                year -- year
        """
        monthly_bpjs = []

        total_salary = self.base_salary
        if self.is_salary_allowances is True:
            fixed_allowances = self.summarize( self.fixed_allowances )
            non_fixed_allowances = self.summarize( self.non_fixed_allowances )
            total_salary = total_salary + non_fixed_allowances + fixed_allowances
        #end if

        # initialize variable for storing the annual bpjs
        annual_c_old_age_insurance = 0
        annual_i_old_age_insurance = 0
        annual_c_pension_insurance = 0
        annual_i_pension_insurance = 0
        annual_c_health_insurance  = 0
        annual_i_health_insurance  = 0
        annual_death_insurance     = 0
        annual_accident_insurance  = 0
        
        if with_bpjs is True:
        # only calculate bpjs if is enabled and automatically set everthing to zero when is false
            start_month = 1
            for month in range(start_month, working_months+1):

                company_old_age_insurance = 0
                individual_old_age_insurance = 0
                if self.old_age_insurance_status is True:
                    company_old_age_insurance = \
                    self._company_old_age_insurance(total_salary)

                    individual_old_age_insurance = \
                    self._individual_old_age_insurance(total_salary)
                #end if

                company_pension_insurance    = 0
                individual_pension_insurance = 0
                if self.pension_insurance_status is True:
                    company_pension_insurance = \
                    self._company_pension_insurance(total_salary, month, year)

                    individual_pension_insurance = \
                    self._individual_pension_insurance(total_salary, month, year)
                #end if

                company_health_insurance    = 0
                individual_health_insurance = 0
                if self.health_insurance_status is True:
                    company_health_insurance = \
                    self._company_health_insurance(total_salary)

                    individual_health_insurance = \
                    self._individual_health_insurance(total_salary)
                #end if

                death_insurance = 0
                if self.death_insurance_status is True:
                    death_insurance = self._death_insurance(total_salary)
                #end if

                accident_insurance = 0
                if self.accident_insurance_status is True:
                    accident_insurance = \
                    self._accident_insurance(total_salary, \
                                                  self.industry_risk_rate)
                #end if

                monthly = {
                    "old_age_insurance" : {
                        "company"    : company_old_age_insurance,
                        "individual" : individual_old_age_insurance,
                    },
                    "pension_insurance" : {
                        "company"    : company_pension_insurance,
                        "individual" : individual_pension_insurance,
                    },
                    "health_insurance" : {
                        "company"    : company_health_insurance,
                        "individual" : individual_health_insurance,
                    },
                    "death_insurance" : death_insurance,
                    "accident_insurance" : accident_insurance
                }

                monthly_bpjs.append(monthly)

                annual_c_old_age_insurance = annual_c_old_age_insurance \
                                                  + company_old_age_insurance

                annual_i_old_age_insurance = annual_i_old_age_insurance \
                                                  + individual_old_age_insurance

                annual_c_pension_insurance = annual_c_pension_insurance \
                                                  + company_pension_insurance

                annual_i_pension_insurance = annual_i_pension_insurance \
                                                  + individual_pension_insurance

                annual_c_health_insurance = annual_c_health_insurance \
                                                 + company_health_insurance

                annual_i_health_insurance = annual_i_health_insurance \
                                                 + individual_health_insurance

                annual_death_insurance = annual_death_insurance\
                                              + death_insurance

                annual_accident_insurance = annual_accident_insurance\
                                                 + accident_insurance
            #end for

        annual_bpjs = {
            "old_age_insurance" : {
                "company"    : annual_c_old_age_insurance,
                "individual" : annual_i_old_age_insurance,
            },
            "pension_insurance" : {
                "company"    : annual_c_pension_insurance,
                "individual" : annual_i_pension_insurance,
            },
            "health_insurance" : {
                "company"    : annual_c_health_insurance,
                "individual" : annual_i_health_insurance,
            },
            "death_insurance" : annual_death_insurance,
            "accident_insurance" : annual_accident_insurance
        }
        return annual_bpjs
    #end def
#end class
