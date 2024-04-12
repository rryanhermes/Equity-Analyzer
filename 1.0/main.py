import asyncio
from tda.auth import easy_client
from tda.streaming import StreamClient
import json
import matplotlib.pyplot as plt
from tda import auth
import tda
import resources.config as config

ticker = 'tsla'.upper()
scale = 28
order_size = 1
zoom = False
safety = True


def authenticate():
    try:
        return auth.client_from_token_file(config.token_path, config.api_key)
    except FileNotFoundError:
        from selenium import webdriver
        with webdriver.Chrome(executable_path='/Users/ryanhermes/opt/anaconda3/envs/td-bot/chromedriver') as driver:
            return auth.client_from_login_flow(driver, config.api_key, config.redirect_uri, config.token_path)


def graph(max_volume):
    ax.clear()

    ax.plot([i[1] for i in data], [p[0] for p in data], color='black')

    for ask_set in asks:
        for ask in ask_set:
            plt.scatter(ask[2], ask[0],
                        marker='s',
                        s=300,
                        color='red',
                        alpha=ask[1] / max_volume,
                        linewidths=0
                        )
    for bid_set in bids:
        for bid in bid_set:
            plt.scatter(bid[2], bid[0],
                        marker='s',
                        s=300,
                        color='green',
                        alpha=bid[1] / max_volume,
                        linewidths=0
                        )

    ax.set_title(f'Data for {ticker}', loc='left', pad=9)
    ax.set_xlim(left=max(1, iteration - scale + 1), right=iteration + scale / 5)
    if zoom is True:
        ax.set_ylim(data[-1][0] - (data[-1][0] / 1370), data[-1][0] + (data[-1][0] / 1370))

    fig.canvas.flush_events()
    fig.canvas.draw()


def final_graph():
    max_volume = max(volumes)

    ax.plot([i[1] for i in data], [p[0] for p in data], color='black')
    for ask_set in asks:
        for ask in ask_set:
            plt.scatter(ask[2], ask[0],
                        marker='s',
                        s=300,
                        color='red',
                        alpha=ask[1] / max_volume,
                        linewidths=0
                        )
    for bid_set in bids:
        for bid in bid_set:
            plt.scatter(bid[2], bid[0],
                        marker='s',
                        s=300,
                        color='green',
                        alpha=bid[1] / max_volume,
                        linewidths=0
                        )

    ax.set_title(f'Data for {ticker}', loc='left', pad=9)
    ax.set_xlim(right=iteration + scale / 5)
    if zoom is True:
        ax.set_ylim(data[-1][0] - (data[-1][0] / 1370), data[-1][0] + (data[-1][0] / 1370))
    plt.show()


def order(ticker, key, buy, order_size, safety):
    if safety is False:
        if buy:
            key.place_order(config.account_id, tda.orders.equities.equity_buy_market(ticker, order_size))
        else:
            key.place_order(config.account_id, tda.orders.equities.equity_sell_market(ticker, order_size))


def streamPrice(ticker, key):
    dictionary = json.loads(json.dumps(key.get_quotes(f'{ticker}').json()))
    while True:
        try:
            return dictionary[f'{ticker}']['regularMarketLastPrice']
        except KeyError:
            continue


async def stream():
    await stream_client.login()
    await stream_client.quality_of_service(StreamClient.QOSLevel.EXPRESS)
    stream_client.add_nasdaq_book_handler(order_book_handler)
    await stream_client.nasdaq_book_subs([ticker])

    while True:
        await stream_client.handle_message()


key = authenticate()
iteration, bids, asks, data, volumes, times, bid_wa, ask_wa = 0, [], [], [], [], [], [], []
stream_client = StreamClient(easy_client(api_key=config.api_key, redirect_uri=config.redirect_uri, token_path=config.token_path), account_id=config.account_id)
fig, ax = plt.subplots()
fig.set_size_inches(10, 6)
fig.show()


def order_book_handler(msg):
    global iteration, bids, asks, data, volumes, bid_wa, ask_wa
    iteration += 1
    print(f'Iteration: {iteration}')

    bid_snapshot, ask_snapshot = [], []

    dictionary = json.loads(json.dumps(msg))
    for bid_bucket in dictionary['content'][0]['BIDS']:
        bid_snapshot.append([bid_bucket['BID_PRICE'], bid_bucket['TOTAL_VOLUME'], iteration])
        volumes.append(bid_bucket['TOTAL_VOLUME'])
    for ask_bucket in dictionary['content'][0]['ASKS']:
        ask_snapshot.append([ask_bucket['ASK_PRICE'], ask_bucket['TOTAL_VOLUME'], iteration])
        volumes.append(ask_bucket['TOTAL_VOLUME'])

    # TODO: DOES THIS WORK?
    # bid_wa.append(sum([b[0] * b[1] for b in bid_snapshot]) / sum([b[1] for b in bid_snapshot]) if bid_snapshot else None)
    # ask_wa.append(sum([a[0] * a[1] for a in ask_snapshot]) / sum([a[1] for a in ask_snapshot]) if ask_snapshot else None)

    current_price = streamPrice(ticker, key)

    bids.append(bid_snapshot)
    asks.append(ask_snapshot)
    data.append([current_price, iteration])

    bids, asks, data = bids[-scale:], asks[-scale:], data[-scale:]
    try:
        graph((max(volumes)))
    except ValueError:
        pass


asyncio.run(stream())
