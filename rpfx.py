from ipaddress import IPv4Network,IPv6Network
from random import getrandbits,randrange
# Generate IPv4 RFC1918, IPv6 RFC 4193 ULA prefix.
# return IPv4Network / IPv6Network object.
rfc1918_prefixes = list(IPv4Network('192.168.0.0/16').subnets(new_prefix=24))
rfc1918_prefixes.extend(list(IPv4Network('172.16.0.0/12').subnets(new_prefix=24)))
rfc1918_prefixes.extend(list(IPv4Network('10.0.0.0/8').subnets(new_prefix=24)))
def hxs(str):
	return hex(str)[2:]
def random_prefix(IPv4=True):
	if IPv4:
		return rfc1918_prefixes[randrange(69888)]
	else:
		al = list()
		for k in range(4):
			if k == 0:
				ri = getrandbits(8)
				if ri < 16:
					al.append('fd{}'.format(hxs(ri).zfill(2)))
				else:
					al.append(f'fd{hxs(ri)}')
			else:
				al.append(hxs(getrandbits(16)))
		rad = ':'.join(al)
	return IPv6Network(f'{rad}::/64')

if __name__ == '__main__':
	import argparse as argp
	ap = argp.ArgumentParser(prog='rpfx.py',description="Generate random IPv4/IPv6 Prefixes.")
	ap.add_argument("count",type=int,nargs='?',default=16,help="number of random prefixes")
	ap.add_argument("-6","--ipv6",action="store_true",help="Generate IPv6 ULA /64 prefixes.")
	arg = ap.parse_args()
	for c in range(arg.count):
		if arg.ipv6:
			print(f'v6 prefix {random_prefix(IPv4=False)}')
		else:
			print(f'prefix {random_prefix()}')		

