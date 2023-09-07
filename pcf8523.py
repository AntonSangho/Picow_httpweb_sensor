from machine import I2C
import ustruct

class PCF8523:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr

    def set_time(self, year, month, day, hour, minute, second):
        data = ustruct.pack('7B', second, minute, hour, day, 0, month, year - 2000)
        self.i2c.writeto_mem(self.addr, 0x03, data)

    def get_time(self):
        data = self.i2c.readfrom_mem(self.addr, 0x03, 7)
        second, minute, hour, day, _, month, year = ustruct.unpack('7B', data)
        return (year + 2000, month, day, hour, minute, second)

