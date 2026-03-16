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
    
    # Logical assessments based on performance
    if score >= 0.7:
        risk, action = "Low - Execution focus", "Proceed to Due Diligence"
        alt_sol, alts = "Equity structure to scale", "Expansion into adjacent markets"
    elif score >= 0.4:
        risk, action = "Medium - Margin pressure", "Renegotiate operational costs"
        alt_sol, alts = "Phased funding rounds", "Joint Venture partnership"
    else:
        risk, action = "High - Financial instability", "Immediate Exit / Decline"
        alt_sol, alts = "Debt restructuring", "Pivot business model"

    grid_data = {
        "Analysis Point": [
            "Revenue", "Costs", "Net Profit", 
            "Risk Profile", "Best Course of Action", 
            "Alternative Solutions", "Alternatives"
        ],
        "Details": [
            f"€{rev:,.2f}", 
            f"€{cost:,.2f}", 
            f"€{(rev-cost):,.2f}",
            risk, action, alt_sol, alts
        ]
    }
    return pd.DataFrame(grid_data)

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Connor Analyst", page_icon="📈", layout="centered")

# Branding
st.title("Connor Analyst")
st.markdown("#### First screening")

# Initialize Session States
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
        
        # Display Grid if it exists
        if "grid" in msg and msg["grid"] is not None:
            st.table(msg["grid"])
        
        # Display Charts if they exist
        if "chart_data" in msg and msg["chart_data"] is not None:
            st.bar_chart(msg["chart_data"])

# Handle Conversation
if st.session_state.step < len(QUESTIONS):
    # Auto-prompt the first question
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
            # --- FINAL ANALYSIS BLOCK ---
            try:
                # Math conversions
                rev_v = float(str(st.session_state.deal.get("revenue")).replace(',', ''))
                cost_v = float(str(st.session_state.deal.get("costs")).replace(',', ''))
                inv_v = float(str(st.session_state.deal.get("investment")).replace(',', ''))
                ret_v = float(str(st.session_state.deal.get("expected_return")).replace(',', ''))
                
                profit = rev_v - cost_v
                margin = profit / rev_v if rev_v > 0 else 0
                roi = profit / inv_v if inv_v > 0 else 0
                
                # Connor's Prediction
                features = np.array([margin, roi, ret_v / 100])
                score = st.session_state.connor_brain.predict(features)
                
                # Visual Data preparation
                chart_df = pd.DataFrame({
                    "Financials": ["Revenue", "Costs", "Profit"],
                    "Amount (€)": [rev_v, cost_v, profit]
                }).set_index("Financials")

                df_grid = generate_analysis_grid(st.session_state.deal, score)
                
                # Build the response with metrics and visuals
                summary_text = f"""
### Analysis Complete for {st.session_state.deal['industry']}
**Connor's Final Score:** `{score:.3f}`

---
"""
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": summary_text,
                    "grid": df_grid,
                    "chart_data": chart_df
                })
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": "I couldn't calculate that. Please ensure you enter numbers without symbols."
                })
        
        st.rerun()
else:
    if st.button("Start New Screening"):
        st.session_state.step = 0
        st.session_state.deal = {}
        st.session_state.messages = [{"role": "assistant", "content": "Ready for a new first screening. " + QUESTIONS[0]}]
        st.rerun()
