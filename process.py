import os
import sys
import json
import logging
import collections
import numpy as np
import dateutil.parser
import PIL.Image as Image
import matplotlib.pyplot as plt

# Gets all files in tracks folder, returns them in parsed JSON
def get_files():
    folder = os.path.join(sys.path[0], 'tracks')
    files = []
    print(os.listdir(folder))
    for file in os.listdir(folder):
        with open(os.path.join(os.path.join(folder, file))) as file:
            files.append(
                json.load(file)
            )
    return files

# Simple function to combine a bunch of items from different files
def combine_files(files):
    items = []
    for file in files:
        items.extend(file['items'])
    return items

# Prints the data in a interesting format
def print_data(data):
    for i, item in enumerate(data):
        date = dateutil.parser.parse(item['added_at'])
        explicit = '!' if item['track']['explicit'] else ' '
        track_name = item['track']['name']
        artists = ' & '.join(artist['name'] for artist in item['track']['artists'])
        print('[{}] {} "{}" by {}'.format(date, explicit, track_name, artists))

def process_data(data):
    # Process the data by Month/Year, then by Safe/Explicit
    scores = {}
    for item in data:
        date = dateutil.parser.parse(item['added_at']).strftime('%b %Y')
        if date not in scores.keys():
            scores[date] = [0, 0]
        scores[date][1 if item['track']['explicit'] else 0] += 1
    
    # Create simplified arrays for each piece of data
    months = list(scores.keys())[::-1]
    safe, explicit = [], []
    for item in list(scores.values())[::-1]:
        safe.append(item[0])
        explicit.append(item[1])

    # Done processing date properly, start plotting work
    n = len(scores.values())
    ind = np.arange(n)
    width = 0.55

    p1 = plt.bar(ind, explicit, width)
    p2 = plt.bar(ind, safe, width, bottom=explicit) # bottom= just has the bar sit on top of the explicit

    plt.title('Song by Safe/Explicit')
    plt.ylabel('Song Count')
    plt.xlabel('Month')
    plt.xticks(ind, months, rotation=270) # Rotation 90 will have the 
    plt.legend((p1[0], p2[0]), ('Explicit', 'Safe'))
    # plt.show()
    copy(months, safe, explicit)

# Simple method for exporting data to a table like format
# Will paste into Excel very easily
def copy(months, safe, explicit):
    from pyperclip import copy
    top = 'period\tsafe\texplicit\n'
    copy(top + '\n'.join([
        f'{item[0]}\t{item[1]}\t{item[2]}' for item in zip(months, safe, explicit)
    ]))

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Reading track files")
    files = get_files()
    logging.info(f"Read and parse {len(files)} track files")
    logging.info("Combining into single track file for ease of access")
    data = combine_files(files)
    data.sort(key=lambda item : dateutil.parser.parse(item['added_at']).timestamp(), reverse=True)
    logging.info(f'File combined with {len(data)} items')
    logging.info('Processing file...')
    process_data(data)

main()