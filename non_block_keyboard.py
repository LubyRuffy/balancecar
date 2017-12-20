import threading
import time
import sys, termios, tty, os


if 1:

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

    while 1:
        if finished:
            finished = False
            listener = threading.Thread(target=kbdListener)
            listener.start()
        time.sleep(0.2)
        print kbdInput      
