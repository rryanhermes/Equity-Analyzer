import asyncio
import json
import pprint
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import requests
from tda.auth import easy_client
from tda.streaming import StreamClient
import config

ticker = 'aapl'

# Initialize
key, api_key = config.key, config.api_key
pp = pprint.PrettyPrinter(indent=1)
stream_client = StreamClient(easy_client(api_key=config.api_key, redirect_uri=config.redirect_uri,
                                         token_path=config.token_path), account_id=config.account_id)
fig, ax = plt.subplots()
fig.set_size_inches(10, 6)
fig.show()

# Functions
def graph(calls, puts, current_price, days_until_exp, ask_snapshot, bid_snapshot):
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

    # Plot depth
    for _ in ask_snapshot:
        ax.plot([ask[0] for ask in ask_snapshot], [volume[1] for volume in ask_snapshot])
    for _ in bid_snapshot:
        ax.plot([bid[0] for bid in bid_snapshot], [volume[1] for volume in bid_snapshot])

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

    # Parse for prices
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
def streamDepth(msg):
    # Access API
    dictionary = json.loads(json.dumps(msg))['content'][0]

    # Parse for market depth information
    bid_snapshot, ask_snapshot = [], []
    for bid_bucket in dictionary['BIDS']:
        bid_snapshot.append([bid_bucket['BID_PRICE'], bid_bucket['TOTAL_VOLUME']])
    for ask_bucket in dictionary['ASKS']:
        ask_snapshot.append([ask_bucket['ASK_PRICE'], ask_bucket['TOTAL_VOLUME']])

    return bid_snapshot, ask_snapshot
def streamPrice():
    while True:
        try:
            return json.loads(json.dumps(key.get_quotes(f'{ticker.upper()}').json()))[f'{ticker.upper()}'][
                'regularMarketLastPrice']
        except KeyError:
            continue
async def stream():
    time1 = time.time()
    print('Start')

    await stream_client.login()
    await stream_client.quality_of_service(StreamClient.QOSLevel.FAST)
    stream_client.add_nasdaq_book_handler(order_book_handler_aka_loop)
    await stream_client.nasdaq_book_subs([ticker])

    for _ in range(100):
        time2 = time.time()
        print(f'Beginning stream ({round(time2 - time1, 3)})')
        await stream_client.handle_message()

# Logic flow
def order_book_handler_aka_loop(msg, time2):
    time3 = time.time()
    print(f'Loop begun ({round(time3 - time2, 3)})')

    # Test options4.py to see if streaming price from options API endpoint is viable.
    # I accidentally made those changes in options4.py instead of options5.py,
    # So if it doesn't work I need to revisit.

    # Last thing: make sure that the stream runs once a second with 'Fast' instead of 'Express'
    # Also get rid of time logs if this works

    current_price = streamPrice()
    time4 = time.time()
    print(f'Gathered price ({round(time4 - time3, 3)})')

    puts, calls, days_until_exp = streamOptions(12)
    time5 = time.time()
    print(f'Gathered options ({round(time5 - time4, 3)})')

    bid_snapshot, ask_snapshot = streamDepth(msg)
    time6 = time.time()
    print(f'Gathered depth ({round(time6 - time5, 3)})')

    graph(calls, puts, current_price, days_until_exp, ask_snapshot, bid_snapshot)
    time7 = time.time()
    print(f'Graphing ({round(time7 - time6, 3)})')

    time8 = time.time()
    print(f'Loop end ({round(time8 - time7, 3)})')

asyncio.run(stream())
