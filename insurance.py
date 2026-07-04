"""
According to Vietnamese law, the employee-side compulsory contribution is generally:

    Mandatory insurance = Social Insurance (SI) + Health Insurance (HI) + Unemployment Insurance (UI)

    Employee rates:
        SI = 8%
        HI = 1.5%
        UI = 1%

    Total = 10.5%
"""


def count_mandatory_social_insurance(salary_base):
    social_insurance = salary_base * 8 // 100
    health_insurance = salary_base * 15 // 1000
    # unemployment_insurance = salary_base * 1 // 100

    employee_insurance = (
            social_insurance
            + health_insurance
        # + unemployment_insurance  in case of foreigners Unemployment Insurance (UI) is not applied
    )

    return employee_insurance
