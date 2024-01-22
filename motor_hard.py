
import pigpio
from time import sleep
import numpy as np
import math

class ControllMotor:
	def __init__(self):
		self.math_pi = math.pi
		self.rev = False
		self.wheel_size = 0.063 # wheel size [m]
		self.gearratio = 8.27
		self.neutral_pulse = 1500
		#self.freq = 50
		self.motor_rpm = np.int64(0)
		self.pulse = np.int64(0)
		self.max_rpm = 4000.0
		self.min_rpm = 0.0
		self.max_pulse_plus = 98.193547
		self.min_pulse_plus = 83.568976
		self.max_pulse_minus = 112.818118
		self.min_pulse_minus = 104.461221
		#self.min_pulse = 30
		self.pinnum = 18 # PWM信号を書き出すピンの番号(BOARD指定)

		self.pi = pigpio.pi()
		self.pi.set_mode(self.pinnum, pigpio.OUTPUT)
		# キャリブレーションのためにニュートラルに設定
		self.pulse = self.neutral_pulse
		self.output()
		sleep(5)

	def output(self):
		self.pi.set_servo_pulsewidth(self.pinnum, self.pulse)

	def vel2rpm(self, linear_vel_x): # convert speed to rpm
		# [m/s]
		# スピードが負ならバックモードをTrueにする
		if linear_vel_x < 0.0:
			self.rev = True
			linear_vel_x = linear_vel_x * -1
		else:
			self.rev = False
		wheel_speed = linear_vel_x / (self.wheel_size * 2.0 * self.math_pi) # wheel_speed [1/s]
		# スピードが0ならブレーキをかける
		if linear_vel_x == 0.0:
			self.motor_rpm = 0.0
		else:
			self.motor_rpm = wheel_speed * self.gearratio * 60.0
	
	def rpm2pulse(self):
		# RPM1あたりのパルス幅を調べる
		# pul_widは必ず正 pulse = neutral_pulse +-(motor_rpm / pul_wid)
		if self.rev == False:
			pul_wid = (self.max_rpm - self.min_rpm) / self.max_pulse_plus - self.min_pulse_plus
		else:
			pul_wid = (self.max_rpm - self.min_rpm) / self.max_pulse_minus - self.min_pulse_minus
		if self.motor_rpm == 0.0:
			self.pulse = self.neutral_pulse
		elif self.rev == False:
			self.pulse = self.neutral_pulse + (-self.motor_rpm / pul_wid)
		elif self.rev == True:
			self.pulse = self.neutral_pulse + (self.motor_rpm / pul_wid)
		self.rev = False

	def controll_motor_loop(self, vel_x):
		self.vel2rpm(vel_x)
		self.rpm2pulse()
		self.output()

	def motor_stop(self):
		self.pulse = 0
		self.output()
		self.pi.set_mode(self.pinnum, pigpio.INPUT)
		self.pi.stop()

