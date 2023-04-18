#导入所需类
from machine import Pin,ADC
import utime

#定义引脚
xAxis = ADC(Pin(28))
yAxis = ADC(Pin(29))

#循环读取ADC值，并打印
while True:
    #读取ADC值
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    
    #打印ADC值
    print(str(xValue) +", " + str(yValue) )
    utime.sleep(0.01)