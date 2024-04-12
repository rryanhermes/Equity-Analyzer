import csv
import time
from datetime import datetime
import resources.config as config

ticker = 'aapl'
buffer_size = 10

key, api_key, data_buffer = config.key, config.api_key, []

def streamData():
    while True:
        try:
            response = key.get_quotes(f'{ticker.upper()}').json()[f'{ticker.upper()}']
            return response
        except KeyError:
            continue

print(streamData())

def streamTime():
    return datetime.now().strftime('%m-%d %H:%M:%S:%f')
def streamPrice(response):
    return response['regularMarketLastPrice']
def streamVolume(response):
    return response['regularMarketLastSize']
def streamOpen(response):
    return response['openPrice']
def streamHigh(response):
    return response['highPrice']
def streamLow(response):
    return response['lowPrice']

def prepareRow(response):
    return [streamTime(), streamPrice(response), streamVolume(response), streamOpen(response), streamHigh(response), streamLow(response)]
def flush_buffered_data(file, data_buffer):
    with open(file, 'a+', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data_buffer)
    data_buffer.clear()

for i in range(10800):
    start = time.time()

    row = prepareRow(streamData())
    data_buffer.append(row)
    print(f"{i+1}: {row}")

    if len(data_buffer) >= buffer_size: flush_buffered_data('data.csv', data_buffer)

    try: time.sleep(1 - (time.time() - start))
    except ValueError: continue

if data_buffer: flush_buffered_data('data.csv', data_buffer)

print('finished')
