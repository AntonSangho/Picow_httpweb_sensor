import matplotlib.pyplot as plt
import numpy as np

# Read the data from the file
data = np.loadtxt('sensor_log.txt')

# Extract the x-axis and y-axis data
#x = data[:, 0]
y1 = data[:, 1]
#y2 = data[:, 2]
y3 = data[:, 3]

# Create a custom x-axis array to represent time in hours
x = np.zeros(len(y1))
current_time = 0
for i in range(len(x)):
    if i<6:
        x[i] = 1
        #current_time +=1 # 1-hour internvals for the first 6 points
    else:
        x[i] = i
        #current_time +=1
    #x[i] = current_time

# Create the plot
plt.figure(figsize=(15, 8))

plt.plot(x, y1, label='indoor', marker='o')
#plt.plot(x, y2, label='y2', marker='x')
plt.plot(x, y3, label='outdoor', marker='s')

# Add labels and title
plt.xlabel('Time(Hours)')
plt.ylabel('Temperature')
plt.title('Data Plot with Indoor and Outdoor temperature')

# Add a legend
plt.legend()

# Show the plot
plt.show()

