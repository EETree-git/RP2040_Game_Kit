from machine import Pin, SPI
from ssd1306 import SSD1306_SPI
import framebuf
import time
from utime import sleep_ms
from board import pin_cfg
from astronaut import frames
 
spi = SPI(1, 100000, mosi=Pin(pin_cfg.spi1_mosi), sck=Pin(pin_cfg.spi1_sck))
oled = SSD1306_SPI(128, 64, spi, Pin(pin_cfg.spi1_dc),Pin(pin_cfg.spi1_rstn), Pin(pin_cfg.spi1_cs))

# Clear the oled display in case it has junk on it.
oled.fill(0)

while True:
    for i in range(0, 48):
        fb = framebuf.FrameBuffer(frames[i], 64, 64, framebuf.MONO_HLSB)
        time.sleep_ms(40)
        oled.blit(fb, 0, 0)
        oled.show()
