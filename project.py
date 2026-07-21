import yfinance as yf
import pandas as pd
import numpy as np
import csv
import json
import matplotlib.pyplot as plt

stockData = yf.download('ADS.DE','2026-01-01','2026-07-19')
stockData.columns = stockData.columns.get_level_values(0)
# print(stockData)

stockData.to_csv("Adidas_stock.csv", encoding="utf-8")


df = pd.DataFrame(stockData)
print("--- DataFrame ---")
# print(df)


# 3. Розробіть базову модель торгівлі на основі простої стратегії. Вам потрібно
# реалізувати стратегію перетину ковзного середнього (Moving Average Crossover),
# коли ви генеруєте сигнали купівлі або продажу на основі взаємодії короткострокових
# і довгострокових ковзних середніх.

df["MA20"] = df["Close"].rolling(window=20).mean()
df["MA50"] = df["Close"].rolling(window=50).mean()

df["Signal"] = np.where(df["MA20"] > df["MA50"], 1, np.where(df["MA20"] < df["MA50"], -1, 0))
df["Position"] = df["Signal"].diff()

df["Action"] = np.where(df["Position"] == 2, "Купівля", np.where(df["Position"] == -2, "Продаж", "Утримання"))
# print(df)
df.reset_index().to_csv("Adidas_strategy.csv", index=False, encoding="utf-8")

# 5. Розрахуйте прибуток/збиток (P&L) на основі ваших сигналів. Візуалізуйте
# результати (графік ціни з накладеними ковзними середніми та точками
# входу/виходу з позиції).

df["NextOpen"] = df["Open"].shift(-1)

trades = []
buy_price = None

for index, row in df.iterrows():
    if row["Action"] == "Купівля":
        buy_price = row["NextOpen"]
    elif row["Action"] == "Продаж" and buy_price is not None:
        sell_price = row["NextOpen"]
        profit = sell_price - buy_price
        trades.append({
            "Дата сигналу продажу": index,
            "Ціна купівлі": buy_price,
            "Ціна продажу": sell_price,
            "P&L": profit
        })
        buy_price = None
    else:
        pass

total_profit = sum(trade["P&L"] for trade in trades)
print(f"Total profit is {total_profit}")

for trade in trades:
    print(trade)

plt.figure(figsize=(14, 7))

plt.plot(df.index, df["Close"], label="Ціна закриття", color="black")
plt.plot(df.index, df["MA20"], label="MA20", color="blue")
plt.plot(df.index, df["MA50"], label="MA50", color="orange")

buy_points = df[df["Action"] == "Купівля"]
sell_points = df[df["Action"] == "Продаж"]

plt.scatter(buy_points.index, buy_points["Close"], color="green", label="Купівля", marker="^", s=100)
plt.scatter(sell_points.index, sell_points["Close"], color="red", label="Продаж", marker="v", s=100)

plt.title("Adidas — ковзні середні та сигнали")
plt.xlabel("Дата")
plt.ylabel("Ціна")
plt.legend()
plt.show()



