import requests, config, json, pprint, time, matplotlib.pyplot as plt
from datetime import datetime, timedelta

ticker = 'googl'

# Initialize
key, api_key = config.key, config.api_key
pp = pprint.PrettyPrinter(indent=1)

fig, ax = plt.subplots()
fig.set_size_inches(10, 6)
fig.show()

# Functions
def graph():
    # Clear the Graph
    ax.clear()

    # Plot options
    ax.plot([call[0] for call in calls], [delta[1] for delta in calls], color='green', label='Calls')
    ax.plot([put[0] for put in puts], [delta[1] for delta in puts], color='red', label='Puts')

    for call in calls:
        ax.scatter(call[0], call[1], color='green')
    for put in puts:
        ax.scatter(put[0], put[1], color='red')

    # for call_snapshot in all_calls:
    #     for call in call_snapshot:
    #         ax.scatter(call[0], call[1], color='green')
    # for put_snapshot in all_puts:
    #     for put in put_snapshot:
    #         ax.scatter(put[0], put[1], color='red')

    # Plot lines
    ax.axvline(current_price, color='black', label='Current Price')
    ax.axhline(1, color=(0, 0, 0, .5))
    ax.axhline(0, color=(0, 0, 0, .5))
    for call in calls:
        ax.axvline(call[0], color=(0, 0, 0, .1))

    # Formatting
    plt.xlabel('Strike Price')
    plt.ylabel('Absolute Value of Delta')
    ax.set_title(f'Data for {ticker.upper()}, {days_till_exp} days until exp.', loc='center', pad=9)
    plt.subplots_adjust(left=.07, right=.97, bottom=.1, top=.95)
    plt.xticks([call[0] for call in calls])
    fig.canvas.flush_events()
    plt.legend()
    fig.canvas.draw()
def streamOptions(ticker, key, strikes):
    # Access API
    response = requests.get('https://api.tdameritrade.com/v1/marketdata/chains', params={
        'apikey': api_key,
        'symbol': ticker.upper(),
        'strikeCount': str(strikes),
        'toDate': datetime.now() + timedelta(10),
    }, headers={'Bearer': f'{key}'})
    options = json.loads(json.dumps(response.json()))

    days_till_exp = str([list(options['callExpDateMap'].keys())[0]])[13:14]

    # Parse for deltas
    calls = []
    tomorrow = options['callExpDateMap'][list(options['callExpDateMap'].keys())[0]]
    for strike_price in tomorrow:
        for option in tomorrow[strike_price]:
            calls.append([float(strike_price), float(option['delta'])])

    puts = []
    tomorrow = options['putExpDateMap'][list(options['putExpDateMap'].keys())[0]]
    for strike_price in tomorrow:
        for option in tomorrow[strike_price]:
            puts.append([float(strike_price), abs(float(option['delta']))])

    return puts, calls, days_till_exp
def streamPrice(ticker, key):
    # Access API
    dictionary = json.loads(json.dumps(key.get_quotes(f'{ticker.upper()}').json()))

    # Get Price
    while True:
        try:
            return dictionary[f'{ticker.upper()}']['regularMarketLastPrice']

        # Loop in case of API error
        except KeyError:
            continue

all_calls, all_puts = [], []

# Loop
for i in range(100):
    current_price = streamPrice(ticker, key)
    puts, calls, days_till_exp = streamOptions(ticker, key, 10)
    all_calls.append(calls)
    all_puts.append(puts)

    graph()
    time.sleep(1)
