import motor_hard
import servo
import numpy as np
import pigpio
from time import sleep

velocity = np.float64() #[m/s]
omega = np.float64() #[rad/s]

input('Enterを押すと、ControllMotorをセットアップします。ESCのセットアップをしてください。')
esc = motor_hard.ControllMotor()
sleep(1)

input('Enterを押すと、ControllHandleをセットアップします。車両のセットアップをしてください')
handle = servo.ControllHandle()
sleep(1)

input('Enterを押すと、制御プログラムのテストを開始します。')

while True:
	try:
		velocity = np.float64(input('velocityを入力してください(-X~X, m/s): '))
	except:
		print("Input Error. velocityは0.0[m/s]になります")
		velocity = np.float64(0.0)
	try:
		omega = np.float64(input('omegaを入力してください(-0.523598~0.523598, rad/s): '))
	except:
		print("Input Error. omegaは0.0[rad/s]になります")
		omega = np.float64(0.0)

	print("入力の通りに3秒間、車体を動作させます。")
	print("velocity: ", velocity)
	print("omega: ", omega)
	pi = pigpio.pi()
	print("pin18_mode: %i" % (pi.get_mode(18)))
	print("pin19_mode: %i" % (pi.get_mode(19)))
	handle.controll_handle_loop(velocity, omega)
	esc.controll_motor_loop(velocity)
	sleep(3)
	handle.controll_handle_loop(0.0, 0.0)
	esc.controll_motor_loop(0.0)
	print("動作終了。ループします。")
	sleep(1)




