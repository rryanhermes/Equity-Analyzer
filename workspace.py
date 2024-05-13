from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import config

ticker = 'AAPL'

one = pd.read_csv(f'{ticker}.csv')
two = pd.read_csv(f'{ticker}_insider_trades.csv')

newdata = pd.merge(one, two, 'outer', left_on='Date', right_on='Trade Date')

print(newdata['Close'])

plt.figure(figsize=(12, 6))
plt.plot(newdata['Date'], newdata['Close'], label=f'{ticker} Close Price')

insider_trade_dates = newdata[newdata['Value'].notnull()]
for index, row in insider_trade_dates.iterrows():
    if row['Value'][0] == '-': plt.axvline(x=row['Date'], color='red')
    if row['Value'][0] != '-': plt.axvline(x=row['Date'], color='green')

    plt.text(row['Date'], newdata['Close'].max() * 0.25, row['Insider Name'], rotation=90, fontsize=11, backgroundcolor='white')
    plt.text(row['Date'], newdata['Close'].max() * 1.05, row['Value'], rotation=90, fontsize=11, backgroundcolor='white')

plt.xticks(newdata['Date'][::30], rotation=45)
plt.tight_layout()
plt.show()