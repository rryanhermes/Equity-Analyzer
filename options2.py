import requests
import config
import json
import pprint
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

ticker = 'aapl'
contracts = 'all'
strikes = 10
expiration = 1

pp = pprint.PrettyPrinter(indent=1)

key, api_key = config.key, config.api_key
response1 = requests.get('https://api.tdameritrade.com/v1/marketdata/chains', params={
    'apikey': api_key,
    'symbol': ticker.upper(),
    'contractType': contracts.upper(),
    'strikeCount': str(strikes),
    'toDate': datetime.now() + timedelta(expiration),
}, headers={'Bearer': f'{key}'})
response2 = requests.get('https://api.tdameritrade.com/v1/marketdata/quotes', params={
    'apikey': api_key,
    'symbol': ticker.upper(),
}, headers={'Bearer': f'{key}'})

options = json.loads(json.dumps(response1.json()))
quotes = json.loads(json.dumps(response2.json()))
current_price = json.loads(json.dumps(key.get_quotes(f'{ticker}').json()))[f'{ticker.upper()}']['regularMarketLastPrice']

calls = []
tomorrow = (str(datetime.now() + timedelta(expiration))[0:10] + ':1')
for strike_price in options['callExpDateMap'][tomorrow].keys():
    for option in options['callExpDateMap'][tomorrow][strike_price]:
        delta = option['delta']
        # print(f"Call strike Price: {strike_price}, Delta: {delta}")
        calls.append([float(strike_price), delta])

puts = []
tomorrow = (str(datetime.now() + timedelta(expiration))[0:10] + ':1')
for strike_price in options['putExpDateMap'][tomorrow].keys():
    for option in options['putExpDateMap'][tomorrow][strike_price]:
        delta = option['delta']
        # print(f"Put strike Price: {strike_price}, Delta: {delta}")
        puts.append([float(strike_price), abs(delta)])

# Plot Parameters
plt.figure(figsize=(10, 6))
plt.subplots_adjust(left=.07, right=.97, bottom=.1, top=.95)
plt.xticks([call[0] for call in calls])
plt.xlabel('Strike Price')
plt.ylabel('Absolute Value of Delta')

# Calls & Puts
plt.plot([call[0] for call in calls], [delta[1] for delta in calls], color='green', label='Calls')
plt.plot([put[0] for put in puts], [delta[1] for delta in puts], color='red', label='Puts')
for option in calls:
    plt.scatter(option[0], option[1], color='green')
for option in puts:
    plt.scatter(option[0], option[1], color='red')

# Lines
plt.axvline(current_price, color='black', label='Current Price')
plt.axhline(1, color=(0, 0, 0, .1))
plt.axhline(0, color=(0, 0, 0, .1))
for call in calls:
    plt.axvline(call[0], color=(0, 0, 0, .1))

# Show
plt.legend()
plt.show()
