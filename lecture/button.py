### button.py --- button based on Pin and IRQ, with debounce.
## author: picospuch

import time
from machine import Pin

class button:
    def __init__(self, pin, callback=None, trigger=Pin.IRQ_RISING, min_ago=200):
        #print("button init")
        self.callback = callback
            
        self.min_ago = min_ago
        self._next_call = time.ticks_add(time.ticks_ms(), self.min_ago)

        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)

        self.pin.irq(trigger=trigger, handler=self.debounce_handler)

        self._is_pressed = False

    def call_callback(self, pin):
        #print("call_callback")
        self._is_pressed = True
        if self.callback is not None:
            self.callback(pin)

    def debounce_handler(self, pin):
        #print("debounce")
        if time.ticks_diff(time.ticks_ms(), self._next_call) > 0:
            self._next_call = time.ticks_add(time.ticks_ms(), self.min_ago)
            self.call_callback(pin)

    def value(self):
        p = self._is_pressed
        self._is_pressed = False
        return p
