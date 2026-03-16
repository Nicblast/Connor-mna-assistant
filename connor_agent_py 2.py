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
# Questions & Logic
# -----------------------------
QUESTIONS = [
    "What industry is this deal in?",
    "What is the expected annual revenue (in €)?",
    "What are the annual costs (in €)?",
    "How much capital needs to be invested (in €)?",
    "What is the expected annual return (%)?"
]

def basic_screening_analysis(deal, learner):
    try:
        # Convert inputs to float, removing commas if the user typed them
        revenue = float(str(deal.get("revenue", 0)).replace(',', ''))
        costs = float(str(deal.get("costs", 0)).replace(',', ''))
        investment = float(str(deal.get("investment", 1)).replace(',', '')) # avoid div by zero
        exp_return_pct = float(str(deal.get("expected_return", 0)).replace(',', ''))
        industry = deal.get("industry", "Unknown")

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

        return f"""
**Industry:** {industry}  
**Revenue:** €{revenue:,.2f} | **Costs:** €{costs:,.2f} | **Profit:** €{profit:,.2f}  
**Profit Margin:** {margin*100:.2f}% | **ROI:** {roi*100:.2f}% | **Expected Return:** {exp_return_pct:.2f}%  

**Connor's Deal Score:** {score:.3f}  
{verdict}
"""
    except ValueError:
        return "I couldn't process those numbers. Please ensure they were entered as digits (e.g., 50000)."

# -----------------------------
# Streamlit App UI
# -----------------------------
st.set_page_config(page_title="Connor Business Analyst", page_icon="📊")
st.title("Connor: Business Analyst")

# Initialize session state
if "connor_brain" not in st.session_state:
    st.session_state.connor_brain = FinancialLearner()
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm Connor: Business Analyst. Let's look at your deal."}]
if "step" not in st.session_state:
    st.session_state.step = 0
if "deal" not in st.session_state:
    st.session_state.deal = {}

# Display chat history
for msg in st.session_state.messages:
    label = "Connor: Business Analyst" if msg["role"] == "assistant" else "You"
    with st.chat_message(msg["role"]):
        st.write(f"**{label}**")
        st.markdown(msg["content"])

# Input logic
if st.session_state.step < len(QUESTIONS):
    # Ask the current question
    if st.session_state.step == 0 and len(st.session_state.messages) == 1:
         st.session_state.messages.append({"role": "assistant", "content": QUESTIONS[0]})
         st.rerun()

    if user_input := st.chat_input("Type your answer..."):
        # Record user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Save data to the deal dictionary
        keys = ["industry", "revenue", "costs", "investment", "expected_return"]
        current_key = keys[st.session_state.step]
        st.session_state.deal[current_key] = user_input
        
        # Advance the step
        st.session_state.step += 1
        
        # Determine next response
        if st.session_state.step < len(QUESTIONS):
            next_q = QUESTIONS[st.session_state.step]
            st.session_state.messages.append({"role": "assistant", "content": next_q})
        else:
            # All questions answered, generate report
            report = basic_screening_analysis(st.session_state.deal, st.session_state.connor_brain)
            st.session_state.messages.append({"role": "assistant", "content": f"Screening Complete:\n{report}"})
        
        st.rerun()
else:
    if st.button("Analyze Another Deal"):
        st.session_state.step = 0
        st.session_state.deal = {}
        st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm Connor: Business Analyst. Let's look at a new deal.\n\n" + QUESTIONS[0]}]
        st.rerun()
