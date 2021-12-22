from machine import Pin,Timer
from time import sleep_us

led = Pin(4, Pin.OUT)

tim = Timer()

def tick(timer):
    global led
    led.toggle()

tim.init(period=100, mode=Timer.PERIODIC, callback=tick)