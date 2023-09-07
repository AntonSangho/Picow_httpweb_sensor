from machine import Pin, I2C
import utime
from pcf8523 import PCF8523

# Initialize I2C
i2c = I2C(scl=Pin(13), sda=Pin(12))  # Adjust pins as needed

# Initialize PCF8523
rtc = PCF8523(i2c)

# Set the time (Year, Month, Day, Hour, Minute, Second)
rtc.set_time(2023, 9, 7, 12, 0, 0)

# Function to simulate sensor reading
def read_sensor():
    utime.sleep_ms(50)  # Simulate a 50 ms delay for reading the sensor

# Record the start time
start_time = utime.ticks_ms()

# Collect sensor data
read_sensor()

# Record the finish time
finish_time = utime.ticks_ms()

# Calculate elapsed time
elapsed_time = utime.ticks_diff(finish_time, start_time)

# Get the current time from the RTC
current_time = rtc.get_time()

print("Start Time:", start_time, "ms")
print("Finish Time:", finish_time, "ms")
print("Elapsed Time:", elapsed_time, "ms")
print("Current RTC Time:", current_time)

