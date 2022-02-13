### ir-test.py --- test ir rx and tx.
## author: picospuch

from machine import Pin
from time import sleep
from button import button
from board import game_kit
b = button(game_kit.ir_rx)

while True:
    print(b.value())
    sleep(0.02)
