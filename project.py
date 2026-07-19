import yfinance as yf
import matplotlib.pyplot as plt

stockData = yf.download('PBYI','2022-07-01','2023-07-01')
print(stockData)

