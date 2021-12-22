from machine import Pin,PWM
import time

pwm = PWM(Pin(15))

pwm.freq(50)

control = machine.ADC(2)

while True:

    # 摇杆上下摇动控制舵机
    adc = control.read_u16()
    duty = int(adc * (6553-3276)/0xffff) + 3276
    pwm.duty_u16(duty)
    print(duty)
    time.sleep(0.5)
