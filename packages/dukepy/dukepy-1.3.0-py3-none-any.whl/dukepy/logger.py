from colorama import Fore, Style
from enum import Enum
from functools import total_ordering


class Logger:
	indents = 0
	indentsFlag = True

	@total_ordering
	class Levels:
		# __order__ = "CRITICAL FATAL ERROR SUCCESS WARNING NOTICE INFO VERBOSE DEBUG SPAM ALL"
		NONE = 100
		""" No log is printed if level==NONE"""
		OUTPUT = 55
		CRITICAL = 50
		FATAL = CRITICAL
		ERROR = 40
		SUCCESS = 35
		WARNING = 30
		NOTICE = 25
		INFO = 20
		VERBOSE = 15
		DEBUG = 10
		SPAM = 5
		ALL = 0

		def __lt__(self, other):
			if self.__class__ is other.__class__:
				return self.value < other.value

	level = Levels.ALL
	"""The logs levels below this level are filtered. eg. if level==Level.DEBUG then spam() won't print anything."""

	def __init__(self):
		import colorama
		colorama.init()
		pass

	def spam(self, msg):
		if self.level <= self.Levels.SPAM:
			print(Fore.WHITE + "SPAM: " + msg + Style.RESET_ALL)

	def debug(self, msg, indentOffset=0):
		"""
		Print debug logs.
		:param msg: The string to print.
		:param indentOffset: Increment/Decrement in indent space (must provide at least 0, if indent to be printed)
		:return:
		"""
		if self.level <= self.Levels.DEBUG:
			if indentOffset:
				self.printIndent(indentOffset)
			print(Fore.GREEN + "DEBUG: " + msg + Style.RESET_ALL)

	def verbose(self, msg):
		if self.level <= self.Levels.VERBOSE:
			print(Fore.MAGENTA + "VERBOSE: " + msg + Style.RESET_ALL)

	def info(self, msg):
		if self.level <= self.Levels.INFO:
			print(Fore.WHITE + Style.BRIGHT + "INFO: " + msg + Style.RESET_ALL)

	def notice(self, msg):
		if self.level <= self.Levels.NOTICE:
			print(Fore.RED + "NOTICE: " + msg + Style.RESET_ALL)

	def warning(self, msg):
		if self.level <= self.Levels.WARNING:
			print(Fore.YELLOW + Style.BRIGHT + "WARNING: " + msg + Style.RESET_ALL)

	def success(self, msg):
		if self.level <= self.Levels.SUCCESS:
			print(Fore.GREEN + Style.BRIGHT + "SUCCESS: " + msg + Style.RESET_ALL)

	def error(self, msg):
		if self.level <= self.Levels.ERROR:
			print(Fore.RED + Style.BRIGHT + "ERROR: " + msg + Style.RESET_ALL)

	def fatal(self, msg):
		if self.level <= self.Levels.FATAL:
			print(Fore.MAGENTA + Style.BRIGHT + "FATAL: " + msg + Style.RESET_ALL)

	def critical(self, msg):
		if self.level <= self.Levels.CRITICAL:
			print(Fore.MAGENTA + Style.BRIGHT + "CRITICAL: " + msg + Style.RESET_ALL)

	def output(self, msg):
		if self.level <= self.Levels.OUTPUT:
			try:
				print(msg)
			except UnicodeEncodeError as e:
				pass
			except IOError as e:
				pass

	def printIndent(self, indentOffset):
		if indentOffset > 0:
			self.indents += indentOffset

		if self.indents < 0:
			self.indents = 0
		indentSpace = ""
		for i in range(0, self.indents):
			indentSpace += "  "
		print(indentSpace)

		if indentOffset < 0:
			self.indents += indentOffset
