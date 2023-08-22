from machine import Pin
import time

adc = machine.ADC(Pin(26))

while True:# create ADC object on ADC pin
    print(adc.read_u16())
    time.sleep(1)
