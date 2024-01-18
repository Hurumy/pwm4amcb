import motor
import servo
from time import sleep

velocity = float64 #[m/s]
omega = float64 #[rad/s]

input('Enterを押すと、ControllMotorをセットアップします。ESCのセットアップをしてください。')
esc = ControllMotor()
sleep(1)

input('Enterを押すと、ControllHandleをセットアップします。車両のセットアップをしてください')
handle = ControllHandle()
sleep(1)

input('Enterを押すと、制御プログラムのテストを開始します。')

while True:
	try:
		velocity = float(input('velocityを入力してください(-X~X, m/s): '))
	except:
		print("Input Error. velocityは0.0[m/s]になります")
		velocity = float(0.0)
	try:
		omega = float(input('omegaを入力してください(-1/6pi~1/6pi, rad/s): '))
	except:
		print("Input Error. omegaは0.0[rad/s]になります")
		omega = float(0.0)
	print("入力の通りに3秒間、車体を動作させます。")
	print("velocity: ", velocity)
	print("omega: ", omega)
	esc.controll_motor_loop(velocity)
	handle.controll_handle_loop(velocity, omega)
	sleep(3)
	print("動作終了。ループします。")
	sleep(1)




