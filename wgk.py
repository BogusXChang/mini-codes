import ipaddress as ipa
import secrets as sec
from subprocess import check_output
import requests as req

ipnet = ipa.IPv4Network('172.17.1.0/24')
#generate port number
def port():
	return 1025+sec.randbelow(64509)
#remove newline
def rrs(str):
	retrun str.rstrip('\n')
#generate a list of key
def skeylist(psk=False):
	klist=list()
	if psk:
		klist.append(rrs(check_output(['wg','genpsk'])))
	pk=rrs(check_output(['wg','genkey']))
	klist.append(ppk)
	pbk=rrs(check_output(['wg','pubkey'],input=ppk))
	klist.append(pbk)
	return klist

if '__name__'=='__main__':
	count=16
	server_key = skeylist()
	server_address = req.get('https://ifconfig.me').text()
	lport = port()
	iplist=list(ipnet.hosts())
	for c in range(count):
		if c = 0:
			fn = "server.conf"
			print(f'Writing {fn}.')
			with open(fn,'w') as sfile:
				sfile.write('[Interface]')
				sfile.write(f'Address = {iplist[c]}')
				sfile.write(f'ListenPort = {lport}')
				sfile.write(f'PrivateKey = {server_key[0]}')
				sfile.close()
		else:
			fn = f'client_{c}.conf'
			client_key = skeylist()
			clport = port()
			print(f'Adding peer {c} to server.conf.')
			with open('server.conf','a') as sfile:
				sfile.write('[Peer]')
				sfile.write(f'PublicKey = {client_key[1]}')
				sfile.write(f'AllowIPs = {iplist[c]}/32')
				sfile.close()
			print(f'Writing {fn}.')
			with open(fn,'a') as cfile:
				cfile.write('[Interface]')
				cfile.write('Address = {iplist[c]}/24')
				cfile.write('ListenPort = {clport}')
				cfile.write('PrivateKey = {client_key[0]}')
				cfile.write('MTU = 1420')
				cfile.write('[Peer]')
				cfile.write('PublicKey = {server_key[1]}')
				cfile.write('AllowIPs = {iplist[0]}/32')
				cfile.write('EndPoint = {server_address}:{lport}')
				cfile.close()

