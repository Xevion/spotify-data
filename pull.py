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
    logging.info('Authorizing with Spotify (may require User interaction).')
    token = util.prompt_for_user_token(
        username=auth.username,
        scope=auth.scope,
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        redirect_uri=auth.redirect_uri
    )
    sp = spotipy.Spotify(auth=token)
    logging.info('Authorized with Spotify.')

    root = sys.path[0]
    curoffset, curlimit = 900, 50
    # Start grabbing tracks (long running)
    while curoffset >= 0:
        logging.debug('Requesting tracks {} to {}'.format(curoffset, curoffset + curlimit.))
        response = sp.current_user_saved_tracks(limit=curlimit, offset=curoffset)
        received = len(response['items'])
        logging.debug('Received tracks {} to {}'.format(curoffset, curoffset + received))
        filename = f'saved-tracks-{curoffset}-{curoffset + received}.json'
        filepath = os.path.join(root, 'tracks', filename)
        with open(filepath, 'w+') as file:
            json.dump(response, file)
        curoffset += curlimit
        logging.debug('Saved at "{}" ({}KB)'.format(f'\\tracks\\{filename}', round(os.path.getsize(filepath) / 1024, 2)))
        if received < curlimit:
            logging.info('Done requesting/saving tracks after {} tracks.'.format())

main()