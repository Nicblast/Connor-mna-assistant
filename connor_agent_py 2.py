import streamlit as st
import numpy as np
import pandas as pd

# -----------------------------
# Connor's brain
# -----------------------------
class FinancialLearner:
    def __init__(self, learning_rate=0.1):
        self.lr = learning_rate
        self.weights = np.array([0.2, 0.4, 0.1])

    def predict(self, features):
        return np.dot(self.weights, features)

    def update_weights(self, features, error):
        gradient = error * features
        self.weights -= self.lr * gradient

# -----------------------------
# Questions & Analysis Logic
# -----------------------------
QUESTIONS = [
    "What industry is this deal in?",
    "What is the expected annual revenue (in €)?",
    "What are the annual costs (in €)?",
    "How much capital needs to be invested (in €)?",
    "What is the expected annual return (%)?"
]

def generate_analysis_grid(deal, score):
    rev = float(str(deal.get("revenue", 0)).replace(',', ''))
    cost = float(str(deal.get("costs", 0)).replace(',', ''))
    inv = float(str(deal.get("investment", 1)).replace(',', ''))
    
    # Intelligence logic
    if score >= 0.7:
        risk, action = "Low - Execution focus", "Proceed to Due Diligence"
        alt_sol, alts = "Equity structure to scale", "Expansion into adjacent markets"
    elif score >= 0.4:
        risk, action = "Medium - Margin pressure", "Renegotiate operational costs"
        alt_sol, alts = "Phased funding rounds", "Joint Venture partnership"
    else:
        risk, action = "High - Financial instability", "Immediate Exit / Decline"
        alt_sol, alts = "Debt restructuring", "Pivot business model"

    # Add advanced consulting metrics
    ebitda_margin = ((rev - cost) / rev * 100) if rev > 0 else 0
    payback_period = inv / (rev - cost) if (rev - cost) > 0 else float('inf')

    grid_data = {
        "Consulting Metric": [
            "Revenue", "Costs", "Net Profit", "EBITDA Margin", 
            "Est. Payback (Years)", "Risk Profile", 
            "Best Course of Action", "Alternative Solutions"
        ],
        "Details": [
            f"€{rev:,.2f}", f"€{cost:,.2f}", f"€{(rev-cost):,.2f}", 
            f"{ebitda_margin:.1f}%", f"{payback_period:.1f} yrs",
            risk, action, alt_sol
        ]
    }
    return pd.DataFrame(grid_data)

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Connor Analyst", page_icon="📈")
st.title("Connor Analyst")
st.markdown("#### First screening")

if "connor_brain" not in st.session_state:
    st.session_state.connor_brain = FinancialLearner()
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm Connor Analyst. Let's begin the first screening."}]
if "step" not in st.session_state:
    st.session_state.step = 0
if "deal" not in st.session_state:
    st.session_state.deal = {}

# Display Chat History
for msg in st.session_state.messages:
    label = "Connor Analyst" if msg["role"] == "assistant" else "You"
    with st.chat_message(msg["role"]):
        st.write(f"**{label}**")
        st.markdown(msg["content"])
        if "grid" in msg and msg["grid"] is not None:
            st.table(msg["grid"])
        if "chart_data" in msg and msg["chart_data"] is not None:
            st.bar_chart(msg["chart_data"])
        # Copy-Paste Section
        if "copy_text" in msg:
            with st.expander("📋 Click to Copy Result"):
                st.text_area("Label: Analysis Summary", msg["copy_text"], height=200)

# Input logic
if st.session_state.step < len(QUESTIONS):
    if st.session_state.step == 0 and len(st.session_state.messages) == 1:
        st.session_state.messages.append({"role": "assistant", "content": QUESTIONS[0]})
        st.rerun()

    if user_input := st.chat_input("Enter your answer..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        keys = ["industry", "revenue", "costs", "investment", "expected_return"]
        st.session_state.deal[keys[st.session_state.step]] = user_input
        st.session_state.step += 1
        
        if st.session_state.step < len(QUESTIONS):
            st.session_state.messages.append({"role": "assistant", "content": QUESTIONS[st.session_state.step]})
        else:
            try:
                # Calculations
                rev_v = float(str(st.session_state.deal.get("revenue")).replace(',', ''))
                cost_v = float(str(st.session_state.deal.get("costs")).replace(',', ''))
                inv_v = float(str(st.session_state.deal.get("investment")).replace(',', ''))
                ret_v = float(str(st.session_state.deal.get("expected_return")).replace(',', ''))
                
                margin = (rev_v - cost_v) / rev_v if rev_v > 0 else 0
                roi = (rev_v - cost_v) / inv_v if inv_v > 0 else 0
                score = st.session_state.connor_brain.predict(np.array([margin, roi, ret_v / 100]))
                
                df_grid = generate_analysis_grid(st.session_state.deal, score)
                
                # Format text for easy copy-pasting
                copy_str = f"CONNOR ANALYST - FIRST SCREENING REPORT\n"
                copy_str += f"Industry: {st.session_state.deal['industry']}\n"
                copy_str += f"Deal Score: {score:.3f}\n"
                copy_str += "-"*30 + "\n"
                for index, row in df_grid.iterrows():
                    copy_str += f"{row['Consulting Metric']}: {row['Details']}\n"

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"**Screening complete for {st.session_state.deal['industry']}.**",
                    "grid": df_grid,
                    "chart_data": pd.DataFrame({"€": [rev_v, cost_v, rev_v-cost_v]}, index=["Rev", "Cost", "Profit"]),
                    "copy_text": copy_str
                })
            except:
                st.session_state.messages.append({"role": "assistant", "content": "Error processing data. Use numbers only."})
        st.rerun()
else:
    if st.button("New Screening"):
        st.session_state.step = 0
        st.session_state.deal = {}
        st.session_state.messages = [{"role": "assistant", "content": "Ready. " + QUESTIONS[0]}]
        st.rerun()
