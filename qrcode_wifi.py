#!/usr/bin/env python3
"""Generate passphrase and QR code for given SSID.

This tool generates a passphrase for a given SSID. This tool additionally
offers an opportunity to generate a QR code for given SSID, which the user
can share with others.
"""

__author__ = "Kryno Bosman"
__version__ = "1.0"
__date__ = "2022-03-23"


import argparse
import secrets
import qrcode


def generate_passphrase(length):
    """Generate and return a hexadecimal passphrase of given length.

    Input
        length - length of the hexadecimal passphrase.

    Return
        passphrase - a hexadecimal passphrase of given length.
    """
    passphrase = secrets.token_hex(length)

    return passphrase

def generate_qrstring(ssid, protocol, passphrase,  hidden):
    """Generate and return a string for generating a QR code. The QR string
    be like:

        WIFI:S:<SSID>;T:<WEP|WPA|blank>;P:<PASSWORD>;H:<true|false|blank>;;

    Input
        ssid - service set identifier of the wireless network.
        protocol - used security protocol.
        passphrase - used hexadecimal passphrase.
        hidden - whether the network is hidden or not.

    Return
        qrstring - string for generate QR code for given wireless network.
    """
    qrstring = "WIFI:S:{0};T:{1};P:{2};H:{3};;".format(
        ssid,
        protocol,
        passphrase,
        hidden)

    return qrstring


def generate_qrcode(name, qrstring):
    """Generate a QR code with given string qrstring.

    Input
        name - name of the PNG file.
        qrstring - string containing ssid, protocol, passphrase, hidden.

    Result
        qrcode - a generated QR code in PNG format.
    """
    img = qrcode.make(qrstring)
    img.save(name + ".png")


def main():
    """Main logic of the program which deals with arguments and options
    provided by the user."""
    parser = argparse.ArgumentParser()

    parser.add_argument('ssid',
        metavar = 'NAME',
        help = 'the service set identifier, the name of the wireless network.')
    parser.add_argument('-p', '--protocol',
        metavar = 'PROTO',
        default = 'WPA',
        help = 'used security protocol like WEP, WPA, et cetera (default: %(default)s)')
    parser.add_argument('-P', '--passphrase',
        metavar = 'PASS',
        help = 'the passphrase of the wireless network.')
    parser.add_argument('-l', '--length',
        metavar = 'N',
        type = int,
        default = 16,
        help = 'the lenght of the password (default: %(default)s)')
    parser.add_argument('--hidden',
        action = 'store_true',
        help = 'whether the wireless network is hidden or not (default: false)')

    args = parser.parse_args()

    # print(args)

    if not args.passphrase:
        passphrase = generate_passphrase(args.length)
    else:
        passphrase = args.passphrase

    if args.hidden:
        hidden = "true"
    else:
        hidden = "false"

    qr_string = generate_qrstring(args.ssid, args.protocol, passphrase, hidden)

    generate_qrcode(args.ssid, qr_string)

    print("SSID         : {0}".format(args.ssid))
    print("Passphrase   : {0}".format(passphrase))
    print("QR Code      : {0}".format(qr_string))
    print("QR Code file : {0}.png".format(args.ssid))


if __name__ == "__main__":
    main()
