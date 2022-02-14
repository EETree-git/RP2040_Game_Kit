### rp2040-ani.py --- play rp2040 chip tear-down animation.
## author: picospuch
## resource-from: https://twitter.com/johndmcmaster

### 转换图片的方法
## tjpgd只支持baseline编码的jpeg标准, 所以需要对资源进行转换.
## 通用步骤如下:
## 1. 下载imagemagick并安装
## 2. 打开命令提示符
## 3. 运行`convert rp2040.mp4 -type TrueColor -resize 240x240 rp2040.jpg`
## 4. 把转换后的jpg文件上传pico
## 一些gif每一帧只保存差异信息, 所以需要额外处理, 转换成coalesced gif:
## `convert rp2040.gif -coalesce -set dispose previous rp2040-coalesced.gif`
##

import gc
from machine import Pin, SPI
import st7789c
from board import game_kit
from time import sleep

gc.enable()
gc.collect()

def main():
    spi = SPI(0, baudrate=31250000, polarity=1, phase=1,
                  sck=Pin(game_kit.lcd_sck, Pin.OUT),
                  mosi=Pin(game_kit.lcd_sda, Pin.OUT))
    tft = st7789c.ST7789(
            spi,
            240,
            240,
            reset=Pin(game_kit.lcd_rst, Pin.OUT),
            dc=Pin(game_kit.lcd_dc, Pin.OUT),
            #xstart=0,
            #ystart=0,
            rotation=0)
    
    # enable display and clear screen
    tft.init()

    i = 0
    while True:
        # display jpg
        if i == 0: sleep(2)
        tft.jpg("rp2040-" + str(i) + ".jpg", 0, 52, st7789c.FAST)
        if i == 0: sleep(2)
        i = (i + 1) % 12
        sleep(0.02)

main()
