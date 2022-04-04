#!/usr/bin/env python3
"""Capture minicom output.

A wrapper for the tool minicom to capture the output just a little more
specific.

The capture file will be store in the following format.

~ -+- general   -+- host1
   |             +- host9
   |
   +- projectXY -+- host11
                 +- host19
"""

__author__ = "Kryno Bosman"
__version__ = "1.0"
__date__ = "2022-03-29"


import os
import os.path
import subprocess
import argparse
import datetime


def main():
    """Main logic."""
    parser = argparse.ArgumentParser()
    parser.add_argument('name',
        help = 'machine name')
    parser.add_argument('-p', '--product',
        default = 'general',
        help = 'product or platform')
    parser.add_argument('-D', '--device',
        default = '/dev/ttyUSB0',
        help = 'set device name')
    parser.add_argument('-b', '--baudrate',
        default = '115200',
        help = 'set baudrate')
    args = parser.parse_args()

    # Date and time.
    date = datetime.date.today().strftime("%Y-%m-%d")
    time = datetime.datetime.now().strftime("%H:%M:%S")

    # Define a capture file in the user's home directory.
    home_directory = os.path.expanduser("~")
    filename = args.name + "_" +  date + "_" + time + ".capture"
    console_directory = os.path.join(home_directory, args.product)
    capture_file = os.path.join(console_directory, filename)

    # Create environment if not exist.
    if not os.path.exists(console_directory):
        os.mkdir(console_directory)
    else:
        print(f"Directory {console_directory} exists.")


    # Add capture file to environment.
    cmnd = f"minicom -D {args.device} -b {args.baudrate} -C {capture_file} {args.name}"

    try:
        subprocess.run(cmnd.split(), check = True)
    except subprocess.CalledProcessError as err:
        print(f"Whoops! {err}")


if __name__ == "__main__":
    main()
