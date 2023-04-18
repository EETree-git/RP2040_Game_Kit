#导入所需类
from machine import Pin, I2C
import time
import struct

#导入mma7660驱动文件
import mma7660

#定义引脚
sda=Pin(10)
scl=Pin(11)

#配置I2C协议对应引脚及频率
mma7660=machine.I2C(1,sda=sda,scl=scl,freq=400000)
#配置mma7660
mma7660.writeto_mem(76,7,b'1')

#循环读取数值，并打印
while True:
        #从mma7660寄存器中读取三轴数据
        x=mma7660.readfrom_mem(76,0,8)
        y=mma7660.readfrom_mem(76,1,8)
        z=mma7660.readfrom_mem(76,2,8)
        #更改数据格式
        xout=struct.unpack('<h',x)[0]
        yout=struct.unpack('<h',y)[0]
        zout=struct.unpack('<h',z)[0]
        #打印
        print(xout,yout,zout)
        


