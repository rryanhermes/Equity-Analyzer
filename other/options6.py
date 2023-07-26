import asyncio
import matplotlib.pyplot as plt
from tda.auth import easy_client
from tda.streaming import StreamClient
from datetime import datetime, timedelta
import resources.config as config
import json
import pprint
import requests

ticker = 'aapl'

def graph(calls, puts, current_price, days_until_exp, bid_snapshot, ask_snapshot, yesterday_close, yesterday_open, yesterday_high, yesterday_low):
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

    vol_ceiling = (calls[0][1]) / 2

    # Plot bids & asks
    ax.scatter([bid[0] for bid in bid_snapshot], [volume[1] for volume in bid_snapshot], color='blue', label='Bids')
    ax.scatter([ask[0] for ask in ask_snapshot], [volume[1] for volume in ask_snapshot], color='blue', label='Asks')

    # Plot extrema
    ax.axvline(yesterday_high, color='lightblue', label='Yesterday High')
    ax.axvline(yesterday_low, color='yellow', label='Yesterday Low')
    ax.axvline(yesterday_open, color='red', label='Yesterday Open')
    ax.axvline(yesterday_close, color='orange', label='Yesterday Close')

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
    plt.xlim(calls[0][0], calls[-1][0])
    plt.ylim(0, max(calls[0][1], puts[-1][1]))
    fig.canvas.flush_events()
    # plt.legend()
    fig.canvas.draw()
def streamDepth(message):
    bid_snapshot, ask_snapshot = [], []

    dictionary = json.loads(json.dumps(message))
    for bid_bucket in dictionary['content'][0]['BIDS']:
        bid_snapshot.append([bid_bucket['BID_PRICE'], bid_bucket['TOTAL_VOLUME']])
    for ask_bucket in dictionary['content'][0]['ASKS']:
        ask_snapshot.append([ask_bucket['ASK_PRICE'], ask_bucket['TOTAL_VOLUME']])

    return bid_snapshot, ask_snapshot
def streamHistory():
    response = requests.get(f'https://api.tdameritrade.com/v1/marketdata/{ticker.upper()}/pricehistory',
                            params={
                                'apikey': api_key,
                                'period': 1,
                                'periodType': 'month',
                                'frequency': 1,
                                'frequencyType': 'daily'
                            }, headers={'Bearer': f'{key}'})
    history = json.loads(json.dumps(response.json()))

    historical_data = []
    for day in history['candles']:
        historical_data.append([day['close'], day['open'], day['high'], day['low'], datetime.fromtimestamp(int(str(day['datetime'])[0:10])).strftime('%m-%d')])

    print(f'yesterday: {historical_data[-1]}')
    yesterday_close = historical_data[-1][0]
    yesterday_open = historical_data[-1][1]
    yesterday_high = historical_data[-1][2]
    yesterday_low = historical_data[-1][3]

    return yesterday_close, yesterday_open, yesterday_high, yesterday_low
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
def streamPrice():
    while True:
        try:
            current_price = json.loads(json.dumps(key.get_quotes(f'{ticker.upper()}').json()))[f'{ticker.upper()}'][
                'regularMarketLastPrice']
            return current_price
        except KeyError:
            continue
async def stream():
    await stream_client.login()
    await stream_client.quality_of_service(StreamClient.QOSLevel.FAST)
    stream_client.add_nasdaq_book_handler(order_book_handler)
    await stream_client.nasdaq_book_subs([ticker.upper()])

    while True:
        await stream_client.handle_message()

key, api_key = config.key, config.api_key
pp = pprint.PrettyPrinter(indent=1)
stream_client = StreamClient(easy_client(api_key=config.api_key, redirect_uri=config.redirect_uri,
                                         token_path=config.token_path), account_id=config.account_id)
fig, ax = plt.subplots()
fig.set_size_inches(10, 6)
fig.show()

def order_book_handler(message):

    current_price = streamPrice()
    print(f'Current Price: {current_price}')

    puts, calls, days_until_exp = streamOptions(12)
    print(f'Calls: {calls}')
    print(f'Puts: {puts}')

    bid_snapshot, ask_snapshot = streamDepth(message)
    print(f'Bid Snapshot: {bid_snapshot}')
    print(f'Ask Snapshot: {ask_snapshot}')

    yesterday_close, yesterday_open, yesterday_high, yesterday_low = streamHistory()
    print(f'{yesterday_close}')

    graph(calls, puts, current_price, days_until_exp, bid_snapshot, ask_snapshot, yesterday_close, yesterday_open, yesterday_high, yesterday_low)

asyncio.run(stream())
