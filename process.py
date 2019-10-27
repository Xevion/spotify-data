import json

def main():
    saved_response = json.load(open('saved_tracks.json', 'r'))
    for track in saved_response['items']:
        print('{} by {}'.format(
            track['track']['name'],
            ' & '.join(artist['name'] for artist in track['track']['artists'])
        ))