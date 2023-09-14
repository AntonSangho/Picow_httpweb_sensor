# Import modules for servo, INA219, and OLED
import time
import board
#import pwmio
#from adafruit_motor import servo
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

# Initialize INA219
i2c_bus = board.I2C()
ina219 = INA219(i2c_bus)

# Initialize OLED
displayio.release_displays()
oled_reset = board.D9
spi = board.SPI()
oled_cs = board.D5
oled_dc = board.D6
display_bus = displayio.FourWire(spi, command=oled_dc, chip_select=oled_cs, reset=oled_reset, baudrate=1000000)
WIDTH = 128
HEIGHT = 32
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)
splash = displayio.Group()
display.show(splash)

# Create text area for power consumption
#power_text = label.Label(terminalio.FONT, text="Power: ", color=0xFFFFFF, x=10, y=10)
#splash.append(power_text)

# Ceate text areas for voltage and currnet
voltage_text = label.Label(terminalio.FONT, text="Voltage: ", color=0xFFFFFF, x=10, y=5)
current_text = label.Label(terminalio.FONT, text="Current: ", color=0xFFFFFF, x=10, y=20)
splash.append(voltage_text)
splash.append(current_text)

while True:
    voltage = ina219.bus_voltage
    shunt_voltage = ina219.shunt_voltage
    #print(shunt_voltage)
    current = shunt_voltage / 0.1  # in Amperes
    
    # Update OLED display
    #power_text.text = f"Power: {power:.3f} W"
    voltage_text.text = f"Voltage: {voltage:.3f} V"
    current_text.text = f"Current: {current:.3f} A"
    

