import json
import asyncio
from tda.auth import easy_client
from tda.streaming import StreamClient
from tda import auth
import resources.config as config
import time

# entries = int(input('How many entries? '))
response = input('Confirm data override? (Y/N) ').upper()
if response == 'Y':
    pass
elif response == 'N':
    exit()
else:
    print('Entry error')


def authenticate():
    try:
        return auth.client_from_token_file(config.token_path, config.api_key)
    except FileNotFoundError:
        from selenium import webdriver
        with webdriver.Chrome(executable_path='/Users/ryanhermes/opt/anaconda3/envs/td-bot/chromedriver') as driver:
            return auth.client_from_login_flow(driver, config.api_key, config.redirect_uri, config.token_path)


def streamPrice(ticker, key):
    dictionary = json.loads(json.dumps(key.get_quotes(f'{ticker}').json()))
    while True:
        try:
            return dictionary[f'{ticker}']['regularMarketLastPrice']
        except KeyError:
            continue


async def stream():
    await stream_client.login()
    await stream_client.quality_of_service(StreamClient.QOSLevel.EXPRESS)
    stream_client.add_nasdaq_book_handler(order_book_handler)
    await stream_client.nasdaq_book_subs([ticker])

    while True:
        starttime = time.time()
        await stream_client.handle_message()
        print(f'Time elapsed: {round(time.time() - starttime, 2)}')


file = open('market_data2.py', 'w+')
file.write('import numpy as np')
file.write('\n')
file.write('\n')
file.write('data = np.array([')
file.write('\n')

iteration = 0
total_volumes = []


def order_book_handler(msg):
    global iteration
    iteration += 1
    print(f'Iteration: {iteration}', end=' ')
    file.write('[')

    current_price = str(streamPrice(ticker, key))
    file.write(f"[{current_price}, {iteration - 1}]")
    file.write(', ')

    dictionary = json.loads(json.dumps(msg))
    ask_snapshot, bid_snapshot = [], []

    for ask_bucket in dictionary['content'][0]['ASKS']:
        ask_price = ask_bucket['ASK_PRICE']
        ask_volume = ask_bucket['TOTAL_VOLUME']

        ask_snapshot.append([ask_price, ask_volume, iteration - 1])
        total_volumes.append(ask_volume)

    file.write(str(ask_snapshot))
    file.write(', ')

    for bid_bucket in dictionary['content'][0]['BIDS']:
        bid_price = bid_bucket['BID_PRICE']
        bid_volume = bid_bucket['TOTAL_VOLUME']

        bid_snapshot.append([bid_price, bid_volume, iteration - 1])
        total_volumes.append(bid_volume)

    file.write(str(bid_snapshot))
    file.write(']')
    file.write(',')

    file.write('\n')


ticker = 'aapl'.upper()
key = authenticate()
stream_client = StreamClient(easy_client(api_key=config.api_key, redirect_uri=config.redirect_uri,
                                         token_path=config.token_path), account_id=config.account_id)

asyncio.run(stream())

file.write('], dtype=object)')
