#导入所需类
from sys import platform
import time
import gc
from machine import Pin, freq

#导入文件夹中的包
from ir_rx.print_error import print_error 
from ir_rx.nec import NEC_8, NEC_16, SAMSUNG
from ir_rx.sony import SONY_12, SONY_15, SONY_20
from ir_rx.philips import RC5_IR, RC6_M0
from ir_rx.mce import MCE

#定义ir接收引脚
ir_read = Pin(25, Pin.IN)

#callback子程序
def cb(data, addr, ctrl):
    if data < 0:  
        print("Repeat code.")
    else:
        print(r"Data 0x{data:02x} Addr 0x{addr:04x} Ctrl 0x{ctrl:02x}")

#初始化协议
classes = (NEC_8, NEC_16, SONY_12, SONY_15, SONY_20, RC5_IR, RC6_M0, MCE, SAMSUNG)
ir = classes[0](ir_read, cb)  
ir.error_function(print_error)  

#循环接收信号
while True:
    print("running")
    time.sleep(2)
    gc.collect()



