from mpu6050 import mpu6050
from time import sleep
import math
import sys
import  RPi.GPIO as GPIO
import time
from PID import PID
from pidcontroller import PIDController
from init import *
#from keyboard_control import *
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
        global kbdInput, finished
        kbdInput = getch()
        finished = True


def forward(velocity):
	GPIO.output(motora_in1, GPIO.HIGH)
	GPIO.output(motora_in2, GPIO.LOW)
	pwm_a.ChangeDutyCycle(velocity)
	
	GPIO.output(motorb_in1, GPIO.HIGH)
	GPIO.output(motorb_in2, GPIO.LOW)
	pwm_b.ChangeDutyCycle(velocity)
	
def backward(velocity):
	GPIO.output(motora_in1, GPIO.LOW)
	GPIO.output(motora_in2, GPIO.HIGH)
	pwm_a.ChangeDutyCycle(velocity)
	
	GPIO.output(motorb_in1, GPIO.LOW)
	GPIO.output(motorb_in2, GPIO.HIGH)
	pwm_b.ChangeDutyCycle(velocity)

def stand_still():
	GPIO.output(motora_in1, GPIO.LOW)
	GPIO.output(motora_in2, GPIO.LOW)
	GPIO.output(motorb_in1, GPIO.LOW)
	GPIO.output(motorb_in2, GPIO.LOW)


def distance(a,b):
	return math.sqrt((a*a)+(b*b))
def y_rotation(x,y,z):
	radians = math.atan2(x, distance(y, z))
	return -math.degrees(radians)
def x_rotation(x,y,z):
	radians = math.atan2(y, distance(x, z))
	return math.degrees(radians)


sensor = mpu6050(0x68)
accel_data = sensor.get_accel_data()
gyro_data = sensor.get_gyro_data()
aTempX = accel_data['x']
aTempY = accel_data['y']
aTempZ = accel_data['z']

gTempX = gyro_data['x']
gTempY = gyro_data['y']
gTempZ = gyro_data['z']
last_x = x_rotation(aTempX, aTempY, aTempZ)
last_y = y_rotation(aTempX, aTempY, aTempZ)
gyro_offset_x = gTempX
gyro_offset_y = gTempY
gx_total = (last_x) - gyro_offset_x
gy_total = (last_y) - gyro_offset_y


time_diff = 0.035
K = 0.98

#PID1 = PIDController(P=-40, I=-100, D=-2.5)
#PID1 = PIDController(P=-42, I=-10, D=-5)

#PID1 = PIDController(P=-32, I=-1, D=-5)
#PID1 = PIDController(P=-25, I=-4.5, D=-5)

#PID1 = PIDController(P=-25, I=-0.04, D=-8)



#PID1 = PIDController(P=-15, I=-1, D=-1)


PID1 = PIDController(P=-13, I=-1, D=-1)




with open("./target_value.txt","r") as file:
	targetvalue=float(file.read())
PID1.setTarget(targetvalue)
while True:
	try:
#		forward(30)
#		time.sleep(2)
#		backward(30)
#		time.sleep(2)
#		stand_still()
#		time.sleep(2)
		accel_data = sensor.get_accel_data()
		gyro_data = sensor.get_gyro_data()
		
		ax = accel_data['x']
		ay = accel_data['y']
		az = accel_data['z']
		
		gx = gyro_data['x']
		gy = gyro_data['y']
		gy = gyro_data['z']
		
		gx -= gyro_offset_x
		gy -= gyro_offset_y
		
		gx_delta = (gx *time_diff)
		gy_delta = (gy *time_diff)
		gx_total += gx_delta
		gy_total += gy_delta
		
		rot_x = x_rotation(ax,ay,az)
		rot_y = y_rotation(ax,ay,az)

		# complementary Filter
		last_x = K *(last_x + gx_delta) + (1-K)*rot_x
		
#		print(last_x)
		PIDx = PID1.step(last_x)
		pid1 = PIDx
#		print pid1	
#		print targetvalue
		PID1.setTarget(targetvalue)
		if finished :
			print kbdInput
			finished = False
			listener = threading.Thread(target=kbdListener)
			listener.start()	
		if kbdInput == "t":
			kbdInput = ""
			targetvalue +=0.2
			PID1.setTarget(targetvalue)

		if kbdInput == "g":
			kbdInput=""
			targetvalue -=0.2
			PID1.setTarget(targetvalue)		
		if kbdInput =="w":
			kbdInput = ""
			PID1.setTarget(targetvalue+5)
		
		if kbdInput =="s":
			kbdInput = ""
			PID1.setTarget(targetvalue-5)
					



		if pid1 > 100:
			pid1 = 100
		if pid1 < -100:
			pid1 = -100
		if pid1 < 0.0:
			backward(-(pid1))
		elif pid1 >0.0:
			forward(pid1)
		else:
			stand_still()
								


		time.sleep(0.01)
	except KeyboardInterrupt:
		pwm_a.stop()
		pwm_b.stop()
		GPIO.cleanup()
		with open("./target_value.txt","w") as file:
			file.write(str(targetvalue))
		exit()
	

