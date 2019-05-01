#!/usr/bin/python3

# This Python script recursively finds all *.part1.rar files under the current directory
# and extracts them to the folder where they reside.
# If extraction was successful, it deletes all rar parts.

# Requirements:
# 1. Run with Python3
# 2. Install unrar and python-unrar. See https://pypi.org/project/unrar/

import re
from pathlib import Path
import sys
import os
from unrar import rarfile

def purge(dir, pattern):
    for f in os.listdir(dir):
        if re.search(pattern, f):
            print("deleting: ", os.path.join(dir, f))
            os.remove(os.path.join(dir, f))


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
    
    try:
        print("extracting: ", str(path))
        rar = rarfile.RarFile(str(path))
        rar.extractall(str(parent_path))
    except rarfile.BadRarFile:
        print("Failed to extract: ", path)
        continue
    
    purge(str(parent_path), file_base + '.part[0-9]*.rar')