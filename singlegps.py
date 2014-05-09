import os
import serial
def get_present_gps():
    ser=serial.Serial('/dev/ttyAMA0',9600)
    ser.open()
                    # open a file to write gps data
    f = open('/home/pi/Desktop/gps1', 'w')
    data=ser.read(512) # read 1024 bytes
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
                
                print lat
                print lon
                a=[lat,lon]
                print a[0]
                print a
            except:
                pass
get_present_gps()
