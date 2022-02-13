### ir-test-2.py --- test ir rx and tx with display update.
## author: picospuch
from machine import Pin, RTC
from time import sleep
import random
from button import button
from board import game_kit
from framebuf import FrameBuffer, RGB565
from breakout_colourlcd240x240 import BreakoutColourLCD240x240

width = BreakoutColourLCD240x240.WIDTH
height = BreakoutColourLCD240x240.HEIGHT

display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
display = BreakoutColourLCD240x240(display_buffer)
fbuf = FrameBuffer(display_buffer, 240, 240, RGB565)

display.set_backlight(1.0)

b = button(game_kit.ir_rx)
f_images = [open("/bingdwendwen.png.bin", 'rb'),
           open("/bingdwendwen-3.png.bin", 'rb'),
           open("/bingdwendwen-2.png.bin", 'rb'),
           open("/bingdwendwen-1.png.bin", 'rb')]
#f_image = open("/logo.bin", 'rb')

h = const(24)
@micropython.native
def draw_bg(f = 0):
    f = f_images[f]
    f.seek(0)
    for y in range(240 / h):
        buf = bytearray(f.read(480 * h))
        buf = FrameBuffer(buf, 240, h, RGB565)
        fbuf.blit(buf, 0, y * h)

rtc = RTC()

frame_flip = 0
toggle = True
while True:
    dts = rtc.datetime()
    
    draw_bg(frame_flip)

    if frame_flip > 0:
        frame_flip = frame_flip - 1

    if b.value():
        frame_flip = 3
        # toggle = not toggle
        # if toggle:
        #     display.set_pen(255, 0, 0)
        #     display.text("Hello EETree", width // 2 - 20, height // 2 - 20, 200, 4)
        
    display.set_pen(255, 0, 0)
    display.text("{0:02}:{1:02}:{2:02}".format(dts[4], dts[5], dts[6]), width // 2 + 10, 200, 200, 2)
    display.text("Hello EETree", width // 2 - 20 + random.randint(-3, 3), 220 + random.randint(-3, 3), 200, 2)
            
    display.update()
    sleep(0.02)
