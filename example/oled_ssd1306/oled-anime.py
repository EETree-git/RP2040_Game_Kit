from machine import Pin, SPI, ADC
from ssd1306 import SSD1306_SPI
import framebuf
import time
from utime import sleep_ms
from board import pin_cfg
from astronaut import frames
 
spi = SPI(1, 100000, mosi=Pin(pin_cfg.spi1_mosi), sck=Pin(pin_cfg.spi1_sck))
oled = SSD1306_SPI(128, 64, spi, Pin(pin_cfg.spi1_dc),Pin(pin_cfg.spi1_rstn), Pin(pin_cfg.spi1_cs))

# Clear the oled display in case it has junk on it.

#xAxis = ADC(Pin(28))
#yAxis = ADC(Pin(29))

while True:
    for i in range(0, 48):
        #xValue = xAxis.read_u16()
        #yValue = yAxis.read_u16()
        #duty_x = int(xValue * (64)/0xffff)
        #duty_y = int(yValue * (128)/0xffff)
        oled.fill(0)
        fb = framebuf.FrameBuffer(frames[i], 64, 64, framebuf.MONO_HLSB)
        time.sleep_ms(40)
        oled.blit(fb, 0, 0)
        oled.show()



