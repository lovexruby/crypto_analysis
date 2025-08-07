import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

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
    (df["coin"] == selected_coin_cap) &
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

# Show Plot
fig, ax = plt.subplots()
ax.plot(filtered_df["date"], filtered_df["price"], label = selected_coin)
ax.set_xlabel("Date")
ax.set_ylabel("Price in Euro")
ax.set_title(f"Priceevolution of {selected_coin.upper()}")
ax.legend()
st.pyplot(fig)