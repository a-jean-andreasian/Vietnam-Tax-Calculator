"""
Tax contributed by each full bracket is:

First 5M: 5,000,000 × 5% = 250,000
Next 5M: 5,000,000 × 10% = 500,000
Next 8M: 8,000,000 × 15% = 1,200,000
Next 14M: 14,000,000 × 20% = 2,800,000
Next 20M: 20,000,000 × 25% = 5,000,000
Next 28M: 28,000,000 × 30% = 8,400,000
The rest: 35%
"""

MAX_TAXING_ITERATION = 7  # no more


def calculate_pit(salary_after_deductions: int | float):
    """
    Returns the PIT tax to deduct
    """
    brackets = [
        (10_000_000, 0.05),
        (30_000_000, 0.10),
        (50_000_000, 0.20),
        (100_000_000, 0.30),
        (float('inf'), 0.35),
    ]
    tax = 0
    prev_threshold = 0
    for threshold, rate in brackets:
        if salary_after_deductions <= prev_threshold:
            break
        taxable_in_bracket = min(salary_after_deductions, threshold) - prev_threshold
        tax += taxable_in_bracket * rate
        prev_threshold = threshold
    return tax