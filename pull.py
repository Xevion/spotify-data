import os
import sys
import auth
import json
import shutil
import pprint
import spotipy
import logging
import spotipy.util as util

def main():
    # Get Authorization
    logging.basicConfig(level=logging.INFO)
    logging.info('Authorizing with Spotify via Spotipy')
    logging.warning('May require User Interaction to authenticate properly!')
    token = util.prompt_for_user_token(
        username=auth.username,
        scope=auth.scope,
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        redirect_uri=auth.redirect_uri
    )
    sp = spotipy.Spotify(auth=token)
    logging.info('Authorized with Spotify via Spotipy')

    tracks_folder = os.path.join(sys.path[0], 'tracks')
    logging.warning('Clearing all files in tracks folder for new files')
    if os.path.exists(tracks_folder):
        shutil.rmtree(tracks_folder) # Delete folder and all contents (old track files)
    os.path.makedirs(tracks_folder) # Recreate the folder just deleted
    logging.info('Cleared folder, ready to download new track files')

    curoffset, curlimit = 0, 50
    while curoffset >= 0:
        logging.info('Requesting tracks {} to {}'.format(curoffset, curoffset + curlimit))
        response = sp.current_user_saved_tracks(limit=curlimit, offset=curoffset)
        received = len(response['items'])
        logging.info('Received tracks {} to {}'.format(curoffset, curoffset + received))
        filename = f'saved-tracks-{curoffset}-{curoffset + received}.json'
        filepath = os.path.join(tracks_folder, filename)
        with open(filepath, 'w+') as file:
            json.dump(response, file)
        logging.info('Saved at "{}" ({}KB)'.format(f'\\tracks\\{filename}', round(os.path.getsize(filepath) / 1024, 2)))
        if received < curlimit:
            logging.info('Done requesting/saving tracks after {} tracks'.format(curoffset + received))
            break
        curoffset += curlimit