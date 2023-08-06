import sys
from math import floor, ceil


class Converge():
	'''
	Utility to find valid lower & upper bounds of list.
	'''

	def __init__(self, start, end, callback):
		'''
		Pass random start and end point (both must be vlid, i.e, must be inside bounds),
		and a difference greater than 1 i.e. abs(end-start) > 1,
		with a callback method that will verify whether a prediction is out of bounds or not.
		:param start: lower (known) random bound
		:param end: higher (known) random bound
		:param callback: Verification method
		'''
		self.low = start
		self.high = end
		self.lowStep = (start - end) / 2
		self.highStep = floor((end - start) / 2)
		self.verify = callback

	def run(self):
		while True:  # Converge on low
			IsLowInBounds = self.verify(self.low + self.lowStep)
			if IsLowInBounds:
				self.low = self.low + self.lowStep
				self.lowStep *= 2  # Move faster
			else:
				half = self.lowStep / (2 * 1.0)
				if half < 0:
					half = ceil(half)
				else:
					half = floor(half)
				self.lowStep = half  # Move slower

			if self.lowStep == 0:
				break

		while True:  # Converge on high
			IsHighInBounds = self.verify(self.high + self.highStep)
			if IsHighInBounds:
				self.high = self.high + self.highStep
				self.highStep *= 2  # Move faster
			else:
				half = self.highStep / (2 * 1.0)
				if half < 0:
					half = ceil(half)
				else:
					half = floor(half)
				self.highStep = half  # Move slower

			if self.highStep == 0:
				break

		# IsHighInBounds = self.verify(self.high)
		return (self.low, self.high)


if __name__ == "__main__":
	def check_validity(val):
		if val > -30 and val < 101:
			return True
		else:
			return False


	low, high = Converge(-28, 50, check_validity).run()
	pass
