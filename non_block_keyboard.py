import threading
import time
import sys, termios, tty, os


kbdInput = ''
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
    kbdInput = getch()
    finished = True

k=1
while True:
    if finished:
        finished = False
        listener = threading.Thread(target=kbdListener)
        listener.start()
    print kbdInput
    time.sleep(0.2)
