import matplotlib.pyplot as plt

# Generate x and y data
x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

# Define line weight values as a list
weights = [1, 2, 3, 4, 5]

# Create a plot with a gradient line
fig, ax = plt.subplots()
for i in range(len(x) - 1):
    alpha = weights[i] / max(weights)
    ax.plot(x[i:i+2], y[i:i+2], color='k', linewidth=2, alpha=alpha)

# Set the x and y limits of the plot
ax.set_xlim(min(x), max(x))
ax.set_ylim(min(y), max(y))

# Show the plot
plt.show()
