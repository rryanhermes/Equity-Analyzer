import requests
import config
from tda import auth
import json
import pprint

pp = pprint.PrettyPrinter(indent=1)

# array = np.array(4)
# print(array)
#
# for i in range(5):
#     print(np.append(array, [[i, 'a']]))
#
# print(array)

try:
    key = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path='/Users/ryanhermes/opt/anaconda3/envs/td-bot/chromedriver') as driver:
        key = auth.client_from_login_flow(driver, config.api_key, config.redirect_uri, config.token_path)

endpoint = 'https://api.tdameritrade.com/v1/marketdata/chains'

response = requests.get(endpoint,
                        params={'apikey': config.api_key,
                                'contractType': 'call',
                                'symbol': 'AAPL',
                                'strikeCount': '2',
                                'includeQuotes': True
                                },
                        headers={'Bearer': f'{key}'})
data = json.loads(json.dumps(response.json()))

pp.pprint(data)
