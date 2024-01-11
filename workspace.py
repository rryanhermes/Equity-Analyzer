import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data/SNOW 2024-01-09.csv')

plt.plot(data['simpletime'], data['close'])
plt.plot(data['simpletime'], data['vwap'])
plt.show()