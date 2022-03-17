import spotipy
import os
import json
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv('.env')
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')


scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])
#     # print(item)

song = results['items'][0]
# print(json.dumps(song, indent=4))
print(song['track']['href'])

# https://api.spotify.com/v1/tracks/5k6Ahl1QhUYUU9XBmsvNOX
