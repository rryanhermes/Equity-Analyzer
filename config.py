from tda import auth

api_key = 'K2ZC6DHENFQAKHALOX6IAGQLZELGBDQK@AMER.OAUTHAP'
account_id = '232543017'
redirect_uri = 'http://localhost'
token_path = 'token'

try:
    key = auth.client_from_token_file(token_path, api_key)
except FileNotFoundError:
    from selenium import webdriver

    with webdriver.Chrome(executable_path='/Users/ryanhermes/opt/anaconda3/envs/td-bot/chromedriver') as driver:
        key = auth.client_from_login_flow(driver, api_key, redirect_uri, token_path)