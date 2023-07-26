import asyncio
import json
from tda.auth import easy_client
from tda.streaming import StreamClient
import resources.config as config
from other import _OLD_functions
import matplotlib.pyplot as plt
import time

key = _OLD_functions.authenticate()
ticker = _OLD_functions.chooseStock()[0]

periods = 5
scale = 19
order_size = 1
safety = True

# TODO: NEW DATA TYPES?
iteration, bids, asks, data, volumes = 0, [], [], [], []

client = easy_client(api_key=config.api_key, redirect_uri=config.redirect_uri, token_path=config.token_path)
stream_client = StreamClient(client, account_id=config.account_id)
fig, ax = plt.subplots(figsize=(7, 5))
fig.show()


async def stream():
    await stream_client.login()
    await stream_client.quality_of_service(StreamClient.QOSLevel.FAST)
    # await stream_client.quality_of_service(StreamClient.QOSLevel.EXPRESS)
    stream_client.add_nasdaq_book_handler(order_book_handler)
    await stream_client.nasdaq_book_subs([ticker])

    for i in range(periods + 1):
        await stream_client.handle_message()
        # TODO: TEST WHAT HAPPENS IF STREAM TAKES OVER A SECOND (OR WHATEVER SPEED)


def order_book_handler(msg):
    start_time = time.time()
    global iteration, bids, asks, data, volumes
    bid_snapshot, ask_snapshot = [], []
    iteration += 1
    current_price = _OLD_functions.streamPrice(ticker, key)
    print('-----------------------------------------------------------')
    print(f'Iteration: {iteration}')
    print('-----------------------------------------------------------')

    dictionary = json.loads(json.dumps(msg))
    for bid_bucket in dictionary['content'][0]['BIDS']:
        bid_snapshot.append([bid_bucket['BID_PRICE'], bid_bucket['TOTAL_VOLUME'], iteration])
        volumes.append(bid_bucket['TOTAL_VOLUME'])
    for ask_bucket in dictionary['content'][0]['ASKS']:
        ask_snapshot.append([ask_bucket['ASK_PRICE'], ask_bucket['TOTAL_VOLUME'], iteration])
        volumes.append(ask_bucket['TOTAL_VOLUME'])

    bids.append(bid_snapshot)
    asks.append(ask_snapshot)
    data.append([current_price, iteration])
    bids, asks, data = bids[-scale:], asks[-scale:], data[-scale:]

    max_volume = max(volumes)
    _OLD_functions.liveGraphLevel2(ticker, ax, fig, max_volume, bids, asks, data, current_price, iteration, scale)

    print(f'    Time elapsed: {time.time() - start_time}')


asyncio.run(stream())

print(f'''FINAL DATA:
Bids: {bids}
    Asks: {asks}
        Data: {data}
            Volumes: {volumes}
''')

max_volume = max(volumes)

print('creating figure')
fig, (ax1, ax2) = plt.subplots(1, 2)

print('plotting price')
ax1.plot([i[1] for i in data], [p[0] for p in data], color='black')

print('plotting asks & bids')
for ask_set in asks:
    for ask in ask_set:
        ax1.scatter(ask[2], ask[0],
                    marker='s',
                    s=300,
                    color='red',
                    alpha=ask[1] / max_volume)

for bid_set in bids:
    for bid in bid_set:
        ax1.scatter(bid[2], bid[0],
                    marker='s',
                    s=300,
                    color='green',
                    alpha=bid[1] / max_volume)

print('setting settings')
ax1.set_title(f'Data for {ticker}', loc='left', pad=9)
# ax.grid(axis='y')
ax1.set_xlim(left=max(1, iteration - scale + 1), right=iteration + scale / 5)
# fig.canvas.flush_events()
# fig.canvas.draw()
print('showing')
fig.show()


time.sleep(10)