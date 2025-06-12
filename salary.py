import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
from dotenv import load_dotenv
import os

# Set page configuration
st.set_page_config(page_title="FinTrack: Salary & Tax Analyzer", page_icon="💼", layout="wide")
marquee_html = """
<div style="position:fixed; top:0; left:0; width:100%; background-color:#ffcc00; padding:10px 0; z-index:9999; text-align:center;">
    <p id="marqueeText" style="display:inline-block; font-size:18px; font-weight:bold; white-space: nowrap;">
       📢 New Tax Regime 2025: Lower Taxes, Bigger Savings! 🚀  
    💰 Slabs: ₹0-4L (0%) | ₹4L-8L (5%) | ₹8L-12L (10%) | ₹12L-16L (15%) | ₹16L-20L (20%) | ₹20L-24L (25%) | ₹24L+ (30%) 💼  
🔍 Compare & Optimize Your Tax! Check Now! 📊  
    </p>
</div>

<script>
function animateMarquee() {
    let text = document.getElementById("marqueeText");
    let screenWidth = window.innerWidth;
    let textWidth = text.offsetWidth;
    let startPos = screenWidth;
    let endPos = -textWidth;
    let currentPos = startPos;

    function step() {
        if (currentPos <= endPos) {
            currentPos = startPos;
        } else {
            currentPos -= 2;
        }
        text.style.transform = "translateX(" + currentPos + "px)";
        requestAnimationFrame(step);
    }
    step();
}
animateMarquee();
</script>
"""

# Inject Marquee into Streamlit
st.components.v1.html(marquee_html, height=50)

# ✅ Add spacing below marquee to prevent overlap with content
st.markdown(
    """
    <style>
    h1 {
        margin-top: -20px; /* Adjust this value to reduce space */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Title of the application
st.title("🧾 FinTrack: Salary & Tax Analyzer")
st.caption("Developed by **Jagaputhran S** 👨‍💻")
# st.image("att.jpg", use_container_width=False, width=600)

st.sidebar.markdown(
    """
    <div style="background-color:#ffcc00; padding:10px; border-radius:10px; text-align:center; font-weight:bold;">
        ⚖️ Compare New vs. Old Tax Regime & Save More!
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.image("tax.png", caption="🔍 Tax Regime Comparison", use_container_width=True)

st.sidebar.markdown(
    """
    <div style="padding:8px; background-color:#ffcc00; border-radius:8px;">
        💰 Want to maximize your savings? Compare the old and new tax regimes now!
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("[🟢 Additional External link for comparison ](https://1finance.co.in/calculator/old-vs-new)", unsafe_allow_html=True)



# 🏛 Income Tax Calculator (Govt. Portal)
st.sidebar.write("### 🏛 Income Tax Calculator - Govt Portal")


st.sidebar.markdown("[🔵 Open the Govt. Income Tax Calculator](https://incometaxindia.gov.in/pages/tools/tax-calculator.aspx)", unsafe_allow_html=True)

# Main content
st.write("## Enter Your Details")

# Use columns for layout
col1, col2 = st.columns(2)

with col1:
    # User input for Total Fixed Pay
    total_fixed_pay = st.number_input("Enter Total Fixed Pay:", min_value=0, value=0, step=1000)

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
        "🏦 **Basic Pay** (50% of Total Fixed Pay)",
        "🏡 **House Rent Allowance (HRA)** (50% of Basic)",
        "🎁 **Special Allowance**",
        "🛫**Leave Travel Allowance (LTA)**",
        "💰 **Total Fixed Pay**",
        f"🎯 **Target CIP Bonus Variable Pay** ({cip_bonus_percentage * 100:.1f}%)",
        "💵 **Total Cash**",
        "🏛️ Company Provident Fund (12% of Basic)",
        "📞 **Telephone Reimbursement**",
        "📜  **Gratuity**",
        "💼 **Cost to Company (CTC)**"
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
def calculate_tax(income, slabs, new_regime=False):
    tax = 0
    previous_limit = 0

    for limit, rate in slabs:
        if income > limit:
            tax += (limit - previous_limit) * rate  # Tax for the portion within the slab
            previous_limit = limit
        else:
            tax += (income - previous_limit) * rate  # Tax for the remaining income
            break  # Stop as we've taxed the full income
    if new_regime and income <= 1200000:
        return 0  # Full rebate under Section 87A
    return tax

# Define tax slabs from the image
old_tax_slabs = [(250000, 0), (500000, 0.05), (1000000, 0.2), (float("inf"), 0.3)]
new_tax_slabs = [(400000, 0), (800000, 0.05), (1200000, 0.1), (1600000, 0.15), 
                 (2000000, 0.2), (2400000, 0.25), (float("inf"), 0.3)]

# Example usage
taxable_income_old = max(0, taxable_income_old)  # Ensure non-negative income
taxable_income_new = max(0, taxable_income_new)  # Example value

old_tax = calculate_tax(taxable_income_old, old_tax_slabs)
new_tax = calculate_tax(taxable_income_new, new_tax_slabs, new_regime=True)

old_tax_final = old_tax + (old_tax * 0.04)
new_tax_final = new_tax + (new_tax * 0.04)

if st.button("🔎 Compare Tax Regimes", use_container_width=True):
    st.toast("🔄 Fetching best tax-saving options...", icon="💡")
    time.sleep(2)
# Display tax calculation results
    st.write("### Tax Calculation Results")
    col6, col7 = st.columns(2)
    with col6:
        st.metric(label="📜 **Tax (Old Regime)**", value=f"₹{old_tax_final:,.2f}")
    with col7:
        st.metric(label="📄 **Tax (New Regime)**", value=f"₹{new_tax_final:,.2f}")
    tax_savings = old_tax_final - new_tax_final
    tax_savings_percentage = (tax_savings / old_tax_final * 100) if old_tax_final > 0 else 0

    # Show tax savings using st.metric
    if tax_savings > 0:
        st.toast(f"✅ You save ₹{tax_savings:,.2f} by choosing the New Regime! 🎉", icon="🎉")
        col8 = st.columns(1)  # Single column for emphasis
        with col8[0]:
            st.metric(label="📉 **Tax Savings**", value=f"₹{round(tax_savings):,}", delta=f"{tax_savings_percentage:.2f}% 💰")
    elif tax_savings < 0:
        st.toast(f"⚠️ The Old Regime might be better, as you pay ₹{-tax_savings:,.2f} less tax.", icon="⚠️")
        col8 = st.columns(1)
        with col8[0]:
            st.metric(label="📈 **Additional Tax Paid**", value=f"₹{round(-tax_savings):,}", delta=f"{-tax_savings_percentage:.2f}% 🔺", delta_color="inverse")
    else:
        st.toast("ℹ️ Both tax regimes result in the same tax amount.", icon="ℹ️")
        col8 = st.columns(1)
        with col8[0]:
            st.metric(label="📊 **No Difference in Tax**", value="₹0", delta="0.00%")

    fig = go.Figure()
    fig.add_trace(go.Bar(x=["Old Regime", "New Regime"], 
                        y=[old_tax_final, new_tax_final], 
                        text=[f"₹{old_tax_final:,.2f}", f"₹{new_tax_final:,.2f}"],
                        textposition="auto",
                        marker_color=["red", "green"]))  # Red for higher tax, Green for savings
    fig.add_shape(
    type="line",
    x0="Old Regime", y0=old_tax_final,
    x1="New Regime", y1=new_tax_final,
    line=dict(color="blue", width=3, dash="dashdot")  # Blue dashed line
)

# Add an annotation to show the savings difference
    fig.add_annotation(
        x="New Regime",
        y=(old_tax_final + new_tax_final) / 2,  # Mid-point
        text=f"💰 Savings: ₹{tax_savings:,.2f}",
        showarrow=False,
        arrowhead=2,
        ax=-50,  # Adjust arrow positioning
        ay=40,
        font=dict(size=14, color="black"),
        bgcolor="lightyellow",
        bordercolor="black"
    )
    fig.update_layout(
        title="Visualize tax comparison!!",
        xaxis_title="Tax Regime",
        yaxis_title="Tax Amount (INR)",
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)


import google.generativeai as genai
from streamlit_chat import message

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text

# === Floating Chat Button and Popup Chat Window ===
# Add custom CSS and JS for floating button
st.markdown('''
<style>
#fintrack-chat-btn {
    position: fixed;
    bottom: 40px;
    right: 40px;
    z-index: 10000;
    width: 64px;
    height: 64px;
    background: #ffcc00;
    border-radius: 50%;
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border: 3px solid #fff;
    transition: box-shadow 0.2s;
}
#fintrack-chat-btn:hover {
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}
#fintrack-chat-popup {
    position: fixed;
    bottom: 120px;
    right: 40px;
    width: 350px;
    max-width: 90vw;
    background: #fffbe6;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    z-index: 10001;
    padding: 16px 12px 12px 12px;
    border: 2px solid #ffcc00;
    display: none;
}
#fintrack-chat-popup.active {
    display: block;
}
#fintrack-chat-popup .close-btn {
    position: absolute;
    top: 8px;
    right: 16px;
    font-size: 22px;
    color: #888;
    cursor: pointer;
}
</style>
<div id="fintrack-chat-btn" onclick="document.getElementById('fintrack-chat-popup').classList.toggle('active')">
    <span style="font-size:32px;">💬</span>
</div>
<div id="fintrack-chat-popup">
    <span class="close-btn" onclick="document.getElementById('fintrack-chat-popup').classList.remove('active')">&times;</span>
    <div id="fintrack-chat-streamlit"></div>
</div>
<script>
// Ensure popup closes if user clicks outside
window.addEventListener('click', function(e) {
    var popup = document.getElementById('fintrack-chat-popup');
    var btn = document.getElementById('fintrack-chat-btn');
    if (popup.classList.contains('active') && !popup.contains(e.target) && !btn.contains(e.target)) {
        popup.classList.remove('active');
    }
});
</script>
''', unsafe_allow_html=True)

# Use session state to control chat popup visibility
if "show_chat_popup" not in st.session_state:
    st.session_state["show_chat_popup"] = False

# Use a Streamlit container to render chat UI inside the popup
with st.container():
    # This container will be injected into the popup via JS/CSS
    st.markdown('<div id="fintrack-chat-streamlit-anchor"></div>', unsafe_allow_html=True)
    if st.session_state.get("show_chat_popup", False):
        st.markdown("<style>#fintrack-chat-popup{display:block!important;}</style>", unsafe_allow_html=True)
        st.markdown("<style>#fintrack-chat-btn{display:none!important;}</style>", unsafe_allow_html=True)
        # Chat UI
        st.write("### 💬 Chat with FinTrack Bot")
        if "messages" not in st.session_state:
            st.session_state["messages"] = []
        for msg in st.session_state["messages"]:
            message(msg["content"], is_user=(msg["role"] == "user"))
        user_input = st.text_input("You:", key="user_input", value="", placeholder="Type your message and press Enter...")
        if user_input:
            bot_response = get_gemini_response(user_input)
            st.session_state["messages"].append({"role": "user", "content": user_input})
            st.session_state["messages"].append({"role": "bot", "content": bot_response})
            st.experimental_rerun()

# === Place Chat Bot in Expander at Bottom 2 ===
# with st.expander("💬 Chat with FinTrack Bot", expanded=True):
#     if "messages" not in st.session_state:
#         st.session_state["messages"] = []
#     # Display all previous messages
#     for msg in st.session_state["messages"]:
#         message(msg["content"], is_user=(msg["role"] == "user"))
#     # Place input at the bottom, and clear after sending
#     user_input = st.text_input("You:", key="user_input", value="", placeholder="Type your message and press Enter...")
#     if user_input:
#         bot_response = get_gemini_response(user_input)
#         st.session_state["messages"].append({"role": "user", "content": user_input})
#         st.session_state["messages"].append({"role": "bot", "content": bot_response})
#         st.experimental_rerun()  # Refresh to clear input and show new messages
# === Place Chat Bot in Expander at Bottom ===
# with st.expander("💬 Chat with FinTrack Bot", expanded=True):
#     if "messages" not in st.session_state:
#         st.session_state["messages"] = []
#     user_input = st.text_input("You:", key="user_input")
#     if user_input:
#         bot_response = get_gemini_response(user_input)
#         st.session_state["messages"].append({"role": "user", "content": user_input})
#         st.session_state["messages"].append({"role": "bot", "content": bot_response})
#     for msg in st.session_state["messages"]:
#         message(msg["content"], is_user=(msg["role"] == "user"))
