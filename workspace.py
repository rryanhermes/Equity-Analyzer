import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import datetime

data = pd.read_csv('data/CRM_merged.csv')

data['Insider_Trades'] = data['Insider_Trades'].fillna(0)

# Assuming data is your DataFrame containing 'Date', 'Close', 'Volume', and 'Insider_Trades' columns
data = data[['Date', 'Close', 'Volume', 'Insider_Trades']]
data['Date'] = pd.to_datetime(data['Date'])

# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plot Insider_Trades
ax1.plot(data['Date'], data['Insider_Trades'], color='blue')
ax1.set_ylabel('Insider Trades')

# Plot Close
ax2.plot(data['Date'], data['Close'], color='green')
ax2.set_ylabel('Close Price')

# Set common x-axis label
ax2.set_xlabel('Date')

# Show plot
plt.show()