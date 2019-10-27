import auth
import json
import pprint
import spotipy
import spotipy.util as util

# Get Authorization
token = util.prompt_for_user_token(
    username=auth.username,
    scope=auth.scope,
    client_id=auth.client_id,
    client_secret=auth.client_secret,
    redirect_uri=auth.redirect_uri
)
sp = spotipy.Spotify(auth=token)
saved_response = sp.current_user_saved_tracks(limit=50, offset=100000)
# saved_response = json.load(open('saved_tracks.json', 'r'))
json.dump(saved_response, open('saved_tracks.json', 'w+'))
pprint.pprint(saved_response)
# for track in saved_response['items']:
#     print('{} by {}'.format(
#         track['track']['name'],
#         ' & '.join(artist['name'] for artist in track['track']['artists'])
#     ))

