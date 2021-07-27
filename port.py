#!/usr/bin/env python3
import random
import string
import secrets
import sys

if len(sys.argv) <2:
	count = 16
elif len(sys.argv) >2:
	print('Error: invalid argument count!, must one.')
elif int(sys.argv[1]) <1:
	print('Error: invalid number.')
else:
	count = int(sys.argv[1])

for j in range(count):
	k = random.randrange(1024,65534)
	l = random.randrange(10240,65534)
	m = ''.join(secrets.choice(string.digits) for q in range(4))
	n = ''.join(secrets.choice(string.ascii_uppercase) for p in range(4))
	print(f'--- count {j} ---')
	# generate port used for wireguard.
	print(f'TCP port {k} selected.')
	print(f'UDP port {l} selected.')
	# Module keycode generation
	print('module keycode')
	print(f'Keycode {m}-{n}')
