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
    
    # Consulting Logic
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
# Streamlit UI & Theme
# -----------------------------
st.set_page_config(page_title="Connor Analyst", page_icon="🟢")

# Deloitte Branding via Markdown
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    h1, h2, h3 { color: #000000 !important; font-family: 'Open Sans', sans-serif; }
    .stButton>button { background-color: #86BC25; color: white; border-radius: 0px; border: none; }
    .stButton>button:hover { background-color: #000000; color: #86BC25; }
    /* Chat Styling */
    [data-testid="stChatMessage"] { background-color: #f3f3f3; border-left: 5px solid #86BC25; }
    </style>
    """, unsafe_allow_html=True)

st.title("Connor Analyst 🟢")
st.markdown("**First screening** | *Strategic Deal Assessment*")

if "connor_brain" not in st.session_state:
    st.session_state.connor_brain = FinancialLearner()
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm Connor Analyst. Let's begin the first screening."}]
if "step" not in st.session_state:
    st.session_state.step = 0
if "deal" not in st.session_state:
    st.session_state.deal = {}

# Display Chat
for msg in st.session_state.messages:
    label = "Connor Analyst" if msg["role"] == "assistant" else "Client"
    with st.chat_message(msg["role"]):
        st.write(f"**{label}**")
        st.markdown(msg["content"])
        if "grid" in msg and msg["grid"] is not None:
            st.table(msg["grid"])
        if "chart" in msg and msg["chart"] is not None:
            st.bar_chart(msg["chart"], color="#86BC25") # Deloitte Green
        if "copy_text" in msg:
            with st.expander("📋 Copy Report Data"):
                st.text_area("Plain Text Format", msg["copy_text"], height=150)

# Input logic
if st.session_state.step < len(QUESTIONS):
    if st.session_state.step == 0 and len(st.session_state.messages) == 1:
        st.session_state.messages.append({"role": "assistant", "content": QUESTIONS[0]})
        st.rerun()

    if user_input := st.chat_input("Enter response..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        keys = ["industry", "revenue", "costs", "investment", "expected_return"]
        st.session_state.deal[keys[st.session_state.step]] = user_input
        st.session_state.step += 1
        
        if st.session_state.step < len(QUESTIONS):
            st.session
