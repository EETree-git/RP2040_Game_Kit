from machine import Pin,PWM
import time

mic = machine.ADC(1)

while True:
    adc = mic.read_u16()
    #duty = int(adc * (1024-0)/0xffff)
    print(adc)
    time.sleep(0.001)