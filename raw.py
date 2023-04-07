import requests
import config
from tda import auth

try:
    key = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path='/Users/ryanhermes/opt/anaconda3/envs/td-bot/chromedriver') as driver:
        key = auth.client_from_login_flow(driver, config.api_key, config.redirect_uri, config.token_path)

endpoint = 'https://api.tdameritrade.com/v1/marketdata/AAPL/pricehistory'
response = requests.get(endpoint,
                        params={
                            'apikey': config.api_key,
                            'periodType': 'day',
                            'startDate': '1677891405',
                            'endDate': '1678496205'
                        }, headers={'Bearer': f'{key}'})
data = response.json()

print(data)
