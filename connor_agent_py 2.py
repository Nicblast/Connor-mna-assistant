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
# Streamlit UI & Dark Theme
# -----------------------------
st.set_page_config(page_title="Connor Analyst", page_icon="🟢")

# Deloitte Midnight Style
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Headers */
    h1, h2, h3, h4, p, span, label { color: #ffffff !important; }
    
    /* Buttons */
    .stButton>button { 
        background-color: #86BC25; 
        color: black !important; 
        border-radius: 2px; 
        border: none; 
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover { background-color: #ffffff; color: #86BC25 !important; }
    
    /* Chat Bubbles */
    [data-testid="stChatMessage"] { 
        background-color: #1a1a1a; 
        border-left: 5px solid #86BC25; 
        color: #ffffff;
    }
    
    /* Tables and Inputs */
    .stTable { background-color: #1a1a1a; color: #ffffff; }
    div[data-baseweb="input"] { background-color: #333333 !important; color: white !important; }
    
    /* Metrics/Expander */
    .streamlit-expanderHeader { background-color: #1a1a1a !important; color: #86BC25 !important; }
