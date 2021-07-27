#!/usr/bin/env python3
# this is a TWpay QRcode image generation program.
# usage qrtwpay.py [bankcode] [accountnumber]
import qrcode
import sys
import string
import secrets
# code snippet from secrets module
def rstring(n):
	alpha = string.ascii_letters + string.digits
	return ''.join(secret.choice(alpha) for i in range(n))
# check if it is a integer
def is_integer(n):
	try:
		float(n)
	except ValueError:
		return False
	else:
		return float(n).is_integer()
# main program.
if len(sys.argv) !=3:
		print('Error: require 2 arguments.')
elif ((int(sys.argv[1]) > 826) or (int(sys.argv[1]) < 4) or (len(sys.argv[1]) != 3)):
		print('Error: Incorrect bank number')
elif (len(sys.argv[2]) > 16 or not is_integer(sys.argv[2])):
		print('Error: Incorrect account number')
else:
	if len(sys.argv[2]) < 16:
		acn = sys.argv[2].rjust(16,'0')
	else:
		acn = sys.argv[2]

	desc = rstring(8)
	bcn = sys.argv[1]
	qc = f'twqrp://{bcn}NTDTransfer/158/02/V1?D6={acn}&D5={bcn}&D9={desc}&D10=901'
	qr = qrcode.QRCode(version = 3, error_correction = qrcode.constants.ERROR_CORRECT_H, box_size = 3,border = 4)
	qr.add_data(qc)
	qr.make(fit=True)
	qi = qr.make_image()
	qf = f'{bcn}-{acn}.png'
	qi.save(qf)
	print(f'Saved to {qf}')
