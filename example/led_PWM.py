from machine import Pin, PWM
import time
 
pwm = PWM(Pin(4))
 
pwm.freq(1000)
 
duty = 0
direction = 1
 
while True:
    duty += direction
 
    if duty > 255:
        duty = 255
        direction = -1
    elif duty < 0:
        duty = 0
        direction = 1
 
    pwm.duty_u16(duty*duty)
    time.sleep(0.001)
