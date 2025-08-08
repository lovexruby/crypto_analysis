import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np
from datetime import datetime

# Load Dataframe
dirname = os.path.dirname(__file__)
csv_path = os.path.join(dirname, 'data', 'crypto_prices.csv')
df = pd.read_csv(csv_path)

# Sidebar for Options
st.sidebar.title("Settings")
coins = df["coin"].unique()
# Capitalize Coins
coin_map = {coin.capitalize(): coin for coin in coins}
selected_coin_cap = st.sidebar.selectbox("Choose a Cryptocurrency", list(coin_map.keys()))
selected_coin = coin_map[selected_coin_cap]


# Choose Timeframe
min_date = df["date"].min()
max_date = df["date"].max()
date_range = st.sidebar.date_input("Choose Timeframe", [pd.to_datetime(min_date), pd.to_datetime(max_date)])

# Filter Data
df["date"] = pd.to_datetime(df["date"])
filtered_df = df[
    (df["coin"] == selected_coin) &
    (df["date"] >= pd.to_datetime(date_range[0])) &
    (df["date"] <= pd.to_datetime(date_range[1]))
]

# Calculate Statistic
average = filtered_df["price"].mean()
std_dev = filtered_df["price"].std()

# Output
st.title("Crypto-Dashboard")
st.write(f"**Average Price:** €{average:.2f}")
st.write(f"**Standard Deviation:** €{std_dev:.2f}")

# Convert Date into a Number for the Regressioncalculation
x_numeric = filtered_df["date"].map(datetime.toordinal)
y = filtered_df["price"]

# Calculate Regression
slope, intercept = np.polyfit(x_numeric, y, 1)
trend = slope * x_numeric + intercept


# Show Plot
fig = px.line(
    filtered_df,
    x="date",
    y="price",
    title=f"Price Evolution of {selected_coin.capitalize()}",
    labels={f"price": "Price in Euro", "date": "Date"},
)

fig.add_scatter(
    x=filtered_df["date"],
    y=trend,
    mode="lines",
    name="Trend Line",
    line=dict(dash="dash", color="red")
)

fig.update_traces(mode="lines+markers", selector=dict(type='scatter', name=selected_coin.capitalize()))
st.plotly_chart(fig)