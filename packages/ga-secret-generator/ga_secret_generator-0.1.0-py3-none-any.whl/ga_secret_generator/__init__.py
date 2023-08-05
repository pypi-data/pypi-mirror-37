#!/usr/bin/env python3

"""generate google authenticator totp secret"""

import argparse
import base64
import os
import binascii
import pyqrcode

def qrcode(keyname, secret):
    """generate qrcode"""
    return pyqrcode.create('otpauth://totp/{}?secret={}'.format(keyname, secret))

def generate_secret(length=30):
    """generate secret"""
    return base64.b32encode(base64.b16decode(
        binascii.b2a_hex(os.urandom(length)).upper())).decode()

def main():
    """parse cli args, generate and output totp secret"""
    cli = argparse.ArgumentParser(
        description='''generates google authenticator totp secret as text and
                       optionally as QR code''',
    )
    cli.add_argument(dest="keyname",
                     help="keyname, as displayed in google authenticator")
    cli.add_argument('-n', '--no-qr', action='store_true',
                     help="omit generating a QR code image")
    cli.add_argument('-o', '--output-file', default='qr-code.png',
                     help='''where to store the QR code image
                             (default: %(default)s)''')
    cli.add_argument('-s', '--secret',
                     help="use existing secret instead of generating one")
    args = cli.parse_args()

    if args.secret:
        totp_secret = args.secret
    else:
        totp_secret = generate_secret()

    if not args.no_qr:
        qrcode(args.keyname, totp_secret).png(args.output_file, scale=8)
    print(totp_secret)


if __name__ == '__main__':
    main()
