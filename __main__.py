import time
import sys
import os
import modules.compress as compress
from modules.types import types

try:
    data_folder = sys.argv[1]
    if not os.path.isdir(data_folder):
        raise ValueError("data_folder is not a path")

    file_path = sys.argv[2]
    if not os.path.isfile(file_path):
        raise ValueError("file_path is not a path")

    if len(sys.argv) >= 4:
        item_type = sys.argv[3]
        if not item_type in types:
            raise ValueError("item_type not in type list")
except:
    print("Please specify the text file and what type the items are [python . DATA_FOLDER TEXT_FILE ITEM_TYPE]\n")
    print(f"Available types: {[type for type in types]}")
    sys.exit(1)

with open(file_path, 'r') as file:
    line_count = len(file.readlines())
    file.seek(0)
    #print(line_count)
    line_number = 0
    for line in file:
        line_number += 1

        if line_number % 5 == 0:
            compress.compress(data_folder)

        try:
            item_type, id = line.strip().split(":")
        except ValueError:
            id = line.strip()

        try:
            print(f"Line {str(line_number)}: {id} ({item_type})")
            types[item_type].main(id, data_folder)
        except NameError as e:
            print(f"Error! {e}")
        print("Text Loop: Waiting 3 secs...")
        time.sleep(3)
