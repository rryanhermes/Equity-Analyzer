import csv
import time
from datetime import datetime, timedelta
import resources.config as config
import pprint
import requests

ticker = 'aapl'
key, api_key, pp = config.key, config.api_key, pprint.PrettyPrinter(indent=1)

def streamOptions(strike_count):
    response = requests.get('https://api.tdameritrade.com/v1/marketdata/chains', params={
        'apikey': api_key,
        'symbol': ticker.upper(),
        'strikeCount': str(strike_count),
        'toDate': datetime.now() + timedelta(days=10),
    }, headers={'Bearer': f'{key}'})
    data = response.json()

    current_price = streamPrice()
    current_time = datetime.now().strftime("%m-%d %H:%M:%S")

    narrowed_data = data['callExpDateMap'][list(data['callExpDateMap'].keys())[0]]
    headers = list(narrowed_data.keys())[:strike_count]
    print(headers)
    asks = [current_time] + [current_price] + [narrowed_data[strike][0]['ask'] for strike in headers]
    # print(asks[1:-1])

    return headers, asks

def streamPrice():
    while True:
        try:
            current_price = key.get_quotes(f'{ticker.upper()}').json()[f'{ticker.upper()}']['regularMarketLastPrice']
            return current_price
        except KeyError:
            continue

with open('optionsdata.csv', 'w+', newline='') as file:
    writer = csv.writer(file)
    for iteration in range(20000):

        if file.tell() == 0:
            writer.writerow(['Time', 'Underlying'] + streamOptions(10)[0])

        asks = streamOptions(10)[1]
        writer.writerow(asks)

        time.sleep(1)