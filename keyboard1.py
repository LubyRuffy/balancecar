
'''
import sys

x = 0
while x != chr(27): # ESC
    x=sys.stdin.read(1)[0]
    if x == 'a':
		print x

import  os
import  sys
import  tty, termios
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
try :
    tty.setraw( fd )
    ch = sys.stdin.read( 1 )
finally :
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
'''

#!/usr/bin/env python
#coding: utf-8
from evdev import InputDevice
from select import select

def detectInputKey():
    dev = InputDevice('/dev/input/event4')
    while True:
        select([dev], [], [])
        for event in dev.read():
            print "code:%s value:%s" % (event.code, event.value)


if __name__ == '__main__':
    detectInputKey()
