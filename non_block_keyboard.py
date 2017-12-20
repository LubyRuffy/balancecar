import threading
import time
import sys, termios, tty, os


kbdInput = ''
playingID = ''
finished = True

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def kbdListener():
    global kbdInput, finished
    kbdInput = getch()
    finished = True


while True:
    if playingID != kbdInput:
        playingID = kbdInput
    if kbdInput == 's':
        print "s\n"
    if finished:
        finished = False
        listener = threading.Thread(target=kbdListener)
        listener.start()
    time.sleep(0.2)
