class ServoDetails(object):
	def __init__(self, _pin, _min=500, _max=2500):
		self.__pin = _pin
		if not self.__check_pw(_min) or not self.__check_pw(_max):
			raise ValueError("Given min or max pulsewidth is invalid")
		self.__min = _min
		self.__max = _max
		self.__pos = None

	def __check_pw(self, pw):
		if pw >= 500 and pw <= 2500:
			return True
		return False

	@property
	def pin(self):
		return self.__pin

	@property
	def min(self):
		return self.__min

	@property
	def max(self):
		return self.__max

	@property
	def pos(self):
		return self.__pos

	@pos.setter
	def pos(self, pos):
		if pos > 180 or pos < 0:
			raise ValueError("Invalid servo position: " + str(pos))
		self.__pos = pos

	@property
	def pulsewidth(self):
		return int(self.__pos / float(180) * (self.max - self.min) + self.min)
