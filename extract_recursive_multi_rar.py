#!/usr/bin/python3

# This Python script recursively finds all *.part1.rar files under the current directory
# and extracts them to the folder where they reside.
# If extraction was successful, it deletes all rar parts.

# Requirements:
# 1. Run with Python3
# 2. sudo apt install python3-pip
# 3. sudo pip3 install unrar
# 4. unrar_tgz_url=http://www.rarlab.com/rar/unrarsrc-5.9.4.tar.gz && wget $unrar_tgz_url && tar xvzf $unrar_tgz_url && cd unrar && make lib && sudo make install-lib
# 4.a. Latest unrar source version is in  https://www.rarlab.com/rar_add.htm under "UnRAR source"
# 5. Add "export UNRAR_LIB_PATH=/usr/lib/libunrar.so" to "/etc/profile"

import re
from pathlib import Path
import sys
import os
from unrar import rarfile
from unrar import unrarlib
import argparse


def purge(dir, pattern):
    for f in os.listdir(dir):
        if re.search(pattern, f):
            print("deleting: ", os.path.join(dir, f))
            os.remove(os.path.join(dir, f))

parser = argparse.ArgumentParser(description='Recursively extract multi rar files')
parser.add_argument('-pw', action='append', help='rar password')
args = parser.parse_args()

print('Password list: ' + str(args.pw))

if args.pw is not None:
    args.pw.insert(0, '')
else:
    args.pw = ['']

pathlist = Path(".").glob('**/*.part*1.rar')
for path in pathlist:

    if path.is_file() == False:
        continue

    # example: path = dir1/dir2/fileA.part1.rar

    # example: file_part1_name = fileA.part1.rar
    file_part1_name = path.name
    # example: parent_path = dir1/dir2
    parent_path = path.parent

    matchObj = re.match( r'(.*).part0*1.rar', file_part1_name, re.M|re.I)
    if not matchObj:
        #print("Failed to find match for: ", file_part1_name)
        continue

    # example: file_base = fileA
    file_base = matchObj.group(1)

    is_extracted = bool(False)
    error_msg = ''

    # loop that tries all passwords we have until we succeed extracting
    for pw in args.pw:
        try:
            with rarfile.RarFile(filename=str(path), pwd=pw) as rar:
                if not pw:
                    print('Extracting: ' + str(path))
                else:
                    print('Extracting: ' + str(path) + ' with password: ' + pw)

                rar.extractall(path=str(parent_path))
                is_extracted = bool(True)
        except rarfile.BadRarFile as e:
            error_msg = 'Got rarfile.BadRarFile exception, message: ' + str(e)
            break
        except unrarlib.UnrarException as e:
            error_msg = 'Got unrarlib.UnrarException exception, message: ' + str(e)
            break
        except RuntimeError as e:
            # Invalid password will lead here so we're retrying
            error_msg = str(e)
            continue

        # if we succeeded to extract, break out of the password trials loop
        if is_extracted:
            break

    if is_extracted:
        print('Successfully extracted ' + str(path))
        purge(str(parent_path), re.escape(file_base) + '.part[0-9]*.rar')
    else:
        print('Failed to extract ' + str(path) + ', error: ' + error_msg)
