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
# Helpers
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
    # good deal if ROI > 20% and margin > 15%
    target = 1.0 if (roi > 0.2 and margin > 0.15) else 0.3
    error = score - target
    learner.update_weights(features, error)

    # Simple interpretation
    if score >= 0.7:
        verdict = "This looks like a **promising deal** at first glance."
    elif score >= 0.4:
        verdict = "This deal is **borderline**. It might work, but risks are noticeable."
    else:
        verdict = "This looks like a **weak deal** based on the basic numbers
