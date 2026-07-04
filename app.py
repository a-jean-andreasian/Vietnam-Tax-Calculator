import streamlit as st
from main import TaxCounter

st.title("Vietnam PIT Calculator")

gross = st.number_input("Gross salary (VND)", min_value=0, value=0, step=1_000_000)
base = st.number_input("Base salary (VND, for insurance cap)", min_value=0, value=0, step=1_000_000)
dependents = st.number_input("Number of dependents", min_value=0, value=0, step=1)

TAX_COUNTER = TaxCounter()


if st.button("Calculate"):
    net = TAX_COUNTER.calculate_net(
        salary_base=base,
        dependency_deduction_applied=dependents,
        personal_deduction_applied=True
    )

    st.write(f"Insurance: {insurance:,.0f} VND")
    st.write(f"Taxable income: {salary_after_deductions:,.0f} VND")
    st.write(f"PIT: {pit:,.0f} VND")
    st.write(f"**Net salary: {net:,.0f} VND**")
