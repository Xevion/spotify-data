import os
import sys
import auth
import json
import pprint
import spotipy
import spotipy.util as util

def main():
    # Get Authorization
    print('Authorizing with Spotify')
    token = util.prompt_for_user_token(
        username=auth.username,
        scope=auth.scope,
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        redirect_uri=auth.redirect_uri
    )
    sp = spotipy.Spotify(auth=token)
    print('Authorized')

    curoffset, curlimit = 0, 50
    # Start grabbing tracks (long running)
    while True:
        response = sp.current_user_saved_tracks(limit=curlimit, offset=curoffset)
        if response is not None:
            print('Received ')
            filename = f'saved-tracks-{curoffset}-{curoffset + curlimit}.json'
            filepath = os.path.join(root, 'tracks', filename)
            with open(filepath, 'w+') as file:
                json.dump(response, file)
                curoffset += curlimit
