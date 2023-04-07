from tda import auth
import config

try:
    key = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
    from selenium import webdriver

    with webdriver.Chrome(executable_path='/Users/ryanhermes/opt/anaconda3/envs/td-bot/chromedriver') as driver:
        key = auth.client_from_login_flow(driver, config.api_key, config.redirect_uri, config.token_path)