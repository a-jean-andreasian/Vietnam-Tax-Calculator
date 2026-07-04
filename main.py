from insurance import count_mandatory_social_insurance
from deductions import apply_personal_deduction, apply_dependency_deduction
from pit import calculate_pit_old
from dataclasses import dataclass


@dataclass
class TaxableInfoResponse:
    salary_base: int | float = None
    gross_salary: int | float = None
    insurance: int | float = None
    taxable_income: int | float = None
    pit_tax_percent: int | float = None
    pit_tax: int | float = None
    net: int | float = None
    dependent_deduction: int | float | None = None
    personal_deduction: int | float = None

    def to_dict(self):
        return {
            "salary_base": self.salary_base,
            "gross_salary": self.gross_salary,
            "insurance": self.insurance,
            "taxable_income": self.taxable_income,
            "pit_tax_percent": self.pit_tax_percent,
            "pit_tax": self.pit_tax,
            "net": self.net,
            "dependent_deduction": self.dependent_deduction,
            "personal_deduction": self.personal_deduction
        }


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
        is_vietnamese: bool = False,
        personal_deduction_applied=True,  # default by the gov of vietnam,
        number_of_children_to_apply_deduction: int = 0

    ) -> TaxableInfoResponse:

        response = TaxableInfoResponse()
        response.salary_base = salary_base
        response.gross_salary = gross_salary

        response: TaxableInfoResponse = count_mandatory_social_insurance(response=response, is_vietnamese=is_vietnamese)

        if personal_deduction_applied:
            response: TaxableInfoResponse = apply_personal_deduction(response=response)

            if response.taxable_income == 0:
                return response

        if dependency_deduction_applied:
            response: TaxableInfoResponse = apply_dependency_deduction(
                response=response,
                number_of_children_to_apply_deduction=number_of_children_to_apply_deduction
            )

            if response.taxable_income == 0:
                return response

        response = calculate_pit_old(response=response)
        return cls.enrich_metadata(response=response)

    @staticmethod
    def enrich_metadata(response: TaxableInfoResponse):
        tax_rate = response.pit_tax_percent / 100

        if response.personal_deduction:
            response.personal_deduction = round(
                response.personal_deduction * tax_rate
            )

        if response.dependent_deduction:
            response.dependent_deduction = round(
                response.dependent_deduction * tax_rate
            )

        return response


if __name__ == '__main__':
    taxCounter = TaxCounter()

    salary_to_test = 64_513_808
    salary_base_to_test = 10_292_208

    response = taxCounter.calculate_net(
        salary_base=salary_base_to_test,
        gross_salary=salary_to_test,
        dependency_deduction_applied=True,
        is_vietnamese=True,
        number_of_children_to_apply_deduction=1
    )

    import pprint

    pprint.pprint(response.to_dict())
