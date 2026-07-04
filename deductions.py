from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main import TaxableInfoResponse

PERSONAL_DEDUCTION = 15_500_000
DEPENDENCY_DEDUCTION = 6_200_000


def apply_personal_deduction(response: "TaxableInfoResponse"):
    taxable_income = response.taxable_income
    response.taxable_income -= PERSONAL_DEDUCTION

    if response.taxable_income <= 0:
        response.pit_tax = 0
        response.taxable_income = 0
        response.personal_deduction = response.taxable_income

    response.personal_deduction = taxable_income - response.taxable_income
    return response



def apply_dependency_deduction(response: "TaxableInfoResponse", number_of_children_to_apply_deduction: int = 0):
    """
    Applied if the employee has a child < 18 y.o. and the salary is lower than 15.5 million VND
    """
    taxable_income = response.taxable_income
    if taxable_income < 15_500_000:
        response.pit_tax = 0
        response.taxable_income = 0
        response.dependent_deduction = 0
        return response

    to_deduct = DEPENDENCY_DEDUCTION * number_of_children_to_apply_deduction
    response.dependent_deduction = to_deduct
    taxable_income -= to_deduct

    if taxable_income <= 0:
        response.pit_tax = 0
        response.taxable_income = 0
        return response

    response.taxable_income = taxable_income
    return response
