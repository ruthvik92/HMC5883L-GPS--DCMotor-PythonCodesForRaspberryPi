import RPi.GPIO as gpio
import smbus
import time
import math
gpio.setmode(gpio.BOARD)
gpio.setup(7,gpio.OUT)
gpio.setup(11,gpio.OUT)
gpio.setup(13,gpio.OUT)
gpio.setup(15,gpio.OUT)
gpio.setup(16,gpio.OUT)
gpio.setup(18,gpio.OUT)
def get_bearing():
    bus=smbus.SMBus(1)
    address=0x1e
    def read_byte(adr):
        return bus.read_byte_data(address, adr)
    def read_word(adr):
        high = bus.read_byte_data(address, adr)
        low = bus.read_byte_data(address, adr+1)
        val = (high<< 8) +low
        return val
    def read_word_2c(adr):
        val = read_word(adr)
        if (val>=0x8000):
            return -((65535-val)+1)
        else:
            return val
    def write_byte(adr,value):
        bus.write_byte_data(address, adr, value)
    write_byte(0, 0b01110000)
    write_byte(1, 0b00100000)
    write_byte(2, 0b00000000)
    scale = 0.92
    x_offset = -10
    y_offset = 10
    x_out = (read_word_2c(3)- x_offset+2) * scale
    y_out = (read_word_2c(7)- y_offset+2)* scale
    z_out = read_word_2c(5) * scale
    bearing = math.atan2(y_out, x_out)+.45
    if (bearing<0):
        bearing +=2*math.pi
        return math.degrees(bearing)
    else:
        return math.degrees(bearing)
def rotate():
    a=get_bearing()
    if (a>=0 and a<=1):
        gpio.output(7,False)
        gpio.output(11,False)
        gpio.cleanup()
    elif(a>=358 and a<=360):
        gpio.output(7,False)
        gpio.output(11,False)
        gpio.cleanup()
    else:
        gpio.setup(18,False)
        gpio.setup(16,False)
        time.sleep(.2)
        gpio.output(7,False)
        gpio.output(11,True)
        p=gpio.PWM(11,80)
        p.start(1)
        time.sleep(.2)
        gpio.setup(13,False)
        gpio.setup(15,False)
        gpio.setup(16,True)
        gpio.setup(18,False)
        p.ChangeDutyCycle(50)
        rotate()
rotate()
        
    
