import matplotlib.pyplot as plt
import market_data2
from statistics import median as stats_median
import statistics

# Adjustable settings below
start = 400
end = 500
zoom = True
set_trim = .1

show_depth = True
calculate_mean = True
calculate_means = True
calculate_median = True
calculate_medians = True

# Calculation functions for later
def trimValues(trim):
    valid_asks, valid_bids = [], []

    for ask in ask_snapshot:
        if ask[0] < (current_price + trim):
            valid_asks.append(ask)
    for bid in bid_snapshot:
        if bid[0] > (current_price - trim):
            valid_bids.append(bid)

    return valid_asks, valid_bids

def calculateMean(trim):
    valid_asks, valid_bids = trimValues(trim)
    weighted_sum = 0
    total_weight = 0

    for ask in valid_asks:
        number, weight = ask[0], ask[1]
        weighted_sum += number * weight
        total_weight += weight
    for bid in valid_bids:
        number, weight = bid[0], bid[1]
        weighted_sum += number * weight
        total_weight += weight

    try:
        all_mean = weighted_sum / total_weight
        all_means.append(all_mean)
    except ZeroDivisionError:
        all_mean = all_means[1]
        all_means.append(all_mean)

    return all_mean
def calculateMeans(trim):
    valid_asks, valid_bids = trimValues(trim)
    weighted_sum_bids, weighted_sum_asks = 0, 0
    total_weight_bids, total_weight_asks = 0, 0

    for ask in valid_asks:
        number, weight = ask[0], ask[1]
        weighted_sum_asks += number * weight
        total_weight_asks += weight
    for bid in valid_bids:
        number, weight = bid[0], bid[1]
        weighted_sum_bids += number * weight
        total_weight_bids += weight

    try:
        ask_mean = weighted_sum_asks / total_weight_asks
        ask_means.append(ask_mean)
    except ZeroDivisionError:
        ask_mean = ask_means[-1]
        ask_means.append(ask_mean)
    try:
        bid_mean = weighted_sum_bids / total_weight_bids
        bid_means.append(bid_mean)
    except ZeroDivisionError:
        bid_mean = bid_means[-1]
        bid_means.append(bid_mean)

    return ask_mean, bid_mean
def calculateMedian(trim):
    valid_asks, valid_bids = trimValues(trim)
    combine = []

    for ask in valid_asks:
        combine.append(ask[0])
    for bid in valid_bids:
        combine.append(bid[0])

    try:
        all_median = stats_median(combine)
        all_medians.append(all_median)
    except statistics.StatisticsError:
        all_median = current_price
        ask_medians.append(all_medians[-1])

    return all_median
def calculateMedians(trim):
    valid_asks, valid_bids = trimValues(trim)
    asks, bids = [], []

    for ask in valid_asks:
        asks.append(ask[0])
    for bid in valid_bids:
        bids.append(bid[0])

    try:
        ask_median = stats_median(asks)
        ask_medians.append(ask_median)
    except statistics.StatisticsError:
        ask_median = all_medians[-1]
        ask_medians.append(ask_median)
    try:
        bid_median = stats_median(bids)
        bid_medians.append(bid_median)
    except statistics.StatisticsError:
        bid_median = bid_medians[-1]
        bid_medians.append(bid_median)

    return ask_median, bid_median

# Preparing data
data = market_data2.data[start:end]
all_means, ask_means, bid_means = [], [], []
all_medians, ask_medians, bid_medians = [], [], []
trim_visualiser, times, highest_volume = [], [], 0

# Begin the loop
for iteration in data:
    try:
        # Gather iteration specific, consolidated data
        current_price = iteration[0][0]
        current_time = iteration[0][1]
        ask_snapshot = iteration[1]
        bid_snapshot = iteration[2]

        # Calculations
        if calculate_mean:
            all_mean = calculateMean(set_trim)
        if calculate_means:
            ask_mean, bid_mean = calculateMeans(set_trim)
        if calculate_median:
            all_median = calculateMedian(set_trim)
        if calculate_medians:
            ask_median, bid_median = calculateMedians(set_trim)

    except IndexError:
        break

# Search for highest volume value
for x in data:
    ask_snapshot = x[1]
    bid_snapshot = x[2]
    for ask in ask_snapshot:
        if ask[1] > highest_volume:
            highest_volume = ask[1]
    for bid in bid_snapshot:
        if bid[1] > highest_volume:
            highest_volume = bid[1]

# Fill the area representing trim
for y in data:
    price = y[0][0]
    trim_visualiser.append([price + set_trim, price - set_trim])

# Generate a list of times
for z in data:
    times.append(z[0][1])
    # placeholder

# Create the plot
fig, ax = plt.subplots()
fig.set_size_inches(10, 6)
ax.set_facecolor('whitesmoke')
fig.show()
if zoom:
    last = data[-1][0][0]
    ax.set_ylim(last - last / 1370, last + last / 1370)

# Plot lines
ax.plot(times, [p[0][0] for p in data], color='black', linewidth='2')
ax.fill_between([i[0][1] for i in data], [p[0] for p in trim_visualiser], [p[1] for p in trim_visualiser], color='white')
if calculate_mean:
    ax.plot(times, all_means, color='olive')
    # placeholder
if calculate_means:
    ax.plot(times, ask_means, color='cornflowerblue')
    ax.plot(times, bid_means, color='darkorange')
if calculate_median:
    ax.plot(times, all_medians, color='purple')
    # placeholder
if calculate_medians:
    ax.plot(times, ask_medians, color='cornflowerblue')
    ax.plot(times, bid_medians, color='darkorange')

# Plot market depth
if show_depth:
    biggest_volume = highest_volume
    for iteration in data:
        time = iteration[0][1]
        ask_snap = iteration[1]
        for ask in ask_snap:
            plt.scatter(time,
                        ask[0],
                        color='red',
                        marker='v',
                        edgecolors='white',
                        alpha=ask[1] / highest_volume,
                        linewidths=0
                        )
    for iteration in data:
        time = iteration[0][1]
        bid_snap = iteration[2]
        for bid in bid_snap:
            plt.scatter(time,
                        bid[0],
                        color='green',
                        marker='^',
                        edgecolors='white',
                        alpha=bid[1] / highest_volume,
                        linewidths=0
                        )

# Plot!
plt.show()
