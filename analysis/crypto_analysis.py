from coin_data_fetcher import fetch_coin_history
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

os.makedirs("data", exist_ok=True)
os.makedirs("plots", exist_ok=True)
coins = ["bitcoin", "ethereum", "dogecoin", "trumpcoin"]

all_data = []
for coin in coins:
    try:
        df = fetch_coin_history(coin , days = 180)
        all_data.append(df)
        time.sleep(2)
    except Exception as e:
        print(e)

crypto_df = pd.concat(all_data)
crypto_df.to_csv("data/crypto_prices.csv", index = False)

for coin in coins:
    coin_df = crypto_df[crypto_df["coin"] == coin]
    plt.plot(coin_df["date"], coin_df["price"], label = coin)

plt.title("Cryptoprices in the past 180 days")
plt.xlabel("Date")
plt.ylabel("Price in Euro")
plt.legend()
plt.tight_layout()
plt.savefig("plots/price_chart.png")
plt.show()