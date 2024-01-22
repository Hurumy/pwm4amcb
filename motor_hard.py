#import RPi.GPIO as GPIO
#import wiringpi
import pigpio
from time import sleep
import numpy as np
#import #rospy
import math

class ControllMotor:
	def __init__(self):
		self.math_pi = math.pi
		#rospy.loginfo('ControllMotor start.')
		self.rev = False
		self.wheel_size = 0.063 # wheel size [m]
		self.gearratio = 8.27
		self.neutral_duty = 7.500000
		self.freq = 50
		self.motor_rpm = np.int64(0)
		self.duty = np.float64(0)
		self.max_rpm = 12000
		self.min_rpm = 0
		# maxduty != mindutyじゃないとゼロ除算になります
		self.max_duty = self.neutral_duty + 0.8
		self.min_duty = self.neutral_duty - 0.8
		self.pinnum = 18 # PWM信号を書き出すピンの番号(BOARD指定)

		self.pi = pigpio.pi()
		self.pi.set_mode(self.pinnum, pigpio.OUTPUT)

		#wiringpi.wiringPiSetup()
		#wiringpi.pinMode(self.pinnum, wiringpi.GPIO.PWM_OUTPUT)
		#wiringpi.pwmSetMode(wiringpi.PWM_MODE_BAL)
		#wiringpi.pwmSetRange(1920)
		#wiringpi.pwmSetClock(200)
		#GPIO.setmode(GPIO.BOARD)		# ピンの指定方法を選ぶ
		#GPIO.setup(self.pinnum, GPIO.OUT)
		#self.pwm = GPIO.PWM(self.pinnum, self.freq) # PWMのインスタンスを作る
		#rospy.loginfo('ESC Calibration start.')
		#self.pwm.start(self.neutral_duty)

		self.duty = self.neutral_duty
		self.output()
		sleep(5)
		#rospy.loginfo('ESCから、1回の長いビープ音がしたことを確認してください。していなければ、再実行してください。')
		#rospy.loginfo('ESC Calibration end.')
		#rospy.loginfo('Initialising ControllMotor Completed.')

	def output(self):
		#self.pwm.ChangeDutyCycle(self.duty)
		print('output: %i' % int(self.duty*10000))
		self.pi.hardware_PWM(self.pinnum, self.freq, int(self.duty*10000))

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
			self.motor_rpm = 0
		else:
			self.motor_rpm = wheel_speed * self.gearratio * 60.0

	def rpm2duty(self): # convert rpm to duty
		rpm_rate = (self.max_rpm-self.min_rpm)/(self.max_duty-self.neutral_duty) # 1%に対するrpm
		duty_diff = self.motor_rpm / rpm_rate
		if self.rev == False and self.motor_rpm > 0:
			self.duty = self.neutral_duty + duty_diff
		elif self.rev == True and self.motor_rpm > 0:
			self.duty = self.neutral_duty - duty_diff
		elif self.motor_rpm == 0:
			self.duty = self.neutral_duty

		#速度制約
		if self.duty > self.max_duty:
			#rospy.loginfo('Speed is too high: limited')
			self.duty = self.max_duty
		elif self.duty < self.min_duty:
			#rospy.loginfo('Rev Speed is too high: limited')
			self.duty = self.min_duty

	def duty2PWM(self):
		if self.motor_rpm == 0:
			#self.pwm.ChangeDutyCycle(self.neutral_duty)
			self.pi.hardware_PWM(self.pinnum, self.freq, int(self.neutral_duty * 10000))
		else:
			self.output()

	def controll_motor_loop(self, vel_x):
		self.vel2rpm(vel_x)
		self.rpm2duty()
		self.duty2PWM()

	def motor_stop(self):
		#rospy.loginfo('ControllMotor is stopped.')
		#self.pwm.stop() #終了
		#wiringpi.pwmWrite(self.pinnum, 0.0)
		self.pi.set_mode(self.pinnum, pigpio.INPUT)
		self.pi.stop()




