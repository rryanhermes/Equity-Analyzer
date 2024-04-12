import pandas as pd
import matplotlib.pyplot as plt
import os

data = pd.read_csv('data/AAPL 2024-01-24.csv')

gap = data['close'] - data['vwap']

plt.plot(data['simpletime'], data['close'])
plt.plot(data['simpletime'], data['vwap'])

plt.show()

plt.plot(data['simpletime'], gap)
plt.axhline(y=0, color='black', linestyle='--')

plt.show()