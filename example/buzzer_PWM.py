from machine import Pin,PWM
from time import sleep
pwm = PWM(Pin(23))
pwm.freq(50)
control = machine.ADC(2)

while True:
    adc = control.read_u16()
    duty = int(adc * (3000-0)/0xffff) 
    print(duty)
    pwm.freq(duty)
    pwm.duty_u16(400)
    sleep(0.04)