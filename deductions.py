PERSONAL_DEDUCTION = 15_500_000
DEPENDENCY_DEDUCTION = 6_200_000


def apply_personal_deduction(salary: int | float):
    return salary - PERSONAL_DEDUCTION

def apply_dependency_deduction(salary: int | float):
    return salary - DEPENDENCY_DEDUCTION

