import streamlit as st
import numpy as np

# -----------------------------
# Connor's brain
# -----------------------------
class FinancialLearner:
    def __init__(self, learning_rate=0.1):
        self.lr = learning_rate
        # θ1, θ2, θ3
        self.weights = np.array([0.2, 0.4, 0.1])

    def predict(self, features):
        return np.dot(self.weights, features)

    def update_weights(self, features, error):
        gradient = error * features
        self.weights -= self.lr * gradient


# -----------------------------
# Questions
# -----------------------------
QUESTIONS = [
    "What industry is this deal in?",
    "What is the expected annual revenue (in €)?",
    "What are the annual costs (in €)?",
    "How much capital needs to be invested (in €)?",
    "What is the expected annual return (%)?"
]

def get_next_question(step):
    if step < len(QUESTIONS):
        return QUESTIONS[step]
    return None


def basic_screening_analysis(deal, learner):
    revenue = deal["revenue"]
    costs = deal["costs"]
    investment = deal["investment"]
    exp_return_pct = deal["expected_return"]  # as %
    industry = deal["industry"]

    profit = revenue - costs
    margin = profit / revenue if revenue > 0 else 0.0
    roi = profit / investment if investment > 0 else 0.0
    cash_flow = profit  # simple model

    # Features for Connor's learner
    features = np.array([margin, roi, exp_return_pct / 100.0])
    score = learner.predict(features)

    # Simple heuristic target for learning (under the hood)
    target = 1.0 if (roi > 0.2 and margin > 0.15) else 0.3
    error = score - target
    learner.update_weights(features, error)

    if score >= 0.7:
        verdict = "This looks like a **promising deal** at first glance."
    elif score >= 0.4:
        verdict = "This deal is **borderline**. It might work, but risks are noticeable."
    else:
        verdict = "This looks like a **weak deal** based on the basic numbers."

    report = f"""
**Industry:** {industry}

**Revenue:** €{revenue:,.2f}  
**Costs:** €{costs:,.2f}  
**Profit (Revenue - Costs):** €{profit:,.2f}  

**Profit Margin:** {margin*100:.2f}%  
**ROI (Profit / Investment):** {roi*100:.2f}%  
**Expected Return (input):** {exp_return_pct:.2f}%  

**Connor's Deal Score:** {score:.3f}  

{verdict}
"""
    return report


# -----------------------------
# Streamlit App
# -----------------------------
st.title("(¬‿¬) Connor — Basic Deal Screener")

# Init state
if "connor" not in st.session_state:
    st.session_state.connor = FinancialLearner()

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "text": "Hi, I'm Connor. I'll ask you a few questions about your deal and give you a basic initial screening."
    })

if "step" not in st.session_state:
    st.session_state.step = 0

if "deal" not in st.session_state:
    st.session_state.deal = {}

# Show chat history
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.markdown(f"**Connor:** {msg['text']}")
    else:
        st.markdown(f"**You:** {msg['text']}")

# Ask next question if needed
next_q = get_next_question(st.session_state.step)
if next_q and (len(st.session_state.messages) == 1 or st.session_state.messages[-1]["role"] == "user"):
    st.session_state.messages.append({"role": "assistant", "text": next_q})

# Input box
user_input = st.text_input("Your answer", key="user_input")

if st.button("Send"):
    text = user_input.strip()
    if text:
        st.session_state.messages.append({"role": "user", "text": text})

        step = st.session_state.step
        deal = st.session_state.deal
        connor = st.session_state.connor

        try:
            if step == 0:
                deal["industry"] = text
                st.session_state.step += 1

            elif step == 1:
                deal["revenue"] = float(text)
                st.session_state.step += 1

            elif step == 2:
                deal["costs"] = float(text)
                st.session_state.step += 1

            elif step == 3:
                deal["investment"] = float(text)
                st.session_state.step += 1

            elif step == 4:
                deal["expected_return"] = float(text)
                report = basic_screening_analysis(deal, connor)
                st.session_state.messages.append({
                    "role": "assistant",
                    "text": "Here is a basic initial screening of your deal:\n\n" + report
                })
                st.session_state.step += 1

            else:
                st.session_state.messages.append({
                    "role": "assistant",
