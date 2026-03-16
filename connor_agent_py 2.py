import streamlit as st
import numpy as np

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
# Questions
# -----------------------------
QUESTIONS = [
    "What industry is this deal in?",
    "What is the expected annual revenue (in €)?",
    "What are the annual costs (in €)?",
    "How much capital needs to be invested (in €)?",
    "What is the expected annual return (%)?"
]


# -----------------------------
# Basic Analysis
# -----------------------------
def basic_screening_analysis(deal, learner):
    revenue = deal["revenue"]
    costs = deal["costs"]
    investment = deal["investment"]
    exp_return_pct = deal["expected_return"]
    industry = deal["industry"]

    profit = revenue - costs
    margin = profit / revenue if revenue > 0 else 0
    roi = profit / investment if investment > 0 else 0

    features = np.array([margin, roi, exp_return_pct / 100])
    score = learner.predict(features)

    target = 1.0 if (roi > 0.2 and margin > 0.15) else 0.3
    error = score - target
    learner.update_weights(features, error)

    if score >= 0.7:
        verdict = "This looks like a **promising deal**."
    elif score >= 0.4:
        verdict = "This deal is **borderline**."
    else:
        verdict = "This looks like a **weak deal**."

    report = f"""
**Industry:** {industry}

**Revenue:** €{revenue:,.2f}  
**Costs:** €{costs:,.2f}  
**Profit:** €{profit:,.2f}  

**Profit Margin:** {margin*100:.2f}%  
**ROI:** {roi*100:.2f}%  
**Expected Return:** {exp_return_pct:.2f}%  

**Connor's Deal Score:** {score:.3f}

{verdict}
"""
    return report


# -----------------------------
# Streamlit App
# -----------------------------
st.title("(¬‿¬) Connor — Basic Deal Screener")

# Initialize session state
if "connor" not in st.session_state:
    st.session_state.connor = FinancialLearner()

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "text": "Hi, I'm Connor. I'll ask you a few questions about your deal."
    }]

if "step" not in st.session_state:
    st.session_state.step = 0

if "deal" not in st.session_state:
    st.session_state.deal = {}

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.markdown(f"**Connor:** {msg['text']}")
    else:
        st.markdown(f"**You:** {msg['text']}")

# Ask next question
if st.session_state.step < len(QUESTIONS):
    st.markdown(f"**Connor:** {QUESTIONS[st.session_state.step]}")

# Input box
user_input = st.text_input("Your answer", key="input_box")

# Process input
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

            elif step == 1:
                deal["revenue"] = float(text)

            elif step == 2:
                deal["costs"] = float(text)

            elif step == 3:
                deal["investment"] = float(text)

            elif step == 4:
                deal["expected_return"] = float(text)
                report = basic_screening_analysis(deal, connor)
                st.session_state.messages.append({
                    "role": "assistant",
                    "text": "Here is your initial screening:\n\n" + report
                })

            st.session_state.step += 1

        except ValueError:
            st.session_state.messages.append({
                "role": "assistant",
                "text": "Please enter a valid number."
            })

        st.session_state.input_box = ""
        st.experimental_rerun()
