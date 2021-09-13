import ipaddress as ipa
import secrets as sec
from subprocess import check_output
import requests as req
# Initially implementation argparse module.
import argparse as parg
ap = parg.ArgumentParser(prog='wgk2',description='generate Wireguard configuration.')
ap.addArgument("count",type=int,default=16,nargs='?',help="Number of configuration files generated. default: 16")
ap.addArgument("-s","--preshared",action="store_true",help="Use pre-shared Keys.")
ap.addArgument("-S","--server",action="store_true",help="Server mode .")
# required wireguard-tools to work.
ipnet = ipa.IPv4Network('172.17.1.0/24')
#Add Hex strip to future function addition.
def hexstrip(intstr):
	return(hex(intstr)[2:])
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
	count = ag.count
	psk = ag.preshared
	server_address = req.get('https://ifconfig.me').text
	server_key = skeylist()
	lport = port()
	iplist = list(ipnet.hosts())
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
					sfile.write("PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE")
				sfile.close()
			c = c + 1
		elif(c <= count):
			fn = f'client_{c}.conf'
			if psk == True:
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
				sfile.write(f'AllowIPs = {iplist[c]}/32\n')
				sfile.close()
			print(f'Writing {fn}.')
			with open(fn,'a') as cfile:
				cfile.write('[Interface]\n')
				cfile.write('Address = {iplist[c]}/24\n')
				cfile.write('ListenPort = {clport}\n')
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
				else:
					cfile.write(f'AllowIPs = {iplist[0]}/32\n')
				cfile.write('EndPoint = {server_address}:{lport}\n')
				cfile.close()
			c = c + 1
		else:
			print('create {c} configuraton files finished.')
			break
