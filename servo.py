
import pigpio
from time import sleep
import numpy as np
import math

class ControllHandle:
	def __init__(self):
		self.math_pi = math.pi
		self.neutral_pulse = 1500 #[us]
		self.neutral_angle = 90.0 # 度数法
		self.wheel_base = 0.257 # [m]
		self.servocoef = 1.0 #[1]
		#self.freq = 50 # [Hz]
		self.wheelang = np.float64() # [rad]
		self.servrot = 0 # [deg]
		self.pinnum = 19 # PWM信号を書き出すピンの番号(GPIO指定)
		self.serv_maxrot = self.neutral_angle + 30.0 # 度数法[deg]
		self.serv_minrot = self.neutral_angle - 30.0 # 度数法[deg]
		self.pulse = np.int64() #[us]
		self.max_pulse = 300 #[us]
		
		self.pi = pigpio.pi()
		self.pi.set_mode(self.pinnum, pigpio.OUTPUT)
		self.pulse = self.neutral_pulse
		self.output()
		sleep(5)

	def output(self):
		self.pi.set_servo_pulsewidth(self.pinnum, self.pulse)

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
			self.servrot = self.serv_maxrot
		elif self.servrot < self.serv_minrot:
			self.servrot = self.serv_minrot

	def rot2PWM(self):
		pulse_unit = (self.max_pulse*2)/(self.serv_maxrot - self.serv_minrot)
		# サーボの回転1°あたりのパルス幅の変化量
		self.pulse = self.servrot * pulse_unit
		if self.pulse > self.max_pulse + self.neutral_pulse:
			self.pulse = self.max_pulse + self.neutral_pulse
		elif self.pulse < -self.max_pulse + self.neutral_pulse:
			self.pulse = -self.min_pulse + self.neutral_pulse
		elif self.servrot == neutral_angle:
			self.pulse = self.neutral_pulse
		self.output()

	def controll_handle_loop(self, linear_vel_x, angular_vel_z): # omega[rad/s]
		self.omega2rot(linear_vel_x, angular_vel_z)
		self.wheelrot2servrot()
		self.rot2PWM()

	def handle_stop(self):
		self.pulse = 0
		self.output()
		self.pi.set_mode(self.pinnum, pigpio.INPUT)
		self.pi.stop()
