import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BOARD)
gpio.setup(7,gpio.OUT)
gpio.setup(11,gpio.OUT)
gpio.setup(13,gpio.OUT)
gpio.setup(15,gpio.OUT)
gpio.setup(16,gpio.OUT)
gpio.setup(18,gpio.OUT)
gpio.output(7,True)
gpio.output(11,True)
n=raw_input(" enter no of seconds")
try:
    while True:
        gpio.output(13,True)
        gpio.output(15,False)
        gpio.output(16,True)
        gpio.output(18,False)
        time.sleep(float(n))
        gpio.output(13,False)
        gpio.output(15,True)
        gpio.output(16,False)
        gpio.output(18,True)
        time.sleep(float(n))
except KeyboardInterrupt:
    pass
gpio.cleanup()
