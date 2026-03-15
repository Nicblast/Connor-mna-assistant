import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Connor – M&A Assistant", page_icon="🤝")

st.title("🤝 Connor – Your M&A Project Assistant")
st.write("Let's go through the intake questions one at a time.")

# --- Question 1 ---
deal_type = st.selectbox(
    "First question: What type of M&A deal?",
    ["Select an option", "Acquisition", "Merger", "Divestiture", "Other"]
)

if deal_type != "Select an option":
    st.success(f"Deal type recorded: {deal_type}")

    # --- Question 2 ---
    industry = st.text_input("Second question: Which industry does the target operate in?")

    if industry:
        st.success(f"Industry noted: {industry}")

        # --- Question 3 ---
        deal_size = st.selectbox(
            "Third question: What is the approximate deal size?",
            ["Select an option", "<50M", "50–200M", "200M–1B", ">1B", "More"]
        )

        if deal_size != "Select an option":
            st.success(f"Deal size captured: {deal_size}")

            # --- Question 4 ---
            risk = st.selectbox(
                "Fourth question: What is the approximate risk level?",
                ["Select an option", "High risk", "Moderate risk", "Low risk"]
            )

            if risk != "Select an option":
                st.success(f"Risk level identified: {risk}")

                # --- Optional ticker ---
                ticker = st.text_input(
                    "Optional: Enter a stock ticker (e.g., AAPL, MSFT) or leave blank"
                )

                # --- Summary ---
                st.subheader("📄 Connor's Summary")
                st.write(f"**Deal type:** {deal_type}")
                st.write(f"**Industry:** {industry}")
                st.write(f"**Deal size:** {deal_size}")
                st.write(f"**Risk level:** {risk}")

                # --- Recommendation ---
                st.subheader("📌 Connor's Recommendation")

                if risk == "High risk":
                    st.warning("This deal may require enhanced due diligence and deeper risk review.")
                elif risk == "Moderate risk":
                    st.info("This deal appears manageable but should be monitored closely.")
                elif risk == "Low risk":
                    st.success("This deal seems feasible with no major red flags.")

                # --- Market Data ---
                if ticker:
                    st.subheader("📊 Market Data")

                    try:
                        data = yf.Ticker(ticker)
                        info = data.info

                        st.write(f"**Company:** {info.get('longName')}")
                        st.write(f"**Sector:** {info.get('sector')}")
                        st.write(f"**Industry:** {info.get('industry')}")
                        st.write(f"**Market Cap:** {info.get('marketCap')}")
                        st.write(f"**Current Price:** {info.get('currentPrice')}")

                    except Exception:
                        st.error("Could not retrieve market data for that ticker.")
