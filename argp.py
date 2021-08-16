import argparse as argp
import ipaddress as ipa
ap = argp.ArgumentParser()
apg = ap.add_mutually_exclusive_group()
apg.add_argument("-4","--ipv4",action="store_true",help="check IPv4 addresses.")
apg.add_argument("-6","--ipv6",action="store_true",help="check IPv6 addresses.")
ap.add_argument("addr",nargs='+',help="IP addresses")
args = ap.parse_args()

# the Ke-P function
def kp4(str):
	bad = 0
	if (str.find(':') == -1):
		bad = bad + 1
	else:
		return False
	if (str.find('.') != -1):
		bad = bad + 1
	else:
		return False
	if bad == 2:
		return True

if args.ipv6:
	for adr in args.addr:
		# katch the Ke-P
		if kp4(adr): print(f' {adr} is not a IPv6 address.')
		try:
			adx = ipa.IPv6Address(adr)
		except ValueError:
			pass
		else:
			if adx.ipv4_mapped:
				print(f' {adr} is a v4 address packed in v6.')
			else:
				print(f' {adr} is a IPv6 address.')
#				print(f' {adx.prefixlen} prefix.')
		finally:
			if not ('adx' in locals() or 'adx' in globals()):
				print(f' {adr} is not a IPv6 address.')
elif args.ipv4:
	for adr in args.addr:
		try:
			adc = ipa.IPv4Address(adr)
		except ValueError:
			pass
		else:
			print(f'{adr} is a IPv4 address.')
#			print(f'/{adx.prefixlen} prefix.')
		finally:
			if not ( 'adc' in locals() or 'adc' in globals()):
				print(f' {adr} is not a IPv4 address.')
else:
	print('Error: please specify address family.')
