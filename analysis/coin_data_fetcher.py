import requests
import pandas as pd


def fetch_coin_history(coin_id, days=90):
    url = f"http://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    parameters = {"vs_currency": "eur", "days": days, "interval": "daily"}
    response = requests.get(url, params = parameters)

    if response.status_code != 200:
        raise Exception(f"Fehler beim Abrufen von {coin_id}: {response.status_code}")

    data = response.json()["prices"]
    df = pd.DataFrame(data, columns =["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit = "ms")
    df.drop("timestamp", axis = 1, inplace = True)
    df["coin"] = coin_id
    return df