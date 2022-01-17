### mouse-test.py --- test joystick with mouse hid, for mpy.
## author: picospuch

from hid import Mouse
from machine import Pin, ADC
from time import sleep
from button import button

a = button(6)

xAxis = ADC(Pin(28))
yAxis = ADC(Pin(29))

buttonB = Pin(5,Pin.IN, Pin.PULL_UP) #B
buttonA = Pin(6,Pin.IN, Pin.PULL_UP) #A
buttonStart = Pin(7,Pin.IN, Pin.PULL_UP) 
buttonSelect = Pin(8,Pin.IN, Pin.PULL_UP)

m = Mouse()

t = 1
while True:
    xValue = xAxis.read_u16() # ^ dec, v inc
    yValue = yAxis.read_u16() # <- dec, -> inc
    
    x = y = 0
    if xValue < 15000:
        y = -5
    elif xValue > 45000:
        y = +5
    elif yValue < 15000:
        x = -5
    elif yValue > 45000:
        x = +5
    if a.value():
        t = -t
    if t == 1:
        print("hello")
    elif t == -1:
        print("world")
    m.move(x, y)
    sleep(0.1)
