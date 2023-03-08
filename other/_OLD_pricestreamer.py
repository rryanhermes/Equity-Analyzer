from other import _OLD_functions
import time
import matplotlib.pyplot as plt

key = _OLD_functions.authenticate()
ticker = _OLD_functions.chooseStock()[0]

periods = 1000
scale = 40
average_length = 20
order_size = 1
safety = True

in_position, current_position, pl, checkpoint = False, 0, 0, 0
data, buys, sells = [], [], []
fig, (ax1, ax2) = plt.subplots(2, 1, height_ratios=[2, 1])
fig.show()

for iteration in range(periods):
    start_time = time.time()
    current_time = iteration
    current_price = _OLD_functions.streamPrice(ticker, key)
    data.append([current_time, current_price])
    average = _OLD_functions.streamAverage(data, average_length)
    data[-1].append(_OLD_functions.streamAverage(data, average_length))

    if iteration > average_length and current_price > average and in_position is False:
        _OLD_functions.buy(ticker, key, order_size, safety)
        buys.append([current_time, current_price])
        checkpoint, current_position, in_position = pl, current_price, True
    elif iteration > average_length and average >= current_price and in_position is True:
        _OLD_functions.sell(ticker, key, order_size, safety)
        sells.append([current_time, current_price])
        pl, in_position = checkpoint + pl, False
    elif iteration == periods and in_position is True:
        _OLD_functions.sell(ticker, key, order_size, safety)
        sells.append([current_time, current_price])
        data[-1].append(checkpoint + pl)
        in_position = False
        break
    if in_position is True:
        pl = (current_price - current_position) * order_size
        data[-1].append(checkpoint + pl)
    elif in_position is False:
        # placeholder
        data[-1].append(pl)

    data = data[-scale:]

    _OLD_functions.graphMain(ticker, fig, ax1, ax2, iteration, scale, data, average_length, buys, sells, pl)
    _OLD_functions.sleep(start_time, iteration)