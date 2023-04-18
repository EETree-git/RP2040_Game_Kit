#导入所需类
from machine import Pin


#定义第4引脚为led，设置为输出模式
led = Pin(4, Pin.OUT)

#引脚赋值为高电平，即可点亮led
led.value(1)