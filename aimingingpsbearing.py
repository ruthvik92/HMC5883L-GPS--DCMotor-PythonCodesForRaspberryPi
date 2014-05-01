import RPi.GPIO as gpio
import smbus
import time
import math
import os
import serial
from math import degrees, atan2
gpio.setmode(gpio.BOARD)
gpio.setup(7,gpio.OUT)
gpio.setup(11,gpio.OUT)
gpio.setup(13,gpio.OUT)
gpio.setup(15,gpio.OUT)
gpio.setup(16,gpio.OUT)
gpio.setup(18,gpio.OUT)
########### function to calculate the present bearing position of the vehicle.
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

##########function to calculate present GPS coordinates.
def get_present_gps():    
    ser=serial.Serial('/dev/ttyAMA0',9600)
    ser.open()
                    # open a file to write gps data
    f = open('/home/pi/Desktop/gps1', 'w')
    data=ser.read(128) # read 1024 bytes
    f.write(data) #write data into file
    f.flush() #flush from buffer into os buffer
         #ensure to write from os buffers(internal) into disk
    f = open('/home/pi/Desktop/gps1', 'r')# fetch  the required file
    for line in f.read().split('\n'):
        if line.startswith('$GPGGA'):
            lat, _, lon= line.split(',')[2:5]
            try:
                lat=float(lat)
                lon=float(lon)
                a=[lat,lon]
                return a
            except:
                pass
####### #function to calculate present GPS coordinates ends here.
x=float(raw_input('x:'))
y=float(raw_input('y:'))
b=get_present_gps()
centre_x=b[0]/100
centre_y=b[1]/100
#########function to calculate bearing that is between destination and home
def gb(x,y,centre_x, centre_y): 
    angle=degrees(atan2(y-centre_y,x-centre_x))
    bearing1=(angle+360)%360
    return bearing1
######## function that will set the vehicle in the direction(bearing) of destination.
def rotate():
    d=gb(x,y,centre_x, centre_y)
    a=get_bearing()
    if (a-d>=0 and a-d<=1):
        gpio.output(7,False)
        gpio.output(11,False)
        gpio.cleanup()
    elif(d-a<=0 and d-a>=-1):
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
        
    
