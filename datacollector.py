import csv
import time
from datetime import datetime, timedelta
import resources.config as config
import pprint
import requests

ticker = 'aapl'
key, api_key = config.key, config.api_key
old_price, old_high, old_low, old_open, old_vol = 0, 0, 0, 0, 0

def streamTime():
    return datetime.now().strftime('%m-%d %H:%M:%S:%f')

def streamPrice():
    while True:
        try:
            current_price = key.get_quotes(f'{ticker.upper()}').json()[f'{ticker.upper()}']['regularMarketLastPrice']
            old_price = current_price
            return current_price
        except KeyError:
            return old_price

def streamHigh():
    while True:
        try:
            current_high = key.get_quotes(f'{ticker.upper()}').json()[f'{ticker.upper()}']['highPrice']
            old_high = current_high
            return current_high
        except KeyError:
            return old_high

def streamLow():
    while True:
        try:
            current_low = key.get_quotes(f'{ticker.upper()}').json()[f'{ticker.upper()}']['lowPrice']
            old_low = current_low
            return current_low
        except KeyError:
            return old_low
        
def streamOpen():
    while True:
        try:
            current_open = key.get_quotes(f'{ticker.upper()}').json()[f'{ticker.upper()}']['openPrice']
            old_open = current_open
            return current_open
        except KeyError:
            return old_open
        
def streamVolume():
    while True:
        try:
            current_vol = key.get_quotes(f'{ticker.upper()}').json()[f'{ticker.upper()}']['regularMarketLastSize']
            old_vol = current_vol
            return current_vol
        except KeyError:
            return old_vol

def prepareRow():
    return [streamTime(), streamPrice(), streamVolume(), streamOpen(), streamHigh(), streamLow()]

with open('data.csv', 'a+', newline='') as file: 
    writer = csv.writer(file)
    for i in range(5):
        start = time.time()

        # print(streamTime())
        # print(streamPrice())
        # print(streamHigh())
        # print(streamLow())
        # print(streamOpen())
        # print(streamVolume())

        writer.writerow(prepareRow())
        time.sleep(1 - (time.time() - start))
        
    print('finished')