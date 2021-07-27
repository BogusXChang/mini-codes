import ipaddress

try:
	ipad = ipaddress.IPv4Network('192.168.1.0/25')
except ValueError:
	pass
except NetMaskValueError:
	pass
else:
	ave = False
	nve = False
	print(f' Netmask is {ipad.prefixlen}.')
finally:
	if ('ipad' not in locals() or 'ipad' not in globals()):
		print('not a valid address or netmask')
	else:
		print('done')
