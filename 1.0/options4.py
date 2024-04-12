from datetime import datetime, timedelta
import resources.config as config
import json
import matplotlib.pyplot as plt
import pprint
import requests
import time

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

    # # Plot volumes
    # ax.plot([call[0] for call in calls], [price[3] for price in calls], color='green', label='Calls')
    # ax.plot([put[0] for put in puts], [price[3] for price in puts], color='red', label='Puts')

    # for call_snapshot in all_calls:
    #     for call in call_snapshot:
    #         ax.scatter(call[0], call[1], color='green')
    # for put_snapshot in all_puts:
    #     for put in put_snapshot:
    #         ax.scatter(put[0], put[1], color='red')

    # Plot lines
    ax.axvline(current_price, color='black', label='Current Price')
    for call in calls:
        ax.axvline(call[0], color=(0, 0, 0, .1))

    # Formatting
    plt.xlabel('Strike Price ($)')
    plt.ylabel('Contract Price ($)')
    ax.set_title(f'Data for {ticker.upper()}, {days_until_exp} days until exp.', loc='center', pad=9)
    plt.subplots_adjust(left=.07, right=.97, bottom=.1, top=.95)
    plt.xticks([call[0] for call in calls])
    fig.canvas.flush_events()
    plt.legend()
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

    pp.pprint(options)

    days_until_exp = str([list(options['callExpDateMap'].keys())[0]])[13:-2]

    # Parse for prices & deltas
    calls = []
    tomorrow = options['callExpDateMap'][list(options['callExpDateMap'].keys())[0]]
    for strike_price in tomorrow:
        for option in tomorrow[strike_price]:
            calls.append([float(strike_price), float(option['ask']) * 100, float(option['bid']) * 100])
            # calls[-1].append(option['totalVolume'])

    puts = []
    tomorrow = options['putExpDateMap'][list(options['putExpDateMap'].keys())[0]]
    for strike_price in tomorrow:
        for option in tomorrow[strike_price]:
            puts.append([float(strike_price), float(option['ask']) * 100, float(option['bid']) * 100])
            # puts[-1].append(option['totalVolume'])

    return puts, calls, days_until_exp
def streamPrice():
    while True:
        try:
            current_price = json.loads(json.dumps(key.get_quotes(f'{ticker.upper()}').json()))[f'{ticker.upper()}'][
                'regularMarketLastPrice']
            return current_price
        except KeyError:
            continue

all_calls, all_puts = [], []
fff = []

# Loop
for i in range(100):
    current_price = streamPrice()

    puts, calls, days_until_exp = streamOptions(12)
    all_calls.append(calls)
    all_puts.append(puts)

    # fff.append(calls[5][1])
    # if i > 3: print(statistics.st_dev(fff))

    graph()
    time.sleep(1)
