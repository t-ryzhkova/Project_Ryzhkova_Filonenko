import yfinance as yf
import pandas as pd
import numpy as np
import csv
import json
import matplotlib.pyplot as plt

stockData = yf.download('ADS.DE','2026-01-01','2026-07-19')
print(stockData)

stockData.to_csv("Adidas_stock.csv", encoding="utf-8")


df = pd.DataFrame(stockData)
print("--- DataFrame ---")
print(df)
