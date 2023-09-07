import utime
from machine import Pin, I2C
import ahtx0
import os
import ds18x20
import onewire

# Initialize I2C and AHT20 sensor
# i2c = I2C(0, sda=Pin(0), scl=Pin(1))
# sensor = aht20.AHT20(i2c)
I2C_SDA_PIN = 0
I2C_SCL_PIN = 1
i2c=machine.I2C(0,sda=machine.Pin(I2C_SDA_PIN), scl=machine.Pin(I2C_SCL_PIN), freq=400000)
sensor = ahtx0.AHT20(i2c)
ds_pin = machine.Pin(16) # DS18B20 pin 
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()

button_presses = 0
last_time = 0
logging = False
log_file = None
log_count = 1
max_file_size = 1024  # 1023kbyte

led = machine.Pin(14, machine.Pin.OUT)
#builtin_led = machine.Pin("LED", machine.Pin.OUT)
button_pin = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)

def button_pressed_handler(pin):
    global button_presses, last_time, logging, log_file
    new_time = utime.ticks_ms()
    
    if (new_time - last_time) > 200:
        button_presses += 1
        last_time = new_time
        
        if logging:
            print("데이터 수집 종료")
            log_file.close()
            logging = False
            led.value(False)

        else:
            print("데이터 수집 시작")
            log_file = open("sensor_log.txt", "a")  # "a"는 파일을 추가 모드로 열기
            logging = True
            led.value(True)

button_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_pressed_handler)

while True:
    if logging:
        temperature = sensor.temperature
        humidity = sensor.relative_humidity
        ds_sensor.convert_temp()
        utime.sleep_ms(750)
        for rom in roms:
            outdoor_temp = ds_sensor.read_temp(rom)
            #print(rom)
            #print(outdoor_temp)
        #print(temperature)
        value1 = str(round(temperature, 2))
        value2 = str(round(humidity, 2))
        value3 = str(round(outdoor_temp,2))
        num = str(log_count)
        #print("num:"+ num)
        log_file.write(num+"\t"+value1+"\t"+value2+"\t"+value3+"\n")

        # 파일 사이즈 체크
        if log_file.tell() >= max_file_size*400:
            print("파일 사이즈 초과, 데이터 수집 종료")
            log_file.close()
            logging = False
            led.value(False)
        
        #utime.sleep_ms(1000)  # 1초마다 데이터 로깅
        utime.sleep_ms(600000)
        log_count += 1
    
    utime.sleep_ms(100)  # 불필요한 반복을 방지하기 위해 작은 지연
