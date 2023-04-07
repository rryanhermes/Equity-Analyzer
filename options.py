import requests
import config
import json
import pprint
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

symbol = 'aapl'
contracts = 'all'
strikes = '10'
expiration = 1

pp = pprint.PrettyPrinter(indent=1)
plt.figure(figsize=(10, 6))

key, api_key = config.key, config.api_key
response1 = requests.get('https://api.tdameritrade.com/v1/marketdata/chains', params={
                            'apikey': api_key,
                            'symbol': symbol.upper(),
                            'contractType': contracts.upper(),
                            'strikeCount': strikes,
                            'toDate': datetime.now() + timedelta(expiration),
                        }, headers={'Bearer': f'{key}'})
response2 = requests.get('https://api.tdameritrade.com/v1/marketdata/quotes', params={
                             'apikey': api_key,
                             'symbol': symbol.upper(),
                         }, headers={'Bearer': f'{key}'})
response3 = requests.get(f'https://api.tdameritrade.com/v1/marketdata/{symbol.upper()}/pricehistory',params={
                            'apikey': api_key,
                            'period': 1,
                            'periodType': 'year',
                            'frequency': 1,
                            'frequencyType': 'daily'
                        }, headers={'Bearer': f'{key}'})

options = json.loads(json.dumps(response1.json()))
quotes = json.loads(json.dumps(response2.json()))
history = json.loads(json.dumps(response3.json()))

# pp.pprint(options)
# pp.pprint(quotes)
pp.pprint(history)

historical_data = []
for day in history['candles']:
    historical_data.append([datetime.fromtimestamp(int(str(day['datetime'])[0:10])).strftime('%m-%d'), day['close']])
historical_data.pop(0)
times = [time[0] for time in historical_data]
prices = [price[1] for price in historical_data]

calls = []
tomorrow = (str(datetime.now() + timedelta(expiration))[0:10] + ':1')
for strike_price in options['callExpDateMap'][tomorrow].keys():
    for option in options['callExpDateMap'][tomorrow][strike_price]:
        delta = option['delta']
        print(f"Call strike Price: {strike_price}, Delta: {delta}")
        calls.append([float(strike_price), delta])
for price in calls:
    plt.axhline(price[0], c=(0.1, .7, .2, price[1]))

puts = []
tomorrow = (str(datetime.now() + timedelta(expiration))[0:10] + ':1')
for strike_price in options['putExpDateMap'][tomorrow].keys():
    for option in options['putExpDateMap'][tomorrow][strike_price]:
        delta = option['delta']
        print(f"Put strike Price: {strike_price}, Delta: {delta}")
        puts.append([float(strike_price), delta])
for price in puts:
    plt.axhline(price[0], c=(0.8, .3, .2, abs(price[1])))

plt.plot(times, prices, color='black')
plt.xticks(range(0, 320, 50))
plt.show()