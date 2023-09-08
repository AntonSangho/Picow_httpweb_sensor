import time 
import board
import sdcardio
import storage
import busio
#import adafruit_dht
import adafruit_pcf8523
from adafruit_ds18x20 import DS18X20
from adafruit_onewire.bus import OneWireBus
import adafruit_ahtx0
import digitalio

# Initialize PCF8523 RTC on I2C bus connected to GP5 and GP4
I2C = busio.I2C(board.GP5, board.GP4)    # dc18b20
rtc = adafruit_pcf8523.PCF8523(I2C)

# Initialize AHT20 sensor on a different I2C bus connected to GP1 and GP0
#i2c_aht = busio.I2C(board.GP1, board.GP0)    # aht20
#aht = adafruit_ahtx0.AHTx0(I2C)


#dht = adafruit_dht.DHT22(board.GP15)
ow_bus = OneWireBus(board.GP6)
# Scan for sensors and grab the first one found.
ds18 = DS18X20(ow_bus, ow_bus.scan()[0])
aht = adafruit_ahtx0.AHTx0(I2C)

# Initialize button on GPIO 15
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

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

#set_time = False
set_time = True 

initial_time = time.monotonic()


if set_time:
    t = time.struct_time((2023, 9, 8, 18, 10, 00, 1, -1, -1))
    print("Setting time to :", t)
    rtc.datetime = t
    print()

# while True:
#     t = rtc.datetime
#     #print(t)
# 
#     #print("The data is %s %d/%d/%d" % (days[t.tm_wday], t.tm_mon, t.tm_mday, t.tm_year))
#     #print("The time is %d:%02d%02d" % (t.tm_hour, t.tm_min, t.tm_sec))
#     
#     time.sleep(1)

def get_temp(sensor):
    #temperature = dht.temperature
    temperature = ds18.temperature
    #temperature = aht.temperature
    return temperature

# initial write to the SD card on startup 
try:
    with open("/sdcard/temp.txt", "a") as f:
        # write the date
        f.write('The date is {} {}/{}/{}\n'.format(days[t.tm_wday],t.tm_mon, t.tm_mday, t.tm_year))
        # write the start time
        f.write('Time, Temp\n')
        # debug statement for REPL
        print("initial write to SD card complete, starting to log")
except ValueError:
    print("initial write to SD card failed - check card")

while True:
    # Check if button is pressed
    if not button.value:
        recording = not recording  # Toggle recording state
        led.value = recording  # Turn LED on or off based on recording state
        time.sleep(0.2)  # Debounce time

    if recording:
        try:
            t = rtc.datetime
            with open("/sdcard/temp.txt", "a") as f:
                outdoor_temp = ds18.temperature  # Outdoor temperature from DS18B20
                indoor_temp = aht.temperature  # Indoor temperature from AHT20
                print(f"Outdoor Temp: {outdoor_temp}, Indoor Temp: {indoor_temp}")
                
                # RTC
                current_time = time.monotonic()
                time_stamp = current_time - initial_time
                print("Seconds since current data log started:", int(time_stamp))
                
                f.write(' {},{},{}\n'.format(int(time_stamp), outdoor_temp, indoor_temp))
                print("data written to sd card ")
            
            # Sleep for 10 minutes, but check the button every second
            for _ in range(600):  # 600 seconds = 10 minutes
                if not button.value:
                    recording = not recording  # Toggle recording state
                    led.value = recording  # Turn LED on or off based on recording state
                    time.sleep(0.2)  # Debounce time
                    break  # Exit the for loop if button is pressed
                time.sleep(1)  # Sleep for 1 second
        except ValueError:
            print("data error - cannot write to SD card")
            time.sleep(10)
    else:
        # If not recording, just check the button state
        if not button.value:
            recording = not recording  # Toggle recording state
            led.value = recording  # Turn LED on or off based on recording state
            time.sleep(0.2)  # Debounce time
        time.sleep(1)


