### board.py --- eetree micropython training board configuration.
## author: picospuch

class game_kit:
    # joystick FJO8K-N VR1
    joy_x = 28
    joy_y = 29

    # buzzer Buzzer LS1
    buzzer = 23

    # accelerometer MMA7660FC U2
    accelerometer_scl = 11
    accelerometer_sda = 10
    accelerometer_int = 9
    accelerometer_i2c = 1

    # keys (SW3 SW4 SW5 SW6)
    key_b = 5
    key_a = 6
    key_start = 7
    key_select = 8

    # infra-red-rtx (IRM-H638T VSMB10940) U4
    ir_rx = 25
    ir_tx = 24

    # liquid-crystal-display ST7789_1.54_240x240 DS1
    lcd_sck = 2
    lcd_sda = 3
    lcd_rst = 0
    lcd_dc = 1

    # status-led STA D1
    led_sta = 4
    
class pin_cfg:
    yellow_led = 20
    blue_led = 21
    green_led = 22
    red_led = 26
    
    buzzer = 19
    mic = 27
    
    i2c0_scl = 17
    i2c0_sda = 16
    
    i2c1_scl = 15
    i2c1_sda = 14

    spi1_mosi = 11
    spi1_sck = 10
    spi1_dc = 9
    spi1_rstn = 8
    spi1_cs = 29

    adc0 = 26
    adc1 = 27

    k1 = 12
    k2 = 13

    pot = 28
