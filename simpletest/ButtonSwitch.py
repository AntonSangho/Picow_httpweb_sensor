# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
"""CircuitPython Digital Input example for Feather RP2040"""
import board
import digitalio

# Initialize LED on GPIO 14
led = digitalio.DigitalInOut(board.GP14)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.GP7)
button.switch_to_input(pull=digitalio.Pull.UP)

while True:
    if not button.value:
        led.value = True
    else:
        led.value = False
