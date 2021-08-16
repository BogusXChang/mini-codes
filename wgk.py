import ipaddress as ipa
import secrets as sec
from subprocess import check_output
import requests as req

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
#generate a list of key
def skeylist(psk=False):
	klist = list()
	if psk:
		klist.append(rrs(check_output(['wg','genpsk'])))
	pk = check_output(['wg','genkey'])
	klist.append(rrs(pk))
	pbk = rrs(check_output(['wg','pubkey'],input=pk))
	klist.append(pbk)
	return klist

if __name__ == '__main__':
	c = 0
	count = 16
	server_key = skeylist()
	server_address = req.get('https://ifconfig.me').text
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
				sfile.write(f'PrivateKey = {server_key[0]}\n')
				sfile.close()
			c = c + 1
		elif(c <= count):
			fn = f'client_{c}.conf'
			client_key = skeylist()
			clport = port()
			print(f'Adding peer {c} to server.conf.')
			with open('server.conf','a') as sfile:
				sfile.write('\n')
				sfile.write('[Peer]\n')
				sfile.write(f'PublicKey = {client_key[1]}\n')
				sfile.write(f'AllowIPs = {iplist[c]}/32\n')
				sfile.close()
			print(f'Writing {fn}.')
			with open(fn,'a') as cfile:
				cfile.write('[Interface]\n')
				cfile.write('Address = {iplist[c]}/24\n')
				cfile.write('ListenPort = {clport}\n')
				cfile.write('PrivateKey = {client_key[0]}\n')
				cfile.write('MTU = 1420\n')
				cfile.write('\n')
				cfile.write('[Peer]\n')
				cfile.write('PublicKey = {server_key[1]}\n')
				cfile.write('AllowIPs = {iplist[0]}/32\n')
				cfile.write('EndPoint = {server_address}:{lport}\n')
				cfile.close()
			c = c + 1
		else:
			print('create {c} configuraton files finished.')
			break
