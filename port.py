#!/usr/bin/env python3
import random
import string
import secrets

for j in range(16):
	k = random.randrange(1024,65534)
	l = random.randrange(10240,65534)
	m = ''.join(secrets.choice(string.digits) for q in range(4))
	n = ''.join(secrets.choice(string.ascii_uppercase) for p in range(4))
	print(f'--- count {j} ---')
	print(f'TCP port {k}')
	print(f'UDP port {l}')
	print(f'Keycode {m}-{n}')
