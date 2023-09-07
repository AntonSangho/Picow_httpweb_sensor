import matplotlib.pyplot as plt
import numpy as np

# Read the data from the file
data = np.loadtxt('sensor_log.txt')

# Extract the x-axis and y-axis data
x = data[:, 0]
y1 = data[:, 1]
#y2 = data[:, 2]
y3 = data[:, 3]

# Create the plot
plt.figure(figsize=(15, 8))

plt.plot(x, y1, label='indoor', marker='o')
#plt.plot(x, y2, label='y2', marker='x')
plt.plot(x, y3, label='outdoor', marker='s')

# Add labels and title
plt.xlabel('time')
plt.ylabel('temperature')
plt.title('Data Plot')

# Add a legend
plt.legend()

# Show the plot
plt.show()

