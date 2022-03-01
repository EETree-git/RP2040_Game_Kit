from machine import Timer, ADC, Pin
import _thread

# from buzzer_music import music
# from time import sleep
# 
# song="0 E5 1 0;1 E5 1 0;3 E5 1 0;5 C5 1 0;6 E5 1 0;8 G5 1 0;12 G4 1 0;19 G4 1 0;25 A4 1 0;27 B4 1 0;29 A#4 1 0;30 A4 1 0;22 E4 1 0;16 C5 1 0;32 C5 1 0;33 E5 1 0;35 G5 1 0;36 A5 1 0;38 F5 1 0;39 G5 1 0;41 E5 1 0;43 C5 1 0;44 D5 1 0;45 B4 1 0;51 G4 1 0;57 A4 1 0;59 B4 1 0;61 A#4 1 0;62 A4 1 0;54 E4 1 0;48 C5 1 0;64 C5 1 0;65 E5 1 0;67 G5 1 0;68 A5 1 0;70 F5 1 0;71 G5 1 0;73 E5 1 0;75 C5 1 0;76 D5 1 0;77 B4 1 0;80 G5 1 0;81 F#5 1 0;82 F5 1 0;83 D#5 1 0;85 E5 1 0;87 G#4 1 0;88 A4 1 0;89 C5 1 0;91 A4 1 0;93 D5 1 0;96 G5 1 0;97 F#5 1 0;98 F5 1 0;103 C6 1 0;99 D#5 1 0;105 C6 1 0;101 E5 1 0;92 C5 1 0;106 C6 1 0;111 G5 1 0;112 F#5 1 0;113 F5 1 0;114 D#5 1 0;116 E5 1 0;118 G#4 1 0;119 A4 1 0;120 C5 1 0;122 A4 1 0;124 D5 1 0;123 C5 1 0;127 D#5 1 0;130 D5 1 0;133 C5 1 0;139 C5 1 0;140 C5 1 0;142 C5 1 0;144 C5 1 0;145 D5 1 0;147 E5 1 0;148 C5 1 0;150 A4 1 0;151 G4 1 0;154 C5 1 0;155 C5 1 0;157 C5 1 0;159 C5 1 0;160 D5 1 0;162 E5 1 0;167 C5 1 0;168 C5 1 0;170 C5 1 0;172 C5 1 0;173 D5 1 0;175 E5 1 0;176 C5 1 0;178 A4 1 0;179 G4 1 0;183 E5 1 0;184 E5 1 0;186 E5 1 0;188 C5 1 0;189 E5 1 0;191 G5 1 0;195 G4 1 0;198 B6 1 0;199 E7 1 0;201 B6 1 0;202 E7 1 0;204 B6 1 0;205 E7 1 0;207 B6 1 0;208 E7 1 0;210 B6 1 0;211 E7 1 0;213 E6 1 0;214 G6 1 0;215 E7 1 0;216 C7 1 0;217 D7 1 0;218 G7 1 0"
# mymusic = music(song)
# 
# while True:
#     mymusic.tick()
#     sleep(0.02)

import infones
from board import game_kit

machine.freq(250_000_000) # basically no any effect at shallow sight.

xAxis = ADC(Pin(game_kit.joy_x))
yAxis = ADC(Pin(game_kit.joy_y))

tim = Timer()

a = Pin(game_kit.key_a, Pin.IN, Pin.PULL_UP);
b = Pin(game_kit.key_b, Pin.IN, Pin.PULL_UP);
select = Pin(game_kit.key_select, Pin.IN, Pin.PULL_UP);

def dir():
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    director = 0
        
    if xValue <1000:
        director = 64
    elif xValue >40000:
        director = 128
            
    if yValue <1000:
        director = 16
    elif yValue >40000:
        director = 32
    return director

def poll_events(t):
    dwPad = 0
    if a.value() == 0:
        dwPad |= 1
    if b.value() == 0:
        dwPad |= 8
    if select.value() == 0:
        dwPad |= 2
    dwPad |= dir()
    #if dwPad != 0: 
    infones.input(dwPad)
    print(dwPad);
    #mymusic.tick()

# 125hz
tim.init(period=8, mode=Timer.PERIODIC, callback=poll_events)

_thread.start_new_thread(infones.render, ())
infones.load()
