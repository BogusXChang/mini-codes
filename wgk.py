import ipaddress as ipa
import secrets as sec
from subprocess import check_output
import requests as req
import cip
# Initially implementation argparse module.
import argparse as parg
ap = parg.ArgumentParser(prog='wgk2',description='generate Wireguard configuration.')
ap.addArgument("count",type=int,default=16,nargs='?',help="Number of configuration files generated. default: 16")
ap.addArgument("prefix",type=str,default="DEF",nargs='?',help="IPv4 prefix ,default: random generated RFC1918 /24 prefix.")
ap.addArgument("-6","--ipv6",type=str,default="DEF",nargs='?',help="IPv6 prefix ,default: Random RFC4197 ULA /64 prefix.")
ap.addArgument("-s","--preshared",action="store_true",help="Use pre-shared Keys.")
ap.addArgument("-S","--server",action="store_true",help="Server mode .")
# prefix list.
rfc1918_prefixes = list(IPv4Network('192.168.0.0/16').subnets(new_prefix=24))
rfc1918_prefixes.extend(list(IPv4Network('172.16.0.0/12').subnets(new_prefix=24)))
rfc1918_prefixes.extend(list(IPv4Network('10.0.0.0/8').subnets(new_prefix=24)))
def random_prefix(IPv4=True):
	if IPv4:
		return rfc1918_prefixes[sec.randrange(69888)]
	else:
		al = list()
		for k in range(4):
			if k == 0:
				ri = sec.randbits(8)
				if ri < 16:
					al.append('fd{}'.format(hexstrip(ri).zfill(2)))
				else:
					al.append(f'fd{hexstrip(ri)}')
			else:
				al.append(hexstrip(sec.randbits(16)))
		rad = ':'.join(al)
	return IPv6Network(f'{rad}::/64')
# required wireguard-tools to work.
def hexstrip(intstr):
	return hex(intstr)[2:]
#generate port number
def port():
	return 1025+sec.randbelow(64509)
#remove newline
def rrs(str):
	# string-bytes problemic.
	return str.decode().rstrip('\n')
#generate a dictionary of key
def skeylist(psk=False):
	klist = {}
	if psk:
		klist ['psk'] = rrs(check_output(['wg','genpsk']))
	pk = check_output(['wg','genkey'])
	klist['private'] = rrs(pk)
	klist['public'] = rrs(check_output(['wg','pubkey'],input=pk))
	return klist

if __name__ == '__main__':
	c = 0
	ag = ap.parse_args()
	if ag.prefix == "DEF"
		ipnet=random_prefix()
	elif v4_prefix(ag.prefix):
		ipnet=ipa.IPv4Network(ag.prefix)
	else:
		print("Warning: network specified is invalid. Use random ULA.")
		ipnet=random_prefix()
	count = ag.count
	psk = ag.preshared
	server_address = req.get('https://ifconfig.me').text
	server_key = skeylist()
	lport = port()
	iplist = list(ipnet.hosts())
	if ag.server and ag.ipv6:
		if ag.ipv6 == "DEF":
			prefix6 = random_prefix(IPv4=False)
		elif cip.v6_prefix(ag.ipv6):
			prefix6 = ipa.IPv6Network(ag.ipv6)
		else:
			print("WARNING: prefix invalid , use ULA.")
			prefix6 = random_prefix(IPv4=False)
	while True:
		if (c == 0):
			fn = "server.conf"
			print(f'Writing {fn}.')
			with open(fn,'w') as sfile:
				sfile.write('[Interface]\n')
				sfile.write(f'Address = {iplist[c]}/24\n')
				sfile.write(f'ListenPort = {lport}\n')
				sfile.write('PrivateKey = {}\n'.format(klist['private']))
				# Server mode.
				if ag.server:
					sfile.write("# please change eth0 to real internet-connected interface.")
					sfile.write("PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
					if ag.ipv6:
						sfile.write('PostUp = echo 1 > /proc/sys/net/ipv6/conf/eth0/proxy_ndp \n')
						for k in range(ag.count):
							sfile.write(f'PostUp = ip neigh add proxy {prefix6[k+1]} dev eth0 \n')
					sfile.write("PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE")
					if ag.ipv6:
						sfile.write('PostDown = echo 0 > /proc/sys/net/ipv6/conf/eth0/proxy_ndp \n')
						for k in range(ag.count):
							sfile.write(f'PostDown = ip neigh del proxy {prefix6[k+1]} dev eth0')
				sfile.close()
			c = c + 1
		elif(c <= count):
			fn = f'client_{c}.conf'
			if psk:
				client_key = skeylist(psk=True)
			else:
				client_key = skeylist()
			clport = port()
			print(f'Adding peer {c} to server.conf.')
			with open('server.conf','a') as sfile:
				sfile.write('\n')
				sfile.write('[Peer]\n')
				if psk == True:
					sfile.write('PresharedKey = {}\n'.format(client_key['psk']))
				sfile.write('PublicKey = {}\n'.format(client_key['public']))
				if ag.ipv6:
					sfile.write(f"AllowIPs {iplist[c]}/32} , {prefix6[c+1]}/128")
				else:
					sfile.write(f'AllowIPs = {iplist[c]}/32\n')
				sfile.close()
			print(f'Writing {fn}.')
			with open(fn,'a') as cfile:
				cfile.write('[Interface]\n')
				cfile.write(f'Address = {iplist[c]}/24\n')
				cfile.write(f'ListenPort = {clport}\n')
				cfile.write('PrivateKey = {}\n'.format(client_key['private']))
				cfile.write('MTU = 1420\n')
				cfile.write('\n')
				cfile.write('[Peer]\n')
				if psk == True:
					cfile.write('PresharedKey = {}\n'.format(client_key['psk']))
				cfile.write('PublicKey = {}\n'.format(client_key['public']))
				# Server mode.
				if ag.server:
					cfile.write("AllowedIPs = 0.0.0.0/0, ::/0")
				elif ag.ipv6:
					cfile.write(f"AllowIPs = {iplist[0]}/32 , {prefix6[1]}/128 \n")
				else:
					cfile.write(f'AllowIPs = {iplist[0]}/32\n')
				cfile.write(f'EndPoint = {server_address}:{lport}\n')
				cfile.close()
			c = c + 1
		else:
			print(f'create {c} configuraton files finished.')
			break
