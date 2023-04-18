import requests
import config
import json
from datetime import datetime

key, api_key, symbol = config.key, config.api_key, 'AAPL'

def streamHistory():
    response = requests.get(f'https://api.tdameritrade.com/v1/marketdata/{symbol.upper()}/pricehistory',
                            params={
                                'apikey': api_key,
                                'period': 1,
                                'periodType': 'month',
                                'frequency': 1,
                                'frequencyType': 'daily'
                            }, headers={'Bearer': f'{key}'})
    history = json.loads(json.dumps(response.json()))

    historical_data = []
    for day in history['candles']: historical_data.append([day['close'], day['open'], day['high'], day['low'], datetime.fromtimestamp(int(str(day['datetime'])[0:10])).strftime('%m-%d')])

    yesterday_close = historical_data[-1][0]
    yesterday_open = historical_data[-1][1]
    yesterday_high = historical_data[-1][2]
    yesterday_low = historical_data[-1][3]

    return yesterday_close, yesterday_open, yesterday_high, yesterday_low

print(streamHistory())