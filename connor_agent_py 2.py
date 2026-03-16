import streamlit as st
import numpy as np

# -----------------------------
# Connor: The Financial Learner
# -----------------------------
class FinancialLearner:
    def __init__(self, learning_rate=0.1):
        self.lr = learning_rate
        self.weights = np.array([0.2, 0.4, 0.1])  # θ1, θ2, θ3

    def predict(self, features):
        return np.dot(self.weights, features)

    def update_weights(self, features, error):
        gradient = error * features
        self.weights -= self.lr * gradient


# -----------------------------
# Streamlit App
# -----------------------------
st.title("(¬‿¬) Connor — Your Learning Agent")

# Initialize Connor in session state
if "connor" not in st.session_state:
    st.session_state.connor = FinancialLearner()

connor = st.session_state.connor

st.subheader("Input Features")
x1 = st.number_input("Feature x1", value=1.0)
x2 = st.number_input("Feature x2", value=1.0)
x3 = st.number_input("Feature x3", value=1.0)

features = np.array([x1, x2, x3])

if st.button("Predict"):
    prediction = connor.predict(features)
    st.write(f"### Connor's Prediction: **{prediction:.4f}**")

st.subheader("Provide Feedback (Target Value)")
target = st.number_input("Target Score", value=1.0)

if st.button("Train Connor"):
    prediction = connor.predict(features)
    error = prediction - target
    connor.update_weights(features, error)

    st.write(f"### Error: **{error:.4f}**")
    st.write("### Updated Weights:")
    st.write(connor.weights)

st.divider()
st.caption("Connor learns through gradient descent — every correction makes him a bit smarter.")
