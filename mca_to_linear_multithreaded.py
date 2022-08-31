#!/usr/bin/python3

import sys
import os
import os.path
from glob import glob
from linear import Chunk, Region, write_region_linear, open_region_anvil
from multiprocessing import Pool

if len(sys.argv) != 5:
    print("Usage: threads compression_level source_dir destination_dir")
    exit(0)

threads = int(sys.argv[1])
compression_level = int(sys.argv[2])
source_dir = sys.argv[3]
destination_dir = sys.argv[4]

#for source_file in glob(os.path.join(source_dir, "*.mca")):
def convert_file(source_file):
    os.makedirs(destination_dir, exist_ok=True)
    
    source_filename = os.path.basename(source_file)
    destination_file = os.path.join(destination_dir, source_filename).rpartition(".")[0] + ".linear"

    convert_to_linear = False
    try:
        mtime_destination = os.path.getmtime(destination_file)
        mtime_source = os.path.getmtime(source_file)
        if mtime_destination != mtime_source:
            convert_to_linear = True
    except FileNotFoundError:
        convert_to_linear = True

    if convert_to_linear == False:
        print(source_filename, "already converted, skipping")
        return

    region = open_region_anvil(source_file)
    write_region_linear(destination_file, region, compression_level=compression_level)

    source_size = os.path.getsize(source_file)
    destination_size = os.path.getsize(destination_file)

    print(source_file, "converted, compression %3d%%" % (100 * destination_size / source_size))

file_list = glob(os.path.join(source_dir, "*.mca"))
print("Found", len(file_list), "files to convert", len(file_list))

pool = Pool(threads)
pool.map(convert_file, file_list)
