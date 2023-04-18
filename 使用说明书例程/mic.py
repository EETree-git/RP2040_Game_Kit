#导入所需类
from machine import Pin,PWM

#定义引脚
mic = machine.PWM(Pin(23))

#设置输出频率控制音调
mic.freq(200)

#设置占空比控制音量
mic.duty_u16(50)