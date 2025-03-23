import streamlit as st
import pandas as pd
import time

# Set page configuration
st.set_page_config(page_title="FinTrack: Salary & Tax Analyzer", page_icon="💼", layout="wide")

# Title of the application
st.title("💼 FinTrack: Salary & Tax Analyzer")
# st.image("att.jpg", use_container_width=False, width=600)
# Sidebar content
st.sidebar.header("📊 New vs. Old Tax Regime")
st.sidebar.image("tax.png", caption="Comparison of New vs. Old Tax Regime", use_container_width=True)
st.sidebar.write("### Compare Old vs. New Tax Regime")
st.sidebar.markdown("[Click here to compare tax regimes and savings](https://1finance.co.in/calculator/old-vs-new)", unsafe_allow_html=True)
st.sidebar.write("### Income Tax Calculator - Govt Portal")
st.sidebar.markdown("[Click here to open the Income Tax Calculator](https://incometaxindia.gov.in/pages/tools/tax-calculator.aspx)")

# Main content
st.write("## Enter Your Details")

# Use columns for layout
col1, col2 = st.columns(2)

with col1:
    # User input for Total Fixed Pay
    total_fixed_pay = st.number_input("Enter Total Fixed Pay:", min_value=0, value=123456, step=1000)

with col2:
    # User input for Target CIP Bonus Variable Pay Percentage
    cip_bonus_percentage = st.number_input("Enter Target CIP Bonus Variable Pay %:", min_value=0.0, value=5.0, step=0.1) / 100

# Constants (Derived from the given salary structure)
basic_percentage = 0.50  # 50% of Total Fixed Pay
hra_percentage = 0.50  # 50% of Basic Pay
special_allowance_percentage = 0.2083333
pf_percentage = 0.12  # Provident Fund ~12% of Basic Pay
telephone_reimbursement = 12000  # Fixed amount

# Salary Component Calculations
basic_pay = total_fixed_pay * basic_percentage
annual_basic_pay = basic_pay * 12
hra = basic_pay * hra_percentage
cip_bonus = total_fixed_pay * cip_bonus_percentage
provident_fund = basic_pay * pf_percentage
lta = (annual_basic_pay / 12)
special_allowance = total_fixed_pay * special_allowance_percentage
gratuity1 = round((annual_basic_pay * 15) / (26 * 12))
gratuity = round(gratuity1 / 12)

# Creating a DataFrame to display salary components
data = {
    "Components": [
        "Basic Pay (50% of Total Fixed Pay)",
        "House Rent Allowance (HRA, 50% of Basic)",
        "Special Allowance",
        "Leave Travel Allowance (LTA)",
        "**Total Fixed Pay**",
        f"Target CIP Bonus Variable Pay ({cip_bonus_percentage * 100:.1f}%)",
        "**Total Cash**",
        "Company Provident Fund (12% of Basic)",
        "Telephone Reimbursement",
        "Gratuity",
        "**Cost to Company (CTC)**"
    ],
    "Monthly in INR": [
        round(basic_pay / 12),
        round(hra / 12),
        round(special_allowance / 12),
        round((lta / 12)/12),
        f"**{round(total_fixed_pay / 12)}**",
        "N/A",
        round((total_fixed_pay + cip_bonus) / 12),
        round(provident_fund / 12),
        round(telephone_reimbursement / 12),
        "N/A",
        round((total_fixed_pay  + telephone_reimbursement + provident_fund) / 12),
    ],
    "Annual in INR": [
        round(basic_pay),
        round(hra),
        round(special_allowance),
        round(lta/12),
        f"**{round(total_fixed_pay)}**",
        round(cip_bonus),
        f"**{round(total_fixed_pay + cip_bonus)}**",
        round(provident_fund),
        round(telephone_reimbursement),
        round(gratuity),
        f"**{round(total_fixed_pay + cip_bonus + provident_fund + gratuity + telephone_reimbursement)}**",
    ],
}

# Convert to DataFrame and display
df = pd.DataFrame(data)
st.write("### Salary Breakdown")
st.markdown(df.to_markdown(), unsafe_allow_html=True)

# Deductions section
st.write("### Select Deductions")
with st.expander("Deductions"):
    deduction_options = {
        "Exempted HRA (10(13A))": 0,
        "EPF, PPF, ELSS, School Fees (80C)": 0,
        "Health Insurance Premium (80D)": 0,
        "NPS Contribution - Self (80CCD(1B))": 0,
        "NPS Contribution - Employer (80CCD(2))": 0,
        "Interest on Home Loan (24(b))": 0,
        "Donations (80G)": 0,
        "Leave Travel Allowance (10(5))": 0,
        "Any Other Deduction": 0
    }

    selected_deductions = {}

    for key in deduction_options:
        selected_deductions[key] = st.number_input(f"Enter amount for {key}:", min_value=0, value=0, step=1000)

# Total deductions
total_deductions = sum(selected_deductions.values())
taxable_income_old = total_fixed_pay + cip_bonus - total_deductions - 50000  # Old regime standard deduction
taxable_income_new = total_fixed_pay + cip_bonus - 75000

# Function to calculate tax under different regimes
def calculate_tax(income, slabs):
    tax = 0
    previous_limit = 0

    for limit, rate in slabs:
        if income > limit:
            tax += (limit - previous_limit) * rate  # Tax for the portion within the slab
            previous_limit = limit
        else:
            tax += (income - previous_limit) * rate  # Tax for the remaining income
            break  # Stop as we've taxed the full income
    
    return tax

# Define tax slabs from the image
old_tax_slabs = [(250000, 0), (500000, 0.05), (1000000, 0.2), (float("inf"), 0.3)]
new_tax_slabs = [(400000, 0), (800000, 0.05), (1200000, 0.1), (1600000, 0.15), 
                 (2000000, 0.2), (2400000, 0.25), (float("inf"), 0.3)]

# Example usage
taxable_income_old = max(0, taxable_income_old)  # Ensure non-negative income
taxable_income_new = max(0, taxable_income_new)  # Example value

old_tax = calculate_tax(taxable_income_old, old_tax_slabs)
new_tax = calculate_tax(taxable_income_new, new_tax_slabs)

# Display tax calculation results
if st.button("🔎 Compare Tax Regimes", use_container_width=True):
    st.toast("🔄 Fetching best tax-saving options...", icon="💡")
    time.sleep(2)
# Display tax calculation results
    st.write("### Tax Calculation Results")
    st.write(f"**Tax Under Old Regime:** ₹{old_tax:,.2f}")
    st.write(f"**Tax Under New Regime:** ₹{new_tax:,.2f}")
    tax_savings = old_tax - new_tax
    if tax_savings > 0:
        st.toast(f"✅ You save ₹{tax_savings:,.2f} by choosing the New Regime! 🎉", icon="🎉")
    elif tax_savings < 0:
        st.toast(f"The Old Regime might be better for you, as you pay ₹{-tax_savings:,.2f} less tax.", icon="⚠️")
    else:
        st.toast("Both tax regimes result in the same tax amount.", icon="ℹ️")

# if tax_savings > 0:
#     st.success(f"✅ You save **₹{tax_savings:,.2f}** by choosing the **New Regime**! 🎉")
# elif tax_savings < 0:
#     st.warning(f"⚠️ The **Old Regime** might be better for you, as you pay ₹{-tax_savings:,.2f} less tax.")
# else:
#     st.info("ℹ️ Both tax regimes result in the same tax amount.")




