from datetime import datetime, timedelta
import config
import json
import matplotlib.pyplot as plt
import pprint
import requests
import time
import os

ticker = 'aapl'

# Initialize
key, api_key = config.key, config.api_key
pp = pprint.PrettyPrinter(indent=1)

fig, ax = plt.subplots()
fig.set_size_inches(10, 6)
fig.show()

# Functions
def graph():
    ax.clear()

    # Plot asks
    ax.plot([call[0] for call in calls], [price[1] for price in calls], color='green', label='Ask (Calls)')
    ax.plot([put[0] for put in puts], [price[1] for price in puts], color='red', label='Ask (Puts)')
    for call in calls:
        ax.scatter(call[0], call[1], color='green')
    for put in puts:
        ax.scatter(put[0], put[1], color='red')

    # Plot bids
    ax.plot([call[0] for call in calls], [price[2] for price in calls], color='green', alpha=.3, label='Bid (Calls)')
    ax.plot([put[0] for put in puts], [price[2] for price in puts], color='red', alpha=.3, label='Bid (Puts)')
    for call in calls:
        ax.scatter(call[0], call[2], color='green', alpha=.3)
    for put in puts:
        ax.scatter(put[0], put[2], color='red', alpha=.3)

    for call in calls:
        ax.axvline(call[0], color=(0, 0, 0, .1))

    # Formatting
    plt.xlabel('Strike Price ($)')
    plt.ylabel('Contract Price ($)')
    ax.set_title(f'Data for {ticker.upper()}, {days_until_exp} days until exp.', loc='center', pad=9)
    plt.subplots_adjust(left=.07, right=.97, bottom=.1, top=.95)
    plt.xticks([call[0] for call in calls])
    plt.xlim(calls[0][0], calls[-1][0])
    plt.ylim(0, max(calls[0][1], puts[-1][1]))
    fig.canvas.flush_events()
    fig.canvas.draw()
def streamOptions(strikes):
    # Access API
    response = requests.get('https://api.tdameritrade.com/v1/marketdata/chains', params={
        'apikey': api_key,
        'symbol': ticker.upper(),
        'strikeCount': str(strikes),
        'toDate': datetime.now() + timedelta(10),
    }, headers={'Bearer': f'{key}'})
    options = json.loads(json.dumps(response.json()))

    # pp.pprint(options)

    days_until_exp = str([list(options['callExpDateMap'].keys())[0]])[13:-2]

    # Parse for prices & deltas
    calls = []
    tomorrow = options['callExpDateMap'][list(options['callExpDateMap'].keys())[0]]
    for strike_price in tomorrow:
        for option in tomorrow[strike_price]:
            calls.append([float(strike_price), float(option['ask']) * 100, float(option['bid']) * 100, option['tradeTimeInLong']])

    puts = []
    tomorrow = options['putExpDateMap'][list(options['putExpDateMap'].keys())[0]]
    for strike_price in tomorrow:
        for option in tomorrow[strike_price]:
            puts.append([float(strike_price), float(option['ask']) * 100, float(option['bid']) * 100])

    return puts, calls, days_until_exp


# Loop
with open('optionsdata.txt', 'w+') as file:
    file.write(f'{datetime.now()}')
    file.write('\n')
    for i in range(10000):
        puts, calls, days_until_exp = streamOptions(12)
        print(calls)

        file.write(str(calls[6]))
        file.write('\n')

        graph()
        time.sleep(1)

