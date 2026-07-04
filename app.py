import streamlit as st
from main import TaxCounter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import TaxableInfoResponse

TAX_COUNTER = TaxCounter()

st.title("Vietnam PIT Calculator")

gross = st.number_input(
    "Gross salary (VND)",
    min_value=0,
    value=0,
    step=1_000_000
)

base = st.number_input(
    "Base salary (VND, insurance base)",
    min_value=0,
    value=0,
    step=1_000_000
)

is_vietnamese = st.checkbox(
    "Vietnamese employee",
    value=True
)

apply_personal = st.checkbox(
    "Apply personal deduction (15.5M)",
    value=True
)

apply_dependents = st.checkbox(
    "Apply dependents deduction (6.2M)",
    value=False
)

dependents = 0  # preventing NameError: name 'dependents' is not defined
if apply_dependents:
    with st.expander("Dependents settings", expanded=True):
        dependents = st.number_input(
            "Children claimed as dependents",
            min_value=1,
            value=1,
            step=1
        )

if st.button("Calculate"):
    response: "TaxableInfoResponse" = TAX_COUNTER.calculate_net(
        salary_base=base,
        gross_salary=gross,
        dependency_deduction_applied=apply_dependents,
        number_of_children_to_apply_deduction=dependents,
        is_vietnamese=is_vietnamese,
        personal_deduction_applied=apply_personal
    )

    st.subheader("Results")

    st.write(
        f"Compulsory insurance: "
        f"{response.insurance:,.0f} VND"
    )

    if response.personal_deduction:
        st.write(
            f"Tax saved from personal deduction: "
            f"{response.personal_deduction:,.0f} VND"
        )

    if response.dependent_deduction:
        st.write(
            f"Tax saved from child deduction: "
            f"{response.dependent_deduction:,.0f} VND"
        )

    st.write(
        f"Taxable income: "
        f"{response.taxable_income:,.0f} VND"
    )

    st.write(
        f"PIT: "
        f"{response.pit_tax:,.0f} VND"
    )

    st.write(
        f"Effective tax bracket: "
        f"{response.pit_tax_percent if response.pit_tax_percent else 0}%"
    )

    st.success(
        f"Net salary: {response.net:,.0f} VND\n\n"
        f"Expenses applied: {response.pit_tax + response.insurance:,.0f} VND"
    )
