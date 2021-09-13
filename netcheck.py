#!/usr/bin/python3.9
# add checkip module, it's more elegent.
import argparse as apr
import ipaddress as ipa
import checkip as cip
# comment out as legacy reference
#def netcheck(addr,IPv4=True):
#	try:
#		if IPv4:
#			nci = ipa.IPv4Network(addr)
#		else:
#			nci = ipa.IPv6Network(addr)
#	except ValueError:
#		pass
#	except NetwmaskValueError:
#		pass
#	else:
#		pfx = nci.prefixlen
#	finally:
#		if ('nci' not in locals() or 'nci' not in globals()):
#			return False
#		else:
#			return pfx

if __name__ = '__main__':
	ar = apr.ArgumentParser(prog='netcheck.py',description='Check if a address is valid.')
	ar.add_argument("addr",nargs='?',type=str,default="192.168.1.1",help="Address to check")
	ap = ar.parse_args()
	if cip.v4_prefix(ap.addr):
		print(f'check ok. prefixlen:{cip.v4_prefix(ap.addr)}.')
	else:
		print(f' {ap.addr} is not a valid network prefix.')
