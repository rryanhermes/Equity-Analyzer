import matplotlib.pyplot as plt



prices = []

iteration = 0

with open('optionsdata.txt', 'r') as file:
    for moment in file:
        prices.append([moment[8:12], moment[20:31], iteration])
        iteration += 1

maxes = []
print(prices)

plt.plot([price[2] for price in prices], [price[0] for price in prices])


plt.show()

# print(prices)
# for item in prices:
#     maxes.append((item[0]))
#
# x = (max(maxes))
# item_index = prices.index(x)
# print(item_index)
# print(prices)