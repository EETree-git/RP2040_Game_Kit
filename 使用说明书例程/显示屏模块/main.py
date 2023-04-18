#导入所需类
from machine import Pin, SPI

#导入驱动及字库文件
import st7789 as st7789
from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2

#定义SPI引脚及配置SPI
spi_sck=Pin(2)
spi_tx=Pin(3)
spi0=SPI(0,baudrate=4000000, phase=1, polarity=1, sck=spi_sck, mosi=spi_tx)

#配置st7789驱动
st7789_res = 0
st7789_dc  = 1
disp_width = 240
disp_height = 240
display = st7789.ST7789(spi0, disp_width, disp_height,
                          reset=machine.Pin(st7789_res, machine.Pin.OUT),
                          dc=machine.Pin(st7789_dc, machine.Pin.OUT),
                          xstart=0, ystart=0, rotation=0)

#屏幕显示字体
display.fill(st7789.BLACK)
display.text(font2, "Hello!", 10, 10)
display.text(font2, "RPi Pico", 10, 40)
display.text(font2, "MicroPython", 35, 100)
display.text(font2, "EETREE", 35, 150)
display.text(font2, "www.eetree.cn", 30, 200)

#屏幕显示图片
image_file0 = "/logo.bin"
f_image = open(image_file0, 'rb')
for column in range(1,240):
                buf=f_image.read(480)
                display.blit_buffer(buf, 1, column, 240, 1)