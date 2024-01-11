import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('daytradingdata.csv')[5000:]
data.drop(['volume', 'seconds'], axis=1, inplace=True)

data['average'] = data['underlying'].rolling(window=800).mean()
data['buy'] = np.where((data['average'] < data['underlying']) & (data['underlying'].shift(1) < data['average'].shift(1)), 1, 0)
data['sell'] = np.where((data['average'] > data['underlying']) & (data['underlying'].shift(1) > data['average'].shift(1)), 1, 0)
# print(data[:30])

def pl(data):
    pl = []
    in_position = False
    last_bought_price = 0
    cumulative_pl = 0

    for i in range(len(data)):
        current_price = data.iloc[i]['underlying']
        buy = data.iloc[i]['buy'] == 1
        sell = data.iloc[i]['sell'] == 1

        if buy and not in_position:
            in_position = True
            last_bought_price = current_price

        elif sell and in_position:
            cumulative_pl += current_price - last_bought_price
            in_position = False

        if in_position:
            pl.append(cumulative_pl + current_price - last_bought_price)
        else:
            pl.append(pl[-1] if pl else 0)

    return pl


profitloss = pl(data)

fig, (ax1, ax2) = plt.subplots(2, 1)

ax1.plot(data['underlying'])
ax1.plot(data['average'])
ax2.plot(profitloss)
plt.show()