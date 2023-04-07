import matplotlib.pyplot as plt
import numpy as np

# Generate some data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a figure and axis object
fig, ax1 = plt.subplots()

# Plot the data
ax1.plot(x, y, 'b-')

# Set labels and colors for the first axis
ax1.set_xlabel('X-axis')
ax1.set_ylabel('Y-axis 1', color='b')
ax1.tick_params('y', colors='b')

# Create a twin axis object
ax2 = ax1.twinx()

# Set labels and colors for the second axis
ax2.set_ylabel('Y-axis 2', color='r')
ax2.tick_params('y', colors='r')

# Hide the ticks and spines for the second axis
ax2.spines['right'].set_visible(False)
ax2.tick_params(axis='y', which='both', length=0)

plt.show()
