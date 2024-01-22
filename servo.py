#import RPi.GPIO as GPIO
import pigpio
from time import sleep
#import #rospy
import numpy as np
import math

class ControllHandle:
	def __init__(self):
		self.math_pi = math.pi
		#rospy.loginfo('ControllHandle start.')
		self.neutral_duty = 7.500 # [1]
		self.neutral_angle = 90.0 # 度数法
		self.wheel_base = 0.257 # [m]
		self.servocoef = 1.0
		self.freq = 50 # [Hz]
		self.wheelang = 0 # [rad]
		self.servrot = 0 # [deg]
		self.pinnum = 19 # PWM信号を書き出すピンの番号(BOARD指定)
		self.serv_maxrot = self.neutral_angle + 30.0 # 度数法
		self.serv_minrot = self.neutral_angle - 30.0 # 度数法
		self.max_duty = 10.0
		self.min_duty = 5.0
		self.duty = np.float64(0)
		
		self.pi = pigpio.pi()
		self.pi.set_mode(self.pinnum, pigpio.OUTPUT)

		#GPIO.setmode(GPIO.BOARD)		# ピンの指定方法を選ぶ
		#GPIO.setup(self.pinnum, GPIO.OUT)
		#self.pwm = GPIO.PWM(self.pinnum, self.freq) # PWMのインスタンスを作る
		#self.pwm.start(self.neutral_duty)
		#rospy.loginfo('サーボモータの傾きを初期化しました。この状態でタイヤをまっすぐにしてください。5秒スリープします。')
		self.duty = self.neutral_duty
		self.output()
		sleep(5)
		#rospy.loginfo('Initialising ControllHandle is Completed.')

	def output(self):
		print('output: %i' % int(self.duty*10000))
		self.pi.hardware_PWM(self.pinnum, self.freq, int(self.duty*10000))

	def omega2rot(self, linear_vel_x, omega_z): # convert omega to rotate angle
		# [m/s], [rad/s]
		# タイヤ角度の設定
		if linear_vel_x == 0.0:
			self.wheelang = self.wheelang
		else:
			self.wheelang = math.asin(omega_z * self.wheel_base / linear_vel_x) #[rad]

	def wheelrot2servrot(self):
		# タイヤの曲がり角とサーボモーターの曲がり角を揃えるための係数などをここでかける
		ang_d = math.degrees(self.wheelang) # 弧度法表記から度数法表記に変換
		ang_d = ang_d + self.neutral_angle # ang_dは正負の数なので、中心を設定
		self.servrot = ang_d * self.servocoef # サーボモータに設定すべき角度(度数法)
		if self.servrot > self.serv_maxrot:
			#rospy.loginfo('Angle is too big: limited')
			self.servrot = self.serv_maxrot
		elif self.servrot < self.serv_minrot:
			#rospy.loginfo('Angle is too small: limited')
			self.servrot = self.serv_minrot

	def rot2PWM(self):
		duty_unit = (self.max_duty - self.min_duty)/(self.serv_maxrot - self.serv_minrot)
		# サーボの回転1°あたりのdutyの変化量
		self.duty = self.servrot * duty_unit
		if self.duty > self.max_duty:
			#rospy.loginfo('Duty is too big: limited')
			self.duty = self.max_duty
		elif self.duty < self.min_duty:
			#rospy.loginfo('Duty is too small: limited')
			self.duty = self.min_duty
		self.output()

	def controll_handle_loop(self, linear_vel_x, angular_vel_z): # omega[rad/s]
		self.omega2rot(linear_vel_x, angular_vel_z)
		self.wheelrot2servrot()
		self.rot2PWM()

	def handle_stop(self):
		#GPIO.cleanup()
		#rospy.loginfo('ControllHandle is stopped.')
		#self.pwm.stop() #終了
		self.pi.set_mode(self.pinnum, pigpio.INPUT)
		self.pi.stop()
