import os
import sys
import auth
import json
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

    root = sys.path[0]
    curoffset, curlimit = 0, 50
    # Start grabbing tracks (long running)
    while curoffset >= 0:
        logging.info('Requesting tracks {} to {}'.format(curoffset, curoffset + curlimit))
        response = sp.current_user_saved_tracks(limit=curlimit, offset=curoffset)
        received = len(response['items'])
        logging.info('Received tracks {} to {}'.format(curoffset, curoffset + received))
        filename = f'saved-tracks-{curoffset}-{curoffset + received}.json'
        filepath = os.path.join(root, 'tracks', filename)
        with open(filepath, 'w+') as file:
            json.dump(response, file)
        logging.info('Saved at "{}" ({}KB)'.format(f'\\tracks\\{filename}', round(os.path.getsize(filepath) / 1024, 2)))
        if received < curlimit:
            logging.info('Done requesting/saving tracks after {} tracks.'.format(curoffset + received))
            break
        curoffset += curlimit