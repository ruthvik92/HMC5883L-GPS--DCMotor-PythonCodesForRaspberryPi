import smbus
import time
import math
bus = smbus.SMBus(1)
address = 0x1e
def read_byte(adr):
    return bus.read_byte_data(address, adr)
def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high<< 8) + low
    return val
def read_word_2c(adr):
    val = read_word(adr)
    if (val>= 0x8000):
        return -((65535 - val)+1)
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

bearing = math.atan2(y_out, x_out)+.48
if(bearing < 0):
    bearing += 2* math.pi
print "Bearing:", math.degrees(bearing)
# added an extra file to check if it appears on git
