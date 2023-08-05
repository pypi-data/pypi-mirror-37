import pigpio

from resettabletimer import ResettableTimer

from piservopantilt import ServoDetails

class ServoControl(object):
	def __init__(self, pan_pin=12, tilt_pin=18, pan_limits=(500,2500),tilt_limits=(500,2500), initial_position=(90,90), auto_off=1.5):
		self.__pi = pigpio.pi()
		self.__pan = ServoDetails(pan_pin, *pan_limits)
		self.__tilt = ServoDetails(tilt_pin, *tilt_limits)

		if auto_off:
			self.__auto_off_timer = ResettableTimer(auto_off, self.off)
			self.__auto_off_timer.start()
		else:
			self.__auto_off_timer = None

		# Move to initial position to have servos in known position
		self.move_to(*initial_position)

	def __set_pw(self, servo, pw=None):
		# TODO: check input pw validity
		if pw is None:
			pw = servo.pulsewidth
		return self.__pi.set_servo_pulsewidth(servo.pin, pw)

	@property
	def position(self):
		return {
			"pan": self.__pan.pos,
			"tilt": self.__tilt.pos
		}

	def move_to(self, pan=None,tilt=None):
		if pan is not None:
			self.__pan.pos = pan
			self.__set_pw(self.__pan)
		if tilt is not None:
			self.__tilt.pos = tilt
			self.__set_pw(self.__tilt)
		if self.__auto_off_timer is not None:
			self.__auto_off_timer.reset()

	def off(self):
		for servo in [self.__pan, self.__tilt]:
			self.__set_pw(servo, 0)

	def min(self):
		self.move_to(0,0)

	def max(self):
		self.move_to(180,180)
