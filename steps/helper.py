


def list_to_str(array_var, separator):
	s = ""
	for i in array_var:
		s += str(i)+separator
	return s[:-1]


def is_integer(s, base=10):
	try:
		val = int(s, base)
		return True
	except ValueError:
		return False