import streamlit as st
import numpy as np

# Connor's brain
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
# Streamlit Chatbot Connor
# -----------------------------
st.title("(¬‿¬) Connor — Your Financial Learning Agent")

# Initialize Connor
if "connor" not in st.session_state:
    st.session_state.connor = FinancialLearner()

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "text": 
        "Hey, I'm Connor. I’ll ask you a few things and learn from your feedback."})


# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.markdown(f"**Connor:** {msg['text']}")
    else:
        st.markdown(f"**You:** {msg['text']}")


# User input
user_input = st.text_input("Your message")

if user_input:
    st.session_state.messages.append({"role": "user", "text": user_input})

    # Connor logic
    connor = st.session_state.connor

    # Expecting 3 features
    try:
        x1, x2, x3 = map(float, user_input.split(","))
        features = np.array([x1, x2, x3])

        prediction = connor.predict(features)

        reply = f"My predicted financial score is **{prediction:.3f}**.\n"
        reply += "What was the real score? (Just type the number)"

        st.session_state.messages.append({"role": "assistant", "text": reply})

    except:
        # If user gives the real score
        try:
            target = float(user_input)

            # Last features used
            features = features  # from previous step
            prediction = connor.predict(features)
            error = prediction - target

            connor.update_weights(features, error)

            reply = f"Got it. Updating my understanding.\n"
            reply += f"My new weights are: {connor.weights}"

            st.session_state.messages.append({"role": "assistant", "text": reply})

        except:
            st.session_state.messages.append({
                "role": "assistant",
                "text": "Give me 3 numbers like: 1.2, 0.5, 3.0"
            })

