import yfinance as yf
import pandas as pd
import numpy as np
import csv
import json
import matplotlib.pyplot as plt

stockData = yf.download('ADS.DE','2026-01-01','2026-07-19', multi_level_index=False)
# print(stockData)

stockData.to_csv("Adidas_stock.csv", encoding="utf-8")


df = pd.DataFrame(stockData)
#print("DataFrame")
#rint(df)

# 3. Розробіть базову модель торгівлі на основі простої стратегії. Вам потрібно
# реалізувати стратегію перетину ковзного середнього (Moving Average Crossover),
# коли ви генеруєте сигнали купівлі або продажу на основі взаємодії короткострокових
# і довгострокових ковзних середніх.

df["MA20"] = df["Close"].rolling(window=20).mean()
df["MA50"] = df["Close"].rolling(window=50).mean()

df["Signal"] = np.where(df["MA20"] > df["MA50"], 1, np.where(df["MA20"] < df["MA50"], -1, 0))
df["Position"] = df["Signal"].diff()

df["Action"] = np.where(df["Position"] == 2, "Купівля", np.where(df["Position"] == -2, "Продаж", "Утримання"))
print(df)