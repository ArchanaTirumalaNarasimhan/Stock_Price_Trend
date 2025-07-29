import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Title
st.title("📈 AAPL Stock Price Analysis")
st.markdown("Visualize Apple's stock price, returns, and moving averages (20-day & 50-day).")

# Download data
ticker = 'AAPL'
start_date = '2020-01-01'
end_date = '2023-01-01'
df = yf.download(ticker, start=start_date, end=end_date)

# Compute returns
df['Returns'] = df['Close'].pct_change()

# Drop missing values
df_clean = df.dropna()
df_clean['MA20'] = df_clean['Close'].rolling(window=20).mean()
df_clean['MA50'] = df_clean['Close'].rolling(window=50).mean()

# Avoid SettingWithCopyWarning
df1 = df_clean[['Close', 'MA20', 'MA50']].dropna()

# Show raw data
st.subheader("📋 Sample Data")
st.dataframe(df1.head(30))

# Plot 1: Close Price
st.subheader("📊 AAPL Close Price")
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(df['Close'], label='Close Price')
ax1.set_title(f"{ticker} Stock Price")
ax1.set_xlabel("Date")
ax1.set_ylabel("Price ($)")
ax1.legend()
st.pyplot(fig1)

# Plot 2: Moving Averages
st.subheader("📊 AAPL Close Price with Moving Averages")
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(df1['Close'], label='Close Price')
ax2.plot(df1['MA20'], label='20-Day MA', color='orange')
ax2.plot(df1['MA50'], label='50-Day MA', color='green')
ax2.set_title(f"{ticker} Stock Price with Moving Averages")
ax2.set_xlabel("Date")
ax2.set_ylabel("Price ($)")
ax2.legend()
st.pyplot(fig2)
