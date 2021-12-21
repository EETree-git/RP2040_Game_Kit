from machine import Pin, SPI
from ssd1306 import SSD1306_SPI
import framebuf
from time import sleep
from utime import sleep_ms
from board import pin_cfg
 
spi = SPI(1, 100000, mosi=Pin(pin_cfg.spi1_mosi), sck=Pin(pin_cfg.spi1_sck))
oled = SSD1306_SPI(128, 64, spi, Pin(pin_cfg.spi1_dc),Pin(pin_cfg.spi1_rstn), Pin(pin_cfg.spi1_cs))
oled.rotate(1)
#oled = SSD1306_SPI(WIDTH, HEIGHT, spi, dc,rst, cs) use GPIO PIN NUMBERS
while True:
    try:
        for i in range(40):
            for j in range(56):
 
                oled.fill(0)
                oled.show()
                #sleep(1)
                oled.text("HELLO www.eetree.cn",i,j)
                oled.show()
                sleep_ms(50)
    except KeyboardInterrupt:
        break
