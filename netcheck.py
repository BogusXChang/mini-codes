#!/usr/bin/python3.9

import sys
import ipaddress as ipa

def netcheck(addr,IPv4=True):
	try:
		if IPv4:
			nci = ipa.IPv4Network(addr)
		else:
			nci = ipa.IPv6Network(addr)
	except ValueError:
		pass
	except NetwmaskValueError:
		pass
	else:
		pfx = nci.prefixlen
	finally:
		if ('nci' not in locals() or 'nci' not in globals()):
			return False
		else:
			return pfx

if __name__ = '__main__':
	if netcheck('192.168.1.1'):
		print('check ok.')
