### yasnake --- yet another snake game.
## copyright: 2021,2022 picospuch
## license: GPLv3
## board: eetree-game-kit

import random
import time
import uasyncio as asyncio
from machine import Pin, SPI

import st7789c
import vga2_8x8 as font

from button import button
from buzzer_music import music

from board import game_kit

class color_cfg:
    black = st7789c.BLACK
    magenta = st7789c.MAGENTA
    blue = st7789c.BLUE
    snake = st7789c.MAGENTA
    food = st7789c.RED
    background = st7789c.color565(0, 255, 120)

class tile_cfg:
    block0 = b"\xfe" # ■
    block1 = b"\xb2" # ▓
    block = b"\xfe"

tile_cfg.block = tile_cfg.block1

class board_cfg:
    width = 30
    height = 29
    dashboard_x = 0
    dashboard_y = 29
    dashboard_width = 30
    dashboard_height = 1

class rotary_encoder:
    def __init__(self, pin_a, pin_b, callback):
        print(" init")
        self.callback = callback

        self.min_ago = 500
        self._next_call = time.ticks_ms() + self.min_ago

        self.pin_a = Pin(pin_a, Pin.IN)
        self.pin_b = Pin(pin_b, Pin.IN)

        self.pin_a.irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING, handler=self.debounce_handler)

    def call_callback(self, pin):
        if self.pin_b.value() != self.pin_a.value():
            self.callback("cw")
        else:
            self.callback("ccw")

    def debounce_handler(self, pin):
        #print("debounce")
        if time.ticks_ms() > self._next_call:
            self._next_call = time.ticks_ms() + self.min_ago
            self.call_callback(pin)

class hardware():
    def init():
        # screen
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

        tft.offset(0, 0)
        tft.init()
        tft.fill(color_cfg.background)
        tft.fill_rect(0, 232, 240, 8, color_cfg.blue)

        hardware.tft = tft

pen_color = color_cfg.background

def outtextxy(x, y, c):
    global pen_color
    hardware.tft.text(font, c, x*8, y*8, pen_color, color_cfg.background)

def setcolor(c):
    global pen_color
    pen_color = c

class location ():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class snake():
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    PAUSE = 1
    RUNNING = 2
    STOP = 3

    n = 6 # 6 body nodes + 1 head + 1 tail(invisible) = 8 nodes, at very first
    
    def __init__(self):
        # bgm
        self.bgm = p_music(p_music.song0, tempo=1, duty=500, pins=[
            Pin(game_kit.buzzer, Pin.OUT)])
        # controller
        #self.re = rotary_encoder(game_kit.rotary_encoder_a, game_kit.rotary_encoder_b, self.direction_callback)
        self.k1 = button(game_kit.key_a, self.k1_callback)

        self.haskey = False
        self.k = "cw"
        self.last_k = self.k

        # iot
        self.led = Pin(game_kit.led_sta, Pin.OUT)

        # interest
        self.score = 0
        self.n = snake.n
        self.state = self.RUNNING

    def direction_callback(self, d):
        print(d + "\n")
        self.haskey = True
        self.last_k = self.k
        self.k = d

    def k1_callback(self, p):
        print("k1 pressed")
        self.bgm.toggle_pause()

    async def opening(self):
        setcolor(color_cfg.snake)
        for j in range(board_cfg.height):
            for i in range(board_cfg.width):
                if j % 2 == 1:
                    x = 29 - i
                else:
                    x = i
                await asyncio.sleep_ms(5)
                outtextxy(x, j, tile_cfg.block)
        setcolor(color_cfg.background)
        for j in range(board_cfg.height):
            for i in range(board_cfg.width):
                if j % 2 == 1:
                    x = 29 - i
                else:
                    x = i
                await asyncio.sleep_ms(5)
                outtextxy(x, j, tile_cfg.block)

    def closing(self):
        self.state = snake.STOP
        setcolor(color_cfg.magenta)
        outtextxy(0, 29, "GAME OVER")
    
    async def blink(self):
        self.led.value(1)
        await asyncio.sleep_ms(50)
        self.led.value(0)
        await asyncio.sleep_ms(50)
        
    async def process(self):
        bgm = asyncio.create_task(self.bgm_process())

        await self.opening()

        self.init_run()
        
        # main loop
        while True:
            self.dir_select()
            self.run()
            self.draw()
            self.judge()
            await self.blink()

    def dir_select(self):
        key = self.getch()
        
        if key == "cw":
            if self.d == snake.RIGHT:
                self.d = snake.DOWN
            elif self.d == snake.DOWN:
                self.d = snake.LEFT
            elif self.d == snake.LEFT:
                self.d = snake.UP
            elif self.d == snake.UP:
                self.d = snake.RIGHT
        if key == "ccw":
            if self.d == snake.RIGHT:
                self.d = snake.UP
            elif self.d == snake.UP:
                self.d = snake.LEFT
            elif self.d == snake.LEFT:
                self.d = snake.DOWN
            elif self.d == snake.DOWN:
                self.d = snake.RIGHT

    def init_run(self):
        self.body = []

        for i in range(self.n):
            self.body.append(location((self.n - 1 - i), 0))

        self.head = location(self.n, 0)
        self.tail = location(-1, 0)

        self.food = location(-1, -1)

        setcolor(color_cfg.snake)
        outtextxy(0, 0, (self.n + 1) * tile_cfg.block)

        self.d = self.RIGHT

        self.fod()
        
    def run(self):
        if self.state != snake.RUNNING:
            return
        
        self.tail.x = self.body[self.n - 1].x
        self.tail.y = self.body[self.n - 1].y

        for i in range(self.n - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x = self.head.x
        self.body[0].y = self.head.y

        if self.d == snake.UP:
            self.head.y -= 1
        elif self.d == snake.DOWN:
            self.head.y += 1
        elif self.d == snake.LEFT:
            self.head.x -= 1
        elif self.d == snake.RIGHT:
            self.head.x += 1

        if self.head.x == -1:
            self.head.x = board_cfg.width - 1
        elif self.head.x == board_cfg.width:
            self.head.x = 0
            
        if self.head.y == -1:
            self.head.y = board_cfg.height - 1
        elif self.head.y == board_cfg.height:
            self.head.y = 0    
            
    def draw(self):
        setcolor(color_cfg.background)
        outtextxy(self.tail.x, self.tail.y, tile_cfg.block)
        setcolor(color_cfg.snake)
        outtextxy(self.head.x, self.head.y, tile_cfg.block)
        
    def judge(self):
        if self.head.x == self.food.x and self.head.y == self.food.y:
            self.body.append(location(-1, -1))
            self.n += 1
            self.fod()
            # add score
            self.score += 100
            setcolor(color_cfg.food)
            outtextxy(board_cfg.dashboard_x + 20, board_cfg.dashboard_y, "SCORE: " + str(self.score))

        for i in range(self.n):
            if self.head.x == self.body[i].x and self.head.y == self.body[i].y:
                self.closing()
        
    def fod(self):
        self.food.x = random.randrange(0, board_cfg.width)
        self.food.y = random.randrange(0, board_cfg.height)
        setcolor(color_cfg.food)
        outtextxy(self.food.x, self.food.y, tile_cfg.block)

    def getch(self):
        if self.haskey:
            self.haskey = False
            return self.k
        else:
            return None

    async def bgm_process(self):
        while True:
            await asyncio.sleep_ms(100)
            self.bgm.tick()

class p_music(music):
    song1 = '0 A5 2 26 0.6299212574958801;2 B5 2 26 0.6299212574958801;4 C6 6 26 0.6299212574958801;10 B5 2 26 0.6299212574958801;12 C6 4 26 0.6299212574958801;16 E6 4 26 0.6299212574958801;20 B5 8 26 0.6299212574958801;32 E5 4 26 0.6299212574958801;36 A5 6 26 0.6299212574958801;42 G5 2 26 0.6299212574958801;44 A5 4 26 0.6299212574958801;48 C6 4 26 0.6299212574958801;52 G5 8 26 0.6299212574958801;64 F5 2 26 0.6299212574958801;66 E5 2 26 0.6299212574958801;68 F5 6 26 0.6299212574958801;74 E5 2 26 0.6299212574958801;76 F5 4 26 0.6299212574958801;80 C6 4 26 0.6299212574958801;84 E5 8 26 0.6299212574958801;94 C6 2 26 0.6299212574958801;96 C6 2 26 0.6299212574958801;98 C6 2 26 0.6299212574958801;100 B5 6 26 0.6299212574958801;106 F#5 2 26 0.6299212574958801;108 F#5 4 26 0.6299212574958801;112 B5 4 26 0.6299212574958801;116 B5 8 26 0.6299212574958801;128 A5 2 26 0.6299212574958801;130 B5 2 26 0.6299212574958801;132 C6 6 26 0.6299212574958801;138 B5 2 26 0.6299212574958801;140 C6 4 26 0.6299212574958801;144 E6 4 26 0.6299212574958801;148 B5 8 26 0.6299212574958801;160 E5 2 26 0.6299212574958801;162 E5 2 26 0.6299212574958801;164 A5 6 26 0.6299212574958801;170 G5 2 26 0.6299212574958801;172 A5 4 26 0.6299212574958801;176 C6 4 26 0.6299212574958801;180 G5 8 26 0.6299212574958801;192 E5 4 26 0.6299212574958801;196 F5 4 26 0.6299212574958801;200 C6 2 26 0.6299212574958801;202 B5 2 26 0.6299212574958801;204 B5 4 26 0.6299212574958801;208 C6 4 26 0.6299212574958801;212 D6 4 26 0.6299212574958801;216 E6 2 26 0.6299212574958801;218 C6 2 26 0.6299212574958801;220 C6 8 26 0.6299212574958801;228 C6 2 26 0.6299212574958801;230 B5 2 26 0.6299212574958801;232 A5 4 26 0.6299212574958801;236 B5 4 26 0.6299212574958801;240 G#5 4 26 0.6299212574958801;244 A5 11 26 0.6299212574958801;256 C6 2 26 0.6299212574958801;258 D6 2 26 0.6299212574958801;260 E6 6 26 0.6299212574958801;266 D6 2 26 0.6299212574958801;268 E6 4 26 0.6299212574958801;272 G6 4 26 0.6299212574958801;276 D6 8 26 0.6299212574958801;288 G5 2 26 0.6299212574958801;290 G5 2 26 0.6299212574958801;292 C6 6 26 0.6299212574958801;298 B5 2 26 0.6299212574958801;300 C6 4 26 0.6299212574958801;304 E6 4 26 0.6299212574958801;308 E6 11 26 0.6299212574958801;324 A5 2 26 0.6299212574958801;326 B5 2 26 0.6299212574958801;328 C6 4 26 0.6299212574958801;332 B5 2 26 0.6299212574958801;334 C6 2 26 0.6299212574958801;336 D6 4 26 0.6299212574958801;340 C6 6 26 0.6299212574958801;346 G5 2 26 0.6299212574958801;348 G5 8 26 0.6299212574958801;356 F6 4 26 0.6299212574958801;360 E6 4 26 0.6299212574958801;364 D6 4 26 0.6299212574958801;368 C6 4 26 0.6299212574958801;372 E6 15 26 0.6299212574958801;388 E6 11 26 0.6299212574958801;400 E6 4 26 0.6299212574958801;404 A6 8 26 0.6299212574958801;412 G6 8 26 0.6299212574958801;420 E6 4 26 0.6299212574958801;424 D6 2 26 0.6299212574958801;426 C6 2 26 0.6299212574958801;428 C6 8 26 0.6299212574958801;436 D6 4 26 0.6299212574958801;440 C6 2 26 0.6299212574958801;442 D6 2 26 0.6299212574958801;444 D6 4 26 0.6299212574958801;448 G6 4 26 0.6299212574958801;452 E6 11 26 0.6299212574958801;464 E6 4 26 0.6299212574958801;468 A6 8 26 0.6299212574958801;476 G6 8 26 0.6299212574958801;484 E6 4 26 0.6299212574958801;488 D6 2 26 0.6299212574958801;490 C6 2 26 0.6299212574958801;492 C6 8 26 0.6299212574958801;500 D6 4 26 0.6299212574958801;504 C6 2 26 0.6299212574958801;506 D6 2 26 0.6299212574958801;508 D6 4 26 0.6299212574958801;512 B5 4 26 0.6299212574958801;516 A5 11 26 0.6299212574958801;528 A5 2 26 0.6299212574958801;530 B5 2 26 0.6299212574958801;532 C6 6 26 0.6299212574958801;538 B5 2 26 0.6299212574958801;540 C6 4 26 0.6299212574958801;544 E6 4 26 0.6299212574958801;548 B5 8 26 0.6299212574958801;560 E5 4 26 0.6299212574958801;564 A5 6 26 0.6299212574958801;570 G5 2 26 0.6299212574958801;572 A5 4 26 0.6299212574958801;576 C6 4 26 0.6299212574958801;580 G5 8 26 0.6299212574958801;592 F5 2 26 0.6299212574958801;594 E5 2 26 0.6299212574958801;596 F5 6 26 0.6299212574958801;602 E5 2 26 0.6299212574958801;604 F5 4 26 0.6299212574958801;608 C6 4 26 0.6299212574958801;612 E5 8 26 0.6299212574958801;622 C6 2 26 0.6299212574958801;624 C6 2 26 0.6299212574958801;626 C6 2 26 0.6299212574958801;628 B5 6 26 0.6299212574958801;634 F#5 2 26 0.6299212574958801;636 F#5 4 26 0.6299212574958801;640 B5 4 26 0.6299212574958801;644 B5 8 26 0.6299212574958801;656 A5 2 26 0.6299212574958801;658 B5 2 26 0.6299212574958801;660 C6 6 26 0.6299212574958801;666 B5 2 26 0.6299212574958801;668 C6 4 26 0.6299212574958801;672 E6 4 26 0.6299212574958801;676 B5 8 26 0.6299212574958801;688 E5 2 26 0.6299212574958801;690 E5 2 26 0.6299212574958801;692 A5 6 26 0.6299212574958801;698 G5 2 26 0.6299212574958801;700 A5 4 26 0.6299212574958801;704 C6 4 26 0.6299212574958801;708 G5 8 26 0.6299212574958801;720 E5 4 26 0.6299212574958801;724 F5 4 26 0.6299212574958801;728 C6 2 26 0.6299212574958801;730 B5 2 26 0.6299212574958801;732 B5 4 26 0.6299212574958801;736 C6 4 26 0.6299212574958801;740 D6 4 26 0.6299212574958801;744 E6 2 26 0.6299212574958801;746 C6 2 26 0.6299212574958801;748 C6 8 26 0.6299212574958801;756 C6 2 26 0.6299212574958801;758 B5 2 26 0.6299212574958801;760 A5 4 26 0.6299212574958801;764 B5 4 26 0.6299212574958801;768 G#5 4 26 0.6299212574958801;772 A5 11 26 0.6299212574958801'
    song0 = '0 E5 2 14;4 B4 2 14;6 C5 2 14;8 D5 2 14;10 E5 1 14;11 D5 1 14;12 C5 2 14;14 B4 2 14;16 A4 2 14;20 A4 2 14;22 C5 2 14;24 E5 2 14;28 D5 2 14;30 C5 2 14;32 B4 2 14;38 C5 2 14;40 D5 2 14;44 E5 2 14;48 C5 2 14;52 A4 2 14;56 A4 2 14;64 D5 2 14;68 F5 2 14;70 A5 2 14;74 G5 2 14;76 F5 2 14;78 E5 2 14;84 C5 2 14;86 E5 2 14;90 D5 2 14;92 C5 2 14;94 B4 2 14;98 B4 2 14;100 C5 2 14;102 D5 2 14;106 E5 2 14;110 C5 2 14;114 A4 2 14;118 A4 2 14;248 E5 8 14;256 C5 8 14;264 D5 8 14;272 B4 8 14;280 C5 8 14;288 A4 8 14;296 G#4 8 14;304 B4 8 14;313 E5 8 14;321 C5 8 14;329 D5 8 14;337 B4 4 14;341 B4 4 14;345 C5 4 14;349 E5 4 14;353 A5 8 14;361 G#5 8 14;248 C5 8 14;256 A4 8 14;264 B4 8 14;272 G#4 8 14;280 A4 8 14;288 E4 8 14;0 B4 2 14;4 G#4 2 14;6 A4 2 14;8 B4 2 14;12 A4 2 14;14 G#4 2 14;28 B4 2 14;30 A4 2 14;32 G#4 4 14;40 B4 2 14;38 A4 2 14;44 C5 2 14;52 E4 2 14;64 F4 2 14;94 G#4 2 14;100 A4 2 14;102 B4 2 14;106 C5 2 14;110 A4 2 14;114 E4 2 14;114 E4 2 14;118 E4 2 14;98 G#4 2 14;296 E4 8 14;304 G#4 8 14;313 C5 8 14;321 A4 8 14;329 B4 8 14;337 G#4 4 14;341 G#4 4 14;345 A4 4 14;349 C5 4 14;353 E5 8 14;353 E5 8 14;361 E5 8 14;48 A4 2 14;56 E4 2 14;68 D5 2 14;70 F5 2 14;74 E5 2 14;76 D5 2 14;80 E5 2 14;78 C5 2 14;80 C5 2 14;22 A4 2 14;24 C5 2 14;84 A4 2 14;86 C5 2 14;92 A4 2 14;90 B4 2 14;0 E5 2 14;4 B4 2 14;6 C5 2 14;8 D5 2 14;10 E5 1 14;11 D5 1 14;12 C5 2 14;14 B4 2 14;16 A4 2 14;20 A4 2 14;22 C5 2 14;24 E5 2 14;28 D5 2 14;30 C5 2 14;32 B4 2 14;38 C5 2 14;40 D5 2 14;44 E5 2 14;48 C5 2 14;52 A4 2 14;56 A4 2 14;64 D5 2 14;68 F5 2 14;70 A5 2 14;74 G5 2 14;76 F5 2 14;78 E5 2 14;84 C5 2 14;86 E5 2 14;90 D5 2 14;92 C5 2 14;94 B4 2 14;98 B4 2 14;100 C5 2 14;102 D5 2 14;106 E5 2 14;110 C5 2 14;114 A4 2 14;118 A4 2 14;0 B4 2 14;4 G#4 2 14;6 A4 2 14;8 B4 2 14;12 A4 2 14;14 G#4 2 14;28 B4 2 14;30 A4 2 14;32 G#4 4 14;40 B4 2 14;38 A4 2 14;44 C5 2 14;52 E4 2 14;64 F4 2 14;94 G#4 2 14;100 A4 2 14;102 B4 2 14;106 C5 2 14;110 A4 2 14;114 E4 2 14;114 E4 2 14;118 E4 2 14;98 G#4 2 14;48 A4 2 14;56 E4 2 14;68 D5 2 14;70 F5 2 14;74 E5 2 14;76 D5 2 14;80 E5 2 14;78 C5 2 14;80 C5 2 14;22 A4 2 14;24 C5 2 14;84 A4 2 14;86 C5 2 14;92 A4 2 14;90 B4 2 14;124 E5 2 14;128 B4 2 14;130 C5 2 14;132 D5 2 14;134 E5 1 14;135 D5 1 14;136 C5 2 14;138 B4 2 14;140 A4 2 14;144 A4 2 14;146 C5 2 14;148 E5 2 14;152 D5 2 14;154 C5 2 14;156 B4 2 14;162 C5 2 14;164 D5 2 14;168 E5 2 14;172 C5 2 14;176 A4 2 14;180 A4 2 14;188 D5 2 14;192 F5 2 14;194 A5 2 14;198 G5 2 14;200 F5 2 14;202 E5 2 14;208 C5 2 14;210 E5 2 14;214 D5 2 14;216 C5 2 14;218 B4 2 14;222 B4 2 14;224 C5 2 14;226 D5 2 14;230 E5 2 14;234 C5 2 14;238 A4 2 14;242 A4 2 14;124 B4 2 14;128 G#4 2 14;130 A4 2 14;132 B4 2 14;136 A4 2 14;138 G#4 2 14;152 B4 2 14;154 A4 2 14;156 G#4 4 14;164 B4 2 14;162 A4 2 14;168 C5 2 14;176 E4 2 14;188 F4 2 14;218 G#4 2 14;224 A4 2 14;226 B4 2 14;230 C5 2 14;234 A4 2 14;238 E4 2 14;238 E4 2 14;242 E4 2 14;222 G#4 2 14;172 A4 2 14;180 E4 2 14;192 D5 2 14;194 F5 2 14;198 E5 2 14;200 D5 2 14;204 E5 2 14;202 C5 2 14;204 C5 2 14;146 A4 2 14;148 C5 2 14;208 A4 2 14;210 C5 2 14;216 A4 2 14;214 B4 2 14;124 E5 2 14;128 B4 2 14;130 C5 2 14;132 D5 2 14;134 E5 1 14;135 D5 1 14;136 C5 2 14;138 B4 2 14;140 A4 2 14;144 A4 2 14;146 C5 2 14;148 E5 2 14;152 D5 2 14;154 C5 2 14;156 B4 2 14;162 C5 2 14;164 D5 2 14;168 E5 2 14;172 C5 2 14;176 A4 2 14;180 A4 2 14;188 D5 2 14;192 F5 2 14;194 A5 2 14;198 G5 2 14;200 F5 2 14;202 E5 2 14;208 C5 2 14;210 E5 2 14;214 D5 2 14;216 C5 2 14;218 B4 2 14;222 B4 2 14;224 C5 2 14;226 D5 2 14;230 E5 2 14;234 C5 2 14;238 A4 2 14;242 A4 2 14;124 B4 2 14;128 G#4 2 14;130 A4 2 14;132 B4 2 14;136 A4 2 14;138 G#4 2 14;152 B4 2 14;154 A4 2 14;156 G#4 4 14;164 B4 2 14;162 A4 2 14;168 C5 2 14;176 E4 2 14;188 F4 2 14;218 G#4 2 14;224 A4 2 14;226 B4 2 14;230 C5 2 14;234 A4 2 14;238 E4 2 14;238 E4 2 14;242 E4 2 14;222 G#4 2 14;172 A4 2 14;180 E4 2 14;192 D5 2 14;194 F5 2 14;198 E5 2 14;200 D5 2 14;204 E5 2 14;202 C5 2 14;204 C5 2 14;146 A4 2 14;148 C5 2 14;208 A4 2 14;210 C5 2 14;216 A4 2 14;214 B4 2 14;248 C5 2 13;252 C5 2 13;254 E5 2 13;250 E5 2 13;256 C5 2 13;260 C5 2 13;258 A4 2 13;262 A4 2 13;264 D5 2 13;268 D5 2 13;266 B4 2 13;270 B4 2 13;272 G#4 2 13;276 G#4 2 13;274 B4 2 13;278 B4 2 13;280 A4 2 13;284 A4 2 13;282 C5 2 13;286 C5 2 13;347 C5 2 13;351 C5 2 13;313 C5 2 13;317 C5 2 13;319 E5 2 13;315 E5 2 13;321 C5 2 13;325 C5 2 13;323 A4 2 13;327 A4 2 13;329 D5 2 13;333 D5 2 13;331 B4 2 13;335 B4 2 13;337 G#4 2 13;341 G#4 2 13;339 B4 2 13;343 B4 2 13;345 A4 2 13;349 A4 2 13;349 E5 2 13;353 E5 2 13;355 A5 2 13;359 A5 2 13;357 E5 2 13;361 E5 2 13;363 G#5 2 13;367 G#5 2 13;365 E5 2 14;292 A4 2 13;288 A4 2 13;294 E4 2 13;290 E4 2 13;300 G#4 2 13;296 G#4 2 13;302 E4 2 13;298 E4 2 13;308 G#4 2 13;304 G#4 2 13;310 B4 2 13;306 B4 2 13'
    def __init__(self, songString='0 D4 8 0', looping=True, tempo=3, duty=2512, pin=None, pins=[Pin(0)]):
        super().__init__(songString, looping, tempo, duty, pin, pins)
        self.pause = True

    def toggle_pause(self):
        self.pause = not self.pause
        if self.pause:
            print("mute\n")
            self.mute()
        else:
            print("unmute\n")
            self.unmute()
    
    def mute(self):
        for pwm in self.pwms:
            pwm.duty_u16(0)
    def unmute(self):
        for pwm in self.pwms:
            pwm.duty_u16(self.duty)

    def tick(self):
        if self.pause:
            pass
        else:
            super().tick()

def main():
    hardware.init()
    s = snake()
    asyncio.run(s.process())

main()
