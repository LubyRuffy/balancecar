import  RPi.GPIO as GPIO
motora_in1 = 21
motora_in2 = 20
motora_pwm = 16

motorb_in1 = 13
motorb_in2 = 19
motorb_pwm = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(motora_in1, GPIO.OUT)
GPIO.setup(motora_in2, GPIO.OUT)
GPIO.setup(motora_pwm, GPIO.OUT)
GPIO.setup(motorb_in1, GPIO.OUT)
GPIO.setup(motorb_in2, GPIO.OUT)
GPIO.setup(motorb_pwm, GPIO.OUT)

pwm_a = GPIO.PWM(motora_pwm, 100)
pwm_b = GPIO.PWM(motorb_pwm, 100)
pwm_a.start(0)
pwm_b.start(0)
