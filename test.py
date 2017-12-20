import keyboard
import time
c = 1;
while 1:
	if keyboard.is_pressed("a"):
		time.sleep(1)
		c+=1
	print c
