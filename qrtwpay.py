#!/usr/bin/env python3
# this is a TWpay QRcode image generation program.
# usage qrtwpay.py [bankcode] [accountnumber]
import qrcode
import sys
import string
import secrets
import argparse
# Argparse related.
parser = argparse.ArgumentParser(prog="TWpayGen",description="Generate TWPay compatable QR code to PNG file.")
parser.add_argument("banknumber",type=int,help="Bank indentify number.")
parser.add_argument("accountnumber",type=int,help="Account number to send.")
parser.add_argument("amount",nargs='?',default=0,type=int,help="Amount to send, optional.")
parser.add_argument("description",nargs='?',default="Default",type=str,help="send description, optional.")
args = parser.parse_args()
# code snippet from secrets module
def rstring(n):
	alpha = string.ascii_letters + string.digits
	return ''.join(secret.choice(alpha) for i in range(n))
#check if it is a integer
#def is_integer(n):
#	try:
#		float(n)
#	except ValueError:
#		return False
#	else:
#		return float(n).is_integer()
# main program.
#if len(sys.argv) !=3:
#		print('Error: require 2 arguments.')
#elif ((int(sys.argv[1]) > 826) or (int(sys.argv[1]) < 4) or (len(sys.argv[1]) != 3)):
#		print('Error: Incorrect bank number')
#elif (len(sys.argv[2]) > 16 or not is_integer(sys.argv[2])):
#		print('Error: Incorrect account number')
if args.banknumber > 826 or args.banknumber < 4:
	print("Error: incorrect bank indentify code.")
elif len(str(args.accountnumber)) > 16 or args.accountnumber < 0:
	print("Error: incorrect bank account number.")
elif args.amount < 0:
	print("Error: incorrect amount , no negative.")
else:
	accn = args.accountnumber
	bcn = args.banknumber
	if len(str(accn)) < 16:
		acn = accn.rjust(16,'0')
	else:
		acn = accn
	if args.description == 'Default':
		desc = rstring(8)
	else:
		desc = args.description
	if args.amount == 0:
		qc = f'twqrp://{bcn}NTDTransfer/158/02/V1?D6={acn}&D5={bcn}&D9={desc}&D10=901'
	elif len(str(args.amount)) < 6:
		amt = str(args.amount).rjust(6,'0')
		qc = f'twqrp://{bcn}NTDTransfer/156/02/V1?D6={acn}&D5={bcn}&D1={amt}&D9={desc}&D10=901'
	else:
		amt = str(args.amount)
		qc = f'twqrp://{bcn}NTDTransfer/156/02/V1?D6={acn}&D5={bcn}&D1={amt}&D9={desc}&D10=901'
	qr = qrcode.QRCode(version = 3, error_correction = qrcode.constants.ERROR_CORRECT_H, box_size = 3,border = 4)
	qr.add_data(qc)
	qr.make(fit=True)
	qi = qr.make_image()
	qf = f'{bcn}-{acn}.png'
	qi.save(qf)
	print(f'Saved to {qf}')
