import streamlit as st
from main import TaxCounter
from typing import TYPE_CHECKING
from PIL import Image
import base64

if TYPE_CHECKING:
    from main import TaxableInfoResponse

TAX_COUNTER = TaxCounter()


def set_page_styling():
    with open("bin/background.png", "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{data}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
    
        /* Global page text */
        .stApp,
        p,
        label,
        h1,h2,h3,h4,h5,h6 {
            color: black !important;
        }
    
        /* Buttons */
        .stButton > button {
            background-color: #1e1e2f !important;
            color: white !important;
            border: none !important;
        }
    
        .stButton > button p {
            color: white !important;
        }
    
        /* Number input field */
        .stNumberInput input {
            color: white !important;
            -webkit-text-fill-color: white !important;
        }
    
        /* +/- buttons */
        .stNumberInput button {
            color: white !important;
        }
    
        /* Expander header */
        .streamlit-expanderHeader p {
            color: white !important;
        }
    
        /* Checkbox labels */
        .stCheckbox p {
            color: black !important;
        }
    
        /* Selectbox */
        div[data-baseweb="select"] * {
            color: white !important;
        }
    
        </style>
        """,
        unsafe_allow_html=True
    )

    st.set_page_config(
        page_title="Vietnam PIT Calculator",
        page_icon=Image.open("bin/icon.png"),
        layout="centered"
    )


set_page_styling()

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
    to_write = list()

    to_write.append(f"**Compulsory insurance:** {response.insurance:,.0f} VND\n\n")

    to_write.append(f"**Taxable income:** {response.taxable_income:,.0f} VND\n\n")
    to_write.append(f"**PIT:** {response.pit_tax:,.0f} VND\n\n")

    to_write.append(f"**Effective tax bracket:** {response.pit_tax_percent if response.pit_tax_percent else 0}%\n\n")

    to_write.append(f"**Net salary:** {response.net:,.0f} VND\n\n")

    if response.personal_deduction:
        to_write.append(f"**Tax saved from personal deduction:** {response.personal_deduction:,.0f} VND\n\n")

    if response.dependent_deduction:
        to_write.append(f"**Tax saved from child deduction:** {response.dependent_deduction:,.0f} VND\n\n")

    to_write.append(f"**Expenses applied:** {response.pit_tax + response.insurance:,.0f} VND\n\n")


    st.success(
        "".join(to_write)
    )
