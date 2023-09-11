import time 
import board
import sdcardio
import storage
import busio
import adafruit_pcf8523
from adafruit_ds18x20 import DS18X20
from adafruit_onewire.bus import OneWireBus
import adafruit_ahtx0
import digitalio

# Initialize PCF8523 RTC on I2C bus connected to GP5 and GP4
I2C = busio.I2C(board.GP5, board.GP4)    # dc18b20
rtc = adafruit_pcf8523.PCF8523(I2C)

ow_bus = OneWireBus(board.GP6)
# Scan for sensors and grab the first one found.
ds18 = DS18X20(ow_bus, ow_bus.scan()[0])
aht = adafruit_ahtx0.AHTx0(I2C)

# Initialize button on GPIO 15
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Initiallize slide switch on GPIO 20
switch = digitalio.DigitalInOut(board.GP20)

# Initialize LED on GPIO 14
led = digitalio.DigitalInOut(board.GP14)
led.direction = digitalio.Direction.OUTPUT

# Variable to keep track of recording state
recording = False

days = ("Sunday", "Monday", "Tuesday", "Wednesday","Thursday","Friday","Saturday")

#SPI SD_CS pin
SD_CS = board.GP17

#SPI setup for SD card
spi = busio.SPI(board.GP18, board.GP19, board.GP16)
sdcard = sdcardio.SDCard(spi, SD_CS)
vfs = storage.VfsFat(sdcard)
try:
    storage.mount(vfs, "/sdcard")
    print("sd card mounted")
except ValueError:
    print("no SD card")

# change to True if you want to write the time!
set_time = False
#set_time = True

initial_time = time.monotonic()
print("initial_time:", end="")
print(initial_time)

if set_time:
    t = time.struct_time((2023, 09, 11, 18, 21, 00, 1, -1, -1))
    print("Setting time to :", t)
    rtc.datetime = t
    print()
    # initial write to the SD card on startup 
    try:
        with open("/sdcard/temp.txt", "a") as f:
            # write the date
            t = rtc.datetime
            f.write('The date is {} {}/{}/{}\n'.format(days[t.tm_wday],t.tm_mon, t.tm_mday, t.tm_year))
            # write the start time
            f.write('Time, Temp\n')
            # debug statement for REPL
            print("initial write to SD card complete, starting to log")
    except ValueError:
        print("initial write to SD card failed - check card")

last_minute = -1  # Variable to store the last minute value
last_check_time = 0  # Time at which we last checked the minute
check_interval = 1  # Check every 1 second

logging_interval = 10

last_logged_timestamp = -logging_interval  # Initialize to a value to ensure the first log happens

while True:
 
    if switch.value: 
        led.value = True

        current_timestamp = time.monotonic()
 
        if (current_timestamp - last_logged_timestamp) >= logging_interval:
            #last_logged_minute = current_minute # Update last logged minutes
            last_logged_timestamp = current_timestamp  # Update last logged timestamp
            
            try:
                rtc_time = rtc.datetime
                with open("/sdcard/temp.txt", "a") as f:
                    outdoor_temp = ds18.temperature
                    indoor_temp = aht.temperature
                    #time_stamp = current_minute
                    time_stamp = "{}:{}:{}".format(rtc_time.tm_hour, rtc_time.tm_min, rtc_time.tm_sec)
                    #f.write('{}, {}, {}\n'.format(int(time_stamp), outdoor_temp, indoor_temp))
                    f.write('{}, {}, {}\n'.format(time_stamp, outdoor_temp, indoor_temp))
                    print("Data wirtten to SD card.")
            except ValueError:
                print("Data error - cannot write to SD card.")
    else:
        led.value = False
        time.sleep(0.2)  # Debounce time

