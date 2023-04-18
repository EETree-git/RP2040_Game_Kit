#导入所需类
from machine import Pin
import utime

#定义按键引脚，并配置为输入上拉模式
buttonB = Pin(5,Pin.IN, Pin.PULL_UP)
buttonA = Pin(6,Pin.IN, Pin.PULL_UP)
buttonX = Pin(7,Pin.IN, Pin.PULL_UP) 
buttonY = Pin(8,Pin.IN, Pin.PULL_UP)

#编写循环程序，持续读取按键状态后打印
while True:
    #读取按键状态
    buttonValueA = buttonA.value()
    buttonValueB = buttonB.value()
    buttonValueX = buttonX.value()
    buttonValueY = buttonY.value()
    
    #打印显示按键状态
    print(str(buttonValueA) + " -- "+ str(buttonValueB)+ " -- " + str(buttonValueX)+ " -- " + str(buttonValueY))
    utime.sleep(0.01)
