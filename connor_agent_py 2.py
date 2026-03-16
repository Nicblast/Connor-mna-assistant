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
    # Data extraction with safety defaults
    rev = float(str(deal.get("revenue", 0)).replace(',', ''))
    cost = float(str(deal.get("costs", 0)).replace(',', ''))
    
    # Intelligence logic for the grid
    if score >= 0.7:
        risk, action = "Low - Execution focus", "Proceed to Due Diligence"
        alt_sol, alts = "Equity structure", "Market expansion"
    elif score >= 0.4:
        risk, action = "Medium - Margin pressure", "Renegotiate terms"
        alt_sol, alts = "Phased funding", "Joint Venture"
    else:
        risk, action = "High - Financial instability", "Exit/Decline"
        alt_sol, alts = "Debt restructuring", "Operational pivot"

    grid_data = {
        "Analysis Point": ["Revenue", "Costs", "Net Profit", "Risk Profile", "Best Course of Action", "Alternative Solutions", "Alternatives"],
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
st.set_page_config(page_title="Connor Analyst", page_icon="📈")
st.title("Connor Analyst")
st.markdown("### First screening")

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
        # FIX: Check if grid exists and is not None before trying to display
        if "grid" in msg and msg["grid"] is not None:
            st.table(msg["grid"])

# Handle Conversation
if st.session_state.step < len(QUESTIONS):
    # Auto-prompt the first question
    if st.session_state.step == 0 and len(st.session_state.messages) == 1:
        st.session_state.messages.append({"role": "assistant", "content": QUESTIONS[0]})
        st.rerun()

    if user_input := st.chat_input("Enter your answer..."):
        # Save user response
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Map input to deal data
        keys = ["industry", "revenue", "costs", "investment", "expected_return"]
        st.session_state.deal[keys[st.session_state.step]] = user_input
        st.session_state.step += 1
        
        if st.session_state.step < len(QUESTIONS):
            # Ask next question
            st.session_state.messages.append({"role": "assistant", "content": QUESTIONS[st.session_state.step]})
        else:
            # Final Analysis
            try:
                # Math calculations
                rev_val = float(str(st.session_state.deal.get("revenue")).replace(',', ''))
                cost_val = float(str(st.session_state.deal.get("costs")).replace(',', ''))
                inv_val = float(str(st.session_state.deal.get("investment")).replace(',', ''))
                ret_val = float(str(st.session_state.deal.get("expected_return")).replace(',', ''))
                
                margin = (rev_val - cost_val) / rev_val if rev_val > 0 else 0
                roi = (rev_val - cost_val) / inv_val if inv_val > 0 else 0
                
                # Predict score
                features = np.array([margin, roi, ret_val / 100])
                score = st.session_state.connor_brain.predict(features)
                
                # Generate Grid
                df_results = generate_analysis_grid(st.session_state.deal, score)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"**First screening complete for {st.session_state.deal['industry']}.**\n\nConnor's Score: `{score:.3f}`",
                    "grid": df_results
                })
            except Exception:
                st.session_state.messages.append({"role": "assistant", "content": "I had trouble with the numbers provided. Please start a new screening and use digits only."})
        
        st.rerun()
else:
    if st.button("New Screening"):
        st.session_state.step = 0
        st.session_state.deal = {}
        st.session_state.messages = [{"role": "assistant", "content": "Starting a new first screening. " + QUESTIONS[0]}]
        st.rerun()
