import os
import sys
import json
import logging
import collections
import numpy as np
import dateutil.parser
import matplotlib.pyplot as plt

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

def print_data(data):
    for i, item in enumerate(data):
        date = dateutil.parser.parse(item['added_at'])
        explicit = '!' if item['track']['explicit'] else ' '
        track_name = item['track']['name']
        artists = ' & '.join(artist['name'] for artist in item['track']['artists'])
        print('[{}] {} "{}" by {}'.format(date, explicit, track_name, artists))

def process_data(data):
    explicit = collections.defaultdict(int)
    safe = collections.defaultdict(int)
    for item in data:
        date = dateutil.parser.parse(item['added_at'])
        date = date.strftime('%b %Y')
        if item['track']['explicit']:
            explicit[date] += 1
        else:
            safe[date] += 1
    times = [dateutil.parser.parse(item['added_at']) for item in data]
    sort_func = lambda x : dateutil.parser.parse(x[0]).epoch
    

    n = len(data)
    ind = np.arange(n)
    width = 0.35
    plt.ylabel('Month')
    plt.xlabel('Song by Type')
    plt.xticks(ind, )
    # plt.show()

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Reading track files")
    files = get_files()
    logging.info(f"Read and parse {len(files)} track files")
    logging.info("Combining into single track file for ease of access")
    data = combine_files(files)
    logging.info(f'File combined with {len(data)} items')
    logging.info('Processing file...')
    process_data(data)
main()