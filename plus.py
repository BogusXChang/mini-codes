#!/usr/bin/python3
import sys
def is_integer(n):
	try:
		float(n)
	except ValueError:
		return False
	else:
		return float(n).is_integer()

if len(sys.argv) != 3:
	print('must 2 arguments')
elif (not is_integer(sys.argv[1]) or not is_integer(sys.argv[2])):
	print('not integer')
else:
	print(f'{sys.argv[1]} + {sys.argv[2]} = {int(sys.argv[1])+int(sys.argv[2])}')
