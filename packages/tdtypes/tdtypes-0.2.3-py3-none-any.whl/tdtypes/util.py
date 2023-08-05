"logging module for the tdtypes package"

__author__ = "Paresh Adhia"
__copyright__ = "Copyright 2016-2017, Paresh Adhia"

class Ident(str):
	"Database Identifier"
	def __str__(self):
		import re

		if re.fullmatch('[a-z#$_][a-z0-9#$_]*', str.__str__(self), re.I):
			return self
		return '"' + str.__str__(self).replace('"', '""') + '"'

	# pylint: disable=locally-disabled, bad-whitespace, multiple-statements
	def __eq__(self, other): return other != None and isinstance(other, str) and self.lower() == other.lower()
	def __lt__(self, other): return other != None and isinstance(other, str) and self.lower() < other.lower()
	def __le__(self, other): return self.__eq__(other) or self.__lt__(other)
	def __ge__(self, other): return not self.__lt__(other)
	def __ne__(self, other): return not self.__eq__(other)
	def __gt__(self, other): return not self.__le__(other)
	def __contains__(self, other): return other != None and isinstance(other, str) and str.__contains__(self.lower(), other.lower())

	def __hash__(self):
		return self.lower().__hash__()


_log_level = None
def getLogger(name):
	"get logger object for the module name"

	global _log_level
	import logging

	logger = logging.getLogger(name)
	if _log_level is None:
		import os
		_log_level = os.environ.get('TDLOGLEVEL', "NOTSET")
		logging.basicConfig(format="%(levelname)s: %(message)s")

	try:
		logger.setLevel(_log_level)
	except ValueError:
		logging.getLogger(__name__).error('"{}" is an invalid value for $TDLOGLEVEL, ignored.'.format(_log_level))
		_log_level = "NOTSET"

	return logger
