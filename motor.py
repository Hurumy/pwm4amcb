import RPi.GPIO as GPIO
from time import sleep
import rospy
import math

class ControllMotor:
	def __init__(self):
        self.pi = math.pi
        rospy.loginfo('ControllMotor start.')
        self.neutral_duty = 7.500
        self.freq = 50
        self.motor_rpm = Int64()
        self.duty = Int64()
        self.pinnum = 12 # PWM信号を書き出すピンの番号(BOARD指定)
        GPIO.setmode(GPIO.BOARD)		# ピンの指定方法を選ぶ
        GPIO.setup(self.pinnum, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pinnum, self.freq) # PWMのインスタンスを作る
        rospy.loginfo('ESC Calibration start.')
        self.pwm.start(self.neutral_duty)
        sleep(5)
        rospy.loginfo('ESC Calibration end.')
        rospy.loginfo('Initialising ControllMotor Completed.')

    def output(self):
        self.pwm.ChangeDutyCycle(self.duty)

    def vel2rpm(self, linear_vel_x): # convert speed to rpm
        # [m/s]
        if linear_vel_x <= 0:
            return 0
        wheel_size = 0.063 # wheel size [m]
        wheel_speed = linear_vel_x / (wheel_size * 2 * self.pi) # wheel_speed [1/s]
        self.motor_rpm = wheel_speed * 8.27 * 60 # gear ratio = 8.27:1

    def rpm2duty(self): # convert rpm to duty
        max_rpm = 12000
        max_duty = 8.8
        min_rpm = 0
        min_duty = self.neutral_duty
        rpm_rate = (max_rpm-min_rpm)/(max_duty-min_duty) # 1%に対するrpm
        if self.motor_rpm >= 0:
            self.duty = self.motor_rpm / rpm_rate + min_duty
        #速度制約
        if self.duty > max_duty:
            rospy.loginfo('Speed is too high: limited')
            self.duty = max_duty
        elif self.duty < min_duty:
            rospy.loginfo('Speed is too low: limited')
            self.duty = min_duty

    def duty2PWM(self):
        if self.motor_rpm == 0:
            self.pwm.ChangeDutyCycle(self.neutral_duty)
        else:
            output()

    def controll_motor_loop(self, vel_x):
        vel2rpm(vel_x)
        rpm2duty()
        duty2PWM()

    def motor_stop(self):
        GPIO.cleanup()
        rospy.loginfo('ControllMotor is stopped.')
        self.pwm.stop()#終了





