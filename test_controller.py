import motor
import servo
import numpy as np
import RPi.GPIO as GPIO
from time import sleep

GPIO.cleanup()

velocity = np.float64(0) #[m/s]
omega = np.float64(0) #[rad/s]

speed = 3.75
angle = 0
bre = 0
acc = 0.05
rot = 0.03

print('このプログラムはコントローラーです。')
print('W:アクセル S:ブレーキ A:左回転 D:右回転 R:加速 F:減速 です。')
input('Enterを押すと、ControllMotorをセットアップします。ESCのセットアップをしてください。')
esc = motor.ControllMotor()
sleep(1)

input('Enterを押すと、ControllHandleをセットアップします。車両のセットアップをしてください')
handle = servo.ControllHandle()
sleep(1)

input('Enterを押すと、コントローラを開始します。')

while True:
    char = input()
    if char == 'w' or char == 'W':
        velocity = speed
        omega = angle
    elif char == 's' or char == 'S':
        velocity = bre
        omega = angle
    elif char == 'a' or char == 'A':
        velocity = speed
        angle = angle - rot
        omega = angle
    elif char == 'd' or char == 'D':
        velocity = speed
        angle = angle + rot
        omega = angle
    elif char == 'r' or char == 'R':
        speed = speed + acc
        velocity = speed
        omega = angle
    elif char == 'f' or char == 'F':
        speed = speed - acc
        velocity = speed
        omega = angle
	print("velocity: ", velocity)
	print("omega: ", omega)
	esc.controll_motor_loop(velocity)
	handle.controll_handle_loop(velocity, omega)
	sleep(0.03)