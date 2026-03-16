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
# Questions & Logic
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
    
    if score >= 0.7:
        risk, action = "Low - Execution focus", "Proceed to Due Diligence"
        alt_sol = "Equity structure to scale"
    elif score >= 0.4:
        risk, action = "Medium - Margin pressure", "Renegotiate operational costs"
        alt_sol = "Phased funding rounds"
    else:
        risk, action = "High - Financial instability", "Immediate Exit / Decline"
        alt_sol = "Debt restructuring"

    ebitda_margin = ((rev - cost) / rev * 100) if rev > 0 else 0
    payback = inv / (rev - cost) if (rev - cost) > 0 else 0

    grid_data = {
        "Strategic Metric": ["Revenue", "Costs", "Net Profit", "EBITDA Margin", "Payback Period", "Risk Profile", "Recommended Action", "Alternative"],
        "Value/Insight": [f"€{rev:,.2f}", f"€{cost:,.2f}", f"€{(rev-cost):,.2f}", f"{ebitda_margin:.1f}%", f"{payback:.1f} Years", risk, action, alt_sol]
    }
    return pd.DataFrame(grid_data)

# -----------------------------
# UI & Midnight Style
# -----------------------------
st.set_page_config(page_title="Connor Analyst", page_icon="")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, h4, p, span, label { color: #ffffff !important; }
    .stButton>button { background-color: #86BC25; color: black !important; font-weight: bold; }
    [data-testid="stChatMessage"] { background-color: #1a1a1a; border-left: 5px solid #86BC25; }
    </style>
    """, unsafe_allow_html=True)

st.title("Connor Analyst")
st.markdown("#### First screening")

if "connor_brain" not in st.session_state:
    st.session_state.connor_brain = FinancialLearner()
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm Connor Analyst. Let's begin."}]
if "step" not in st.session_state:
    st.session_state.step = 0
if "deal" not in st.session_state:
    st.session_state.deal = {}

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "grid" in msg and msg["grid"] is not None:
            st.table(msg["grid"])
        # FIXED: Ensure chart data is a DataFrame
        if "chart_data" in msg:
            st.bar_chart(msg["chart_data"])
        if "copy_text" in msg:
            with st.expander("📋 Copy Report Data"):
                st.text_area("Plain Text", msg["copy_text"], height=150)

if st.session_state.step < len(QUESTIONS):
    if st.session_state.step == 0 and len(st.session_state.messages) == 1:
        st.session_state.messages.append({"role": "assistant", "content": QUESTIONS[0]})
        st.rerun()

    if user_input := st.chat_input("Provide data..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        keys = ["industry", "revenue", "costs", "investment", "expected_return"]
        st.session_state.deal[keys[st.session_state.step]] = user_input
        st.session_state.step += 1
        
        if st.session_state.step < len(QUESTIONS):
            st.session_state.messages.append({"role": "assistant", "content": QUESTIONS[st.session_state.step]})
        else:
            try:
                r = float(str(st.session_state.deal.get("revenue")).replace(',', ''))
                c = float(str(st.session_state.deal.get("costs")).replace(',', ''))
                i = float(str(st.session_state.deal.get("investment")).replace(',', ''))
                rt = float(str(st.session_state.deal.get("expected_return")).replace(',', ''))
                
                score = st.session_state.connor_brain.predict(np.array([(r-c)/r, (r-c)/i, rt/100]))
                df_grid = generate_analysis_grid(st.session_state.deal, score)
                
                # FIXED: Data structure for bar chart
                df_chart = pd.DataFrame({"Value": [r, c, r-c]}, index=["Revenue", "Costs", "Profit"])
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"**Analysis complete.** Score: `{score:.3f}`",
                    "grid": df_grid,
                    "chart_data": df_chart, # Pass the DF directly
                    "copy_text": "Analysis Report..."
                })
            except Exception as e:
                st.error(f"Error: {e}")
        st.rerun()
