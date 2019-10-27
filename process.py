import os
import sys
import json
import logging

def get_files():
    folder = os.path.join(sys.path[0], 'tracks')
    files = []
    for file in os.listdir(folder):
        with open(os.path.join(os.path.join(folder, file))) as file:
            files.append(
                json.load(file)
            )
    return files

def combine_files(files):
    items = []
    for file in files:
        items.extend(file['items'])
    return items

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Reading track files")
    files = get_files()
    logging.info(f"Read and parse {len(files)} track files")
    logging.info("Combining into single track file for ease of access")
    data = combine_files(files)
    logging.info(f'File combined with {len(data)} items')
main()