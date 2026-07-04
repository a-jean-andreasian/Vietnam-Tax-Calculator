from insurance import count_mandatory_social_insurance
from deductions import apply_personal_deduction, apply_dependency_deduction
from pit import calculate_pit
from dataclasses import dataclass


@dataclass
class TaxableInfoResponse:
    insurance: int | float  = None
    taxable_income: int | float = None
    pit_tax: int | float = None
    net: int | float = None
    dependent_deduction: int | float | None = None
    personal_deduction: int | float = None


# -------------------------------
class TaxCounter:
    """
    The order of taxation
    1. MANDATORY_SOCIAL_INSURANCE
    2. PERSONAL_DEDUCTION
    3. DEPENDENCY_DEDUCTION
    4. Taxation
    """

    @classmethod
    def calculate_net(
            cls,
            salary_base: int | float,
            gross_salary: int,
            dependency_deduction_applied: bool,  # for a kid
            personal_deduction_applied=True  # default by the gov of vietnam
    ) -> TaxableInfoResponse:

        response = TaxableInfoResponse()

        insurance = count_mandatory_social_insurance(salary_base=salary_base)
        response.insurance = insurance

        total_gross = gross_salary - insurance  # Salary before tax

        if personal_deduction_applied:
            personal_deduction = apply_personal_deduction(salary=total_gross)
            response.personal_deduction = personal_deduction

            total_gross = personal_deduction

            if total_gross <= 0:
                response.pit_tax = 0
                response.net = total_gross
                return response  # salaries lower than PERSONAL_DEDUCTION are not taxed

        if dependency_deduction_applied:
            dependency_deduction = apply_dependency_deduction(salary=total_gross)
            response.dependent_deduction = dependency_deduction

            if total_gross <= 0:
                response.pit_tax = 0
                response.net = total_gross
                return response  # nothing left to tax

        pit_tax = calculate_pit(salary_after_deductions=total_gross)
        response.pit_tax = pit_tax
        response.net = total_gross - response.net

        return response


if __name__ == '__main__':
    taxCounter = TaxCounter()

    salary_to_test = 64_513_808
    salary_base_to_test = 10_292_208

    response = taxCounter.calculate_net(
        salary_base=salary_base_to_test,
        gross_salary=salary_to_test,
        dependency_deduction_applied=False
    )

    print("Gross:", salary_to_test)
    print("Net:", response.net)
    print("Was taxed:", salary_to_test - response.net)
