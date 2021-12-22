###############################################################
# WS2812 RGB LED Ring Light 
# Google Home and Amazon Alexa LED Emulator
# with the Raspberry Pi Pico Microcontroller
#
# by Joshua Hrisko, Maker Portal LLC (c) 2021
#
# Based on the Example neopixel_ring at:
# https://github.com/raspberrypi/pico-micropython-examples
###############################################################
#
import array, time, math
from machine import Pin
import rp2

#
############################################
# RP2040 PIO and Pin Configurations
############################################
#
# WS2812 LED Ring Configuration
led_count = 12 # number of LEDs in ring light
PIN_NUM = 18 # pin connected to ring light
brightness = 0.01 # 0.1 = darker, 1.0 = brightest

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT,
             autopull=True, pull_thresh=24) # PIO configuration

# define WS2812 parameters
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


# Create the StateMachine with the ws2812 program, outputting on pre-defined pin
# at the 8MHz frequency
state_mach = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))

# Activate the state machine
state_mach.active(1)

# Range of LEDs stored in an array
pixel_array = array.array("I", [0 for _ in range(led_count)])
#
############################################
# Functions for RGB Coloring
############################################
#
def update_pix(brightness_input=brightness): # dimming colors and updating state machine (state_mach)
    dimmer_array = array.array("I", [0 for _ in range(led_count)])
    for ii,cc in enumerate(pixel_array):
        r = int(((cc >> 8) & 0xFF) * brightness_input) # 8-bit red dimmed to brightness
        g = int(((cc >> 16) & 0xFF) * brightness_input) # 8-bit green dimmed to brightness
        b = int((cc & 0xFF) * brightness_input) # 8-bit blue dimmed to brightness
        dimmer_array[ii] = (g<<16) + (r<<8) + b # 24-bit color dimmed to brightness
    state_mach.put(dimmer_array, 8) # update the state machine with new colors
    time.sleep_ms(10)

def set_24bit(ii, color): # set colors to 24-bit format inside pixel_array
    color = hex_to_rgb(color)
    pixel_array[ii] = (color[1]<<16) + (color[0]<<8) + color[2] # set 24-bit color
    
def hex_to_rgb(hex_val):
    return tuple(int(hex_val.lstrip('#')[ii:ii+2],16) for ii in (0,2,4))
#
############################################
# Main Loops and Calls
############################################
#

def google_home():
    # Create Google Home four color rotation scheme
    google_colors = ['#4285f4','#ea4335','#fbbc05','#34a853'] # hex colors by Google
    cycles = 5 # number of times to cycle 360-degrees
    for jj in range(int(cycles*len(pixel_array))):
        for ii in range(len(pixel_array)):
            if ii%int(math.ceil(len(pixel_array)/4))==0: # 90-degree leds only
                set_24bit((ii+jj)%led_count,google_colors[int(ii/len(pixel_array)*4)])
            else:
                set_24bit((ii+jj)%led_count,'#000000') # other pixels blank
        update_pix() # update pixel colors
        time.sleep(0.05) # wait between changes

def amazon_alexa():
    # Create Amazon Alexa rotation wheel
    amazon_colors = ['#00dbdc','#0000d4'] # hex colors by Amazon
    light_width = 3 # width of rotating led array
    cycles = 3 # number of times width rotates 360-deg
    for jj in range(int(cycles*len(pixel_array))):
        for ii in range(len(pixel_array)):
            if ii<light_width: 
                set_24bit((ii+jj)%led_count,amazon_colors[0])
            else:
                set_24bit((ii+jj)%led_count,amazon_colors[1]) # other pixels blank
        update_pix() # update pixel colors
        time.sleep(0.03) # wait between changes
        time.sleep(0.5)

    # turn off LEDs using the Alexa zipper-type turnoff
    for ii in range(int(math.ceil(len(pixel_array)/2))):
        set_24bit(ii,'#000000') # turn off positive side
        set_24bit(int(len(pixel_array)-ii-1),'#000000') # turn off negative side 
        update_pix() # update
        time.sleep(0.02) # wait

while True:
    google_home()
