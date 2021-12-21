from machine import Pin,PWM
import time

pwm = PWM(Pin(15))

pwm.freq(50)

control = machine.ADC(2)

while True:

    for _ in range(100):

        pwm.duty_u16(3276)
        time.sleep(1)

        pwm.duty_u16(6553)
        time.sleep(1)
'''
    # 摇杆上下摇动控制舵机
    adc = control.read_u16()
    duty = int(adc * (6553-3276)/0xffff) + 3276
    pwm.duty_u16(duty)

    time.sleep(0.5)
'''