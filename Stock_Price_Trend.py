import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# -------------------------------
# Sidebar Inputs
# -------------------------------
st.sidebar.header("📊 Analysis Settings")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2023-01-01"))

# -------------------------------
# Title
# -------------------------------
st.title(f"📈 {ticker.upper()} Stock Price Analysis")
st.markdown(f"Visualize {ticker.upper()}'s stock price, returns, and moving averages (20-day & 50-day).")

# -------------------------------
# Download Data (with caching)
# -------------------------------
@st.cache_data(show_spinner=True)
def load_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    return df

df = load_data(ticker, start_date, end_date)

# -------------------------------
# Compute Returns and MAs
# -------------------------------
if not df.empty:
    df['Returns'] = df['Close'].pct_change()
    df_clean = df.dropna()
    df_clean['MA20'] = df_clean['Close'].rolling(window=20).mean()
    df_clean['MA50'] = df_clean['Close'].rolling(window=50).mean()
    df1 = df_clean[['Close', 'MA20', 'MA50']].dropna()

    # Sample Data
    st.subheader("📋 Sample Data")
    st.dataframe(df1.head(30))

    # Plot 1
    st.subheader(f"📊 {ticker.upper()} Close Price")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(df['Close'], label='Close Price')
    ax1.set_title(f"{ticker.upper()} Stock Price")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Price ($)")
    ax1.legend()
    st.pyplot(fig1)

    # Plot 2
    st.subheader(f"📊 {ticker.upper()} Close Price with Moving Averages")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(df1['Close'], label='Close Price')
    ax2.plot(df1['MA20'], label='20-Day MA', color='orange')
    ax2.plot(df1['MA50'], label='50-Day MA', color='green')
    ax2.set_title(f"{ticker.upper()} Stock Price with Moving Averages")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Price ($)")
    ax2.legend()
    st.pyplot(fig2)
else:
    st.warning("No data found for the given ticker and date range.")
