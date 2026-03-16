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
        revenue = float(str(deal["revenue"]).replace(',', ''))
        costs = float(str(deal["costs"]).replace(',', ''))
        investment = float(str(deal["investment"]).replace(',', ''))
        exp_return_pct = float(str(deal["expected_return"]).replace(',', ''))
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

        return f"""
**Industry:** {industry}  
**Revenue:** €{revenue:,.2f} | **Costs:** €{costs:,.2f} | **Profit:** €{profit:,.2f}  
**Profit Margin:** {margin*100:.2f}% | **ROI:** {roi*100:.2f}% | **Expected Return:** {exp_return_pct:.2f}%  

**Connor's Deal Score:** {score:.3f}  
{verdict}
"""
    except Exception as e:
        return "Calculation error. Please ensure all values were entered correctly."

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
    # Custom label for the assistant
    label = "Connor: Business Analyst" if msg["role"] == "assistant" else "You"
    with st.chat_message(msg["role"]):
        st.write(f"**{label}**")
        st.markdown(msg["content"])

# Handle Input
if st.session_state.step < len(QUESTIONS):
    if user_input := st.chat_input("Type your answer here..."):
        # Save User Message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        try:
            keys = ["industry", "revenue", "costs", "investment", "expected_return"]
            current_key = keys[st.session_state.step]
            
            # Save data
            st.session_state.deal[current_key] = user_input
            st.session_state.step += 1

            # Logic for next prompt
            if st.session_state.step == len(QUESTIONS):
                report = basic_screening_analysis(st.session_state.deal, st.session_state.connor_brain)
                st.session_state.messages.append({"role": "assistant", "content": f"Screening Complete:\n{report}"})
            else:
                next_q = QUESTIONS[st.session_state.step]
                st.session_state.messages.append({"role": "assistant", "content": next_q})
            
            st.rerun()

        except Exception:
            st.session_state.messages.append({"role": "assistant", "content": "Sorry, I ran into an error processing that. Let's try that last value again."})
            st.rerun()
else:
    if st.button("Analyze Another Deal"):
        st.session_state.step = 0
        st.session_state.deal = {}
        st.session_state.messages = [{"role": "assistant", "content": "Ready for a new deal. What industry is it in?"}]
        st.rerun()
