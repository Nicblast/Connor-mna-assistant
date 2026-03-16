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
    # Core Financials
    rev = float(str(deal.get("revenue", 0)).replace(',', ''))
    cost = float(str(deal.get("costs", 0)).replace(',', ''))
    inv = float(str(deal.get("investment", 1)).replace(',', ''))
    
    # Logic for dynamic suggestions based on score
    if score >= 0.7:
        risk = "Low - Execution risk mainly."
        action = "Proceed to due diligence immediately."
        alt_sol = "Equity financing to preserve cash flow."
        alternatives = "Expansion into adjacent markets."
    elif score >= 0.4:
        risk = "Medium - Market volatility or high overheads."
        action = "Renegotiate costs before committing."
        alt_sol = "Phased investment approach."
        alternatives = "Joint venture to split the risk."
    else:
        risk = "High - Poor margin/ROI ratio."
        action = "Pivot or walk away."
        alt_sol = "Drastic cost restructuring."
        alternatives = "Wait for better market conditions."

    data = {
        "Category": ["Revenue", "Costs", "Profit", "Risks", "Best Course of Action", "Alternative Solutions", "Other Alternatives"],
        "Details": [
            f"€{rev:,.2f}", 
            f"€{cost:,.2f}", 
            f"€{(rev-cost):,.2f}",
            risk, 
            action, 
            alt_sol, 
            alternatives
        ]
    }
    return pd.DataFrame(data)

def basic_screening_analysis(deal, learner):
    try:
        revenue = float(str(deal.get("revenue", 0)).replace(',', ''))
        costs = float(str(deal.get("costs", 0)).replace(',', ''))
        investment = float(str(deal.get("investment", 1)).replace(',', ''))
        exp_return_pct = float(str(deal.get("expected_return", 0)).replace(',', ''))
        
        profit = revenue - costs
        margin = profit / revenue if revenue > 0 else 0
        roi = profit / investment if investment > 0 else 0

        features = np.array([margin, roi, exp_return_pct / 100])
        score = learner.predict(features)

        # Update Learner
        target = 1.0 if (roi > 0.2 and margin > 0.15) else 0.3
        learner.update_weights(features, score - target)

        return score, f"**Industry:** {deal.get('industry')}"
    except:
        return 0, "Error in processing data."

# -----------------------------
# Streamlit App UI
# -----------------------------
st.set_page_config(page_title="Connor Analyst", page_icon="📈")
st.title("Connor Analyst")
st.caption("First screening")

# Initialize session state
if "connor_brain" not in st.session_state:
    st.session_state.connor_brain = FinancialLearner()
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm Connor Analyst. Let's start the first screening."}]
if "step" not in st.session_state:
