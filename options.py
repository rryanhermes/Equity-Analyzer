import requests
import config
from tda import auth
import json
import pprint

def authenticate():
    try:
        return auth.client_from_token_file(config.token_path, config.api_key)
    except FileNotFoundError:
        from selenium import webdriver
        with webdriver.Chrome(executable_path='/Users/ryanhermes/opt/anaconda3/envs/td-bot/chromedriver') as driver:
            return auth.client_from_login_flow(driver, config.api_key, config.redirect_uri, config.token_path)
key = authenticate()

response = requests.get('https://api.tdameritrade.com/v1/marketdata/chains',
                        params={
                                'apikey': config.api_key,
                                'contractType': 'call',
                                'symbol': 'AAPL',
                                'strikeCount': '2',
                                'includeQuotes': True
                                }, headers={'Bearer': f'{key}'})

data = json.loads(json.dumps(response.json()))

pp = pprint.PrettyPrinter(indent=1)
pp.pprint(data)
