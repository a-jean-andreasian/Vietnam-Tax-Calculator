"""
New 5-bracket schedule (monthly taxable income, VND)
Bracket Range Rate
| 1 | 0 – 10,000,000 | 5% |
| 2 | 10,000,000 – 30,000,000 | 10% |
| 3 | 30,000,000 – 50,000,000 | 20% |
| 4 | 50,000,000 – 100,000,000 | 30% |
| 5 | >100,000,000 | 35% |
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import TaxableInfoResponse



def calculate_pit_new(response: "TaxableInfoResponse"):
    """
    Uses static deduction (rumored to be exploited soon)
    """
    brackets = [
        (10_000_000, 5),
        (30_000_000, 10),
        (50_000_000, 20),
        (100_000_000, 30),
        (float('inf'), 35),
    ]

    taxable_income = response.taxable_income

    tax_percent = 0

    for limit, rate in brackets:
        if taxable_income <= limit:
            tax_percent = rate
            break

    response.pit_tax = taxable_income * tax_percent / 100
    response.pit_tax_percent = tax_percent
    response.net -= response.pit_tax

    return response


def calculate_pit_old(response: "TaxableInfoResponse"):
    """
    Uses dynamic deduction (old way)
    """
    brackets = [
        (10_000_000, 0.05),
        (30_000_000, 0.10),
        (50_000_000, 0.20),
        (100_000_000, 0.30),
        (float('inf'), 0.35),
    ]

    taxable_income = response.taxable_income

    tax = 0
    prev_limit = 0
    rate = 0

    for limit, rate in brackets:
        if taxable_income <= prev_limit:
            break

        amount_in_bracket = min(taxable_income, limit) - prev_limit
        tax += amount_in_bracket * rate

        prev_limit = limit

    response.pit_tax = round(tax)
    response.pit_tax_percent = round(rate * 100)
    response.net = round(response.net - response.pit_tax)

    return response
