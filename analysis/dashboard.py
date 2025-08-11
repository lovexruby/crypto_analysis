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

# Further Key Numbers
min_price = filtered_df["price"].min()
max_price = filtered_df["price"].max()
median_price = filtered_df["price"].median()
pct_change = ((filtered_df["price"].iloc[0]) / filtered_df["price"].iloc[0]) * 100
volatility_pct = (std_dev/average) * 100
days_count = filtered_df.shape[0]

# Output
# Creating Columns
col1, col2 = st.columns([1, 2])
# Output Column 1
with col1:
    st.title("Crypto")
    st.write(f"**Average Price:** €{average:.2f}")
    st.write(f"**Standard Deviation:** €{std_dev:.2f}")

    st.subheader("Further Key Numbers")
    st.write(f"**Min Price:** €{min_price:.2f}")
    st.write(f"**Max Price:** €{max_price:.2f}")
    st.write(f"**Median Price:** €{median_price:.2f}")
    st.write(f"**Percentual Change:** {pct_change:.2f}%")
    st.write(f"**Volatility:** {volatility_pct:.2f}%")
    st.write(f"**Count of Marketdays:**{days_count}")

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
with col2:
    st.title("Dashboard")
    st.markdown("<div style='margin-top:1px'></div>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)