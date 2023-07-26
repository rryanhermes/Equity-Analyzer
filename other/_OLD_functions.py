import json
import math

import matplotlib.pyplot as plt
from tda import auth
import tda
import resources.config as config
import time


def findMax(volumes, list):
    maximum = max(volumes)
    return list[1] / maximum


def liveGraphLevel2(ticker, ax, fig, max_volume, bids, asks, data, iteration, scale, zoom):
    ax.clear()

    ax.plot([i[1] for i in data], [p[0] for p in data], color='black')

    for ask_set in asks:
        for ask in ask_set:
            plt.scatter(ask[2], ask[0],
                        marker='s',
                        s=300,
                        color='red',
                        alpha=ask[1] / max_volume)
    for bid_set in bids:
        for bid in bid_set:
            plt.scatter(bid[2], bid[0],
                        marker='s',
                        s=300,
                        color='green',
                        alpha=bid[1] / max_volume)

    ax.set_title(f'Data for {ticker}', loc='left', pad=9)
    ax.set_xlim(left=max(1, iteration - scale + 1), right=iteration + scale / 5)
    if zoom is True: ax.set_ylim(data[-1][0] - (data[-1][0] / 1700), data[-1][0] + (data[-1][0] / 1700))

    fig.canvas.flush_events()
    fig.canvas.draw()


def graphMain(ticker, fig, ax1, ax2, iteration, scale, data, average_length, buys, sells, pl):
    ax1.clear()
    ax2.clear()

    ax1.plot([entry[0] for entry in data], [price[1] for price in data], color='black', label='Price')
    ax1.plot([entry[0] for entry in data], [average[2] for average in data], color='coral',
             label=f'Average ({average_length} periods)')
    ax2.plot([entry[0] for entry in data], [pl[3] for pl in data], color='darkblue')
    for item in buys:
        if item[0] > iteration - scale:
            ax1.axvline(x=item[0], color='green', linewidth=.5)
            ax2.axvline(x=item[0], color='green', linewidth=.5)
    for item in sells:
        if item[0] > iteration - scale:
            ax1.axvline(x=item[0], color='red', linewidth=.5)
            ax2.axvline(x=item[0], color='red', linewidth=.5)

    ax1.set_title(f'Data for {ticker}', loc='left', pad=9)
    ax1.set_title(f'Session P/L: {pl}', loc='right', pad=9)
    ax1.legend(loc='upper left')
    plt.xlabel('Time')
    plt.ylabel('P/L ($)')
    ax2.grid(axis='y')
    ax1.set_xlim(left=max(0, iteration - scale + 1), right=iteration + scale / 5)
    ax2.set_xlim(left=max(0, iteration - scale + 1), right=iteration + scale / 5)
    ax1.ticklabel_format(axis='y', useOffset=False)

    fig.canvas.flush_events()
    fig.canvas.draw()


def authenticate():
    try:
        return auth.client_from_token_file(config.token_path, config.api_key)
    except FileNotFoundError:
        from selenium import webdriver
        with webdriver.Chrome(executable_path='/Users/ryanhermes/opt/anaconda3/envs/td-bot/chromedriver') as driver:
            return auth.client_from_login_flow(driver, config.api_key, config.redirect_uri, config.token_path)


def buy(ticker, key, order_size, safety):
    if safety is False:
        key.place_order(config.account_id, tda.orders.equities.equity_buy_market(ticker, order_size))


def sell(ticker, key, order_size, safety):
    if safety is False:
        key.place_order(config.account_id, tda.orders.equities.equity_sell_market(ticker, order_size))


def streamPrice(ticker, key):
    dictionary = json.loads(json.dumps(key.get_quotes(f'{ticker}').json()))
    while True:
        try:
            return dictionary[f'{ticker}']['regularMarketLastPrice']
        except KeyError:
            continue


def streamAverage(data, average_length):
    data = list(list(zip(*data[-average_length:]))[1])
    average = sum(data) / len(data)
    return average


def sleep(start_time, iteration):
    execution_time = (time.time() - start_time)
    print(execution_time)
    sleep_time = 1 - execution_time
    try:
        time.sleep(sleep_time)
    except ValueError:
        print(f'Iteration {iteration} took {execution_time} seconds')


def chooseStock():
    ticker = ['aapl'.upper()]
    return ticker
