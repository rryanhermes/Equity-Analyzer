import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data/AAPL 2024-01-19.csv')

plt.plot(data['simpletime'], data['close'])
plt.plot(data['simpletime'], data['vwap'])
plt.show()