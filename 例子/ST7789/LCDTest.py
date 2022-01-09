import uos
import machine
import st7789 as st7789
from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2
import random
import framebuf

image_file0 = "/lib/logo.bin" #图片文件地址

st7789_res = 0
st7789_dc  = 1
disp_width = 240
disp_height = 240
CENTER_Y = int(disp_width/2)
CENTER_X = int(disp_height/2)
print(uos.uname())
spi_sck=machine.Pin(2)
spi_tx=machine.Pin(3)
spi0=machine.SPI(0,baudrate=4000000, phase=1, polarity=1, sck=spi_sck, mosi=spi_tx)
#
print(spi0)
display = st7789.ST7789(spi0, disp_width, disp_width,
                          reset=machine.Pin(st7789_res, machine.Pin.OUT),
                          dc=machine.Pin(st7789_dc, machine.Pin.OUT),
                          xstart=0, ystart=0, rotation=0)
display.fill(st7789.BLACK)
display.text(font2, "Hello!", 10, 10)
display.text(font2, "RPi Pico", 10, 40)
display.text(font2, "MicroPython", 35, 100)
display.text(font2, "EETREE", 35, 150)
display.text(font2, "www.eetree.cn", 30, 200)
f_image = open(image_file0, 'rb')


for i in range(5000):
    display.pixel(random.randint(0, disp_width),
          random.randint(0, disp_height),
          st7789.color565(random.getrandbits(8),random.getrandbits(8),random.getrandbits(8)))
    
for column in range(1,240):
                buf=f_image.read(480)
                display.blit_buffer(buf, 1, column, 240, 1)
        
