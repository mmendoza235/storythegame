# keypress function modified form code.activestate.com/recipes/...
def keypress():
	"""
	Waits for the user to press a key. Returns the ascii code
	for the key pressed or zero for a function key pressed.
	Aborts function with CTL-C
	"""
	import time, msvcrt
	while 1:
		if msvcrt.kbhit():				# Key pressed?
			a = ord(msvcrt.getch())		# get first byte of keyscan code
			if a == 0 or a == 224:		# is it a function key?
				msvcrt.getch()			# discard second byte of key scan code
				return 0				# return 0
			else:
				return a				# else return ascii code
				
		#for dot in ['.', '..', '...']:
		#	print dot
		#	time.sleep(0.5)
		time.sleep(0.5)					# reduce CPU workload during while execution

def prompt():
	"""
	Simple raw_input with custom prompt.
	Returns the raw_input
	"""
	answer = raw_input('--> ').lower()
	return answer