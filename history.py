import requests
import config
import json
from datetime import datetime

key, api_key, symbol = config.key, config.api_key, 'AAPL'
response = requests.get(f'https://api.tdameritrade.com/v1/marketdata/{symbol.upper()}/pricehistory',
                        params={
                            'apikey': api_key,
                            'period': 1,
                            'periodType': 'year',
                            'frequency': 1,
                            'frequencyType': 'daily'
                        }, headers={'Bearer': f'{key}'})
history = json.loads(json.dumps(response.json()))

historical_data = []
for day in history['candles']:
    historical_data.append([datetime.fromtimestamp(int(str(day['datetime'])[0:10])).strftime('%m-%d'), day['close']])

print(historical_data)