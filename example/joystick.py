from machine import Pin, ADC
import utime

xAxis = ADC(Pin(28))
yAxis = ADC(Pin(29))

buttonB = Pin(25,Pin.IN, Pin.PULL_UP) #B
buttonA = Pin(6,Pin.IN, Pin.PULL_UP) #A
buttonStart = Pin(7,Pin.IN, Pin.PULL_UP) #A
buttonSelect = Pin(8,Pin.IN, Pin.PULL_UP) #A

while True:
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    buttonValueA = buttonA.value()
    buttonValueB = buttonB.value()
    buttonValueStart = buttonStart.value()
    buttonValueSelect = buttonSelect.value()
    print(str(xValue) +", " + str(yValue) + " -- " + str(buttonValueA) + " -- "+ str(buttonValueB)+ " -- " + str(buttonValueStart)+ " -- " + str(buttonValueSelect))
    utime.sleep(0.01)