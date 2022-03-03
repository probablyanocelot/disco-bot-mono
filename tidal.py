# pipenv install -e git+https://github.com/tamland/python-tidal.git@0.7.x#egg=tidalapi
import tidalapi
import os

# 0.7.x
session = tidalapi.Session()
# Will run until you visit the printed url and link your account

session_id = session.session_id
token_type = session.token_type
access_token = session.access_token
refresh_token = session.refresh_token


async def login():
    try:
        session.load_oauth_session(
            session_id, token_type, access_token, refresh_token)
        print('we made it!')
    except tidalapi.TidalError as e:
        session.login_oauth_simple()

    # playlist = session.playlist('4261748a-4287-4758-aaab-6d5be3e99e52')
    # session.login('username', 'password') # for 0.6.x
    # tracks = session.get_album_tracks(album_id=16909093)
    # for track in tracks:
    # print(track.name)


def get_playlist(playlist_id):
    playlist = session.playlist(playlist_id)
    return playlist


def get_tracks(playlist):
    tracks = playlist.tracks()
    for track in tracks:
        print(track.name)
    # print(tracks)
    print(tracks[0].get_url())


# get_tracks(playlist)

'''http://ab-pr-cf.audio.tidal.com/4cacf116a17313d6496d33e67a40342f_37.mp4 /
?Expires=1642245527&Signature=UC~bJ2lKQmFqbn8K~uR29e9v9MAO51RCfqquvNQAjC /
~sgOBSN325u8APTvunMZizGLNYtH0HFsOzAn-bKhJfutTPsRBrgYdSYt8kGGABEMqV-qmzADrF /
~eWYkTxMCJhfa9ryZLxWMYPHCyYxn6Ok7Ura5ZT-KfuoegDT3~6OShNyR7GIAMC3MgbfB5iOK~ /
jErdP9rGduvUjAVb-h0xc0FJEGknGa3HUEtndzhvqH72lecwIPO12KM6j~wiS3N61 /
~VuPQ2zy9rFL8299o09995kiCZBDW3OLGYC3LwxmcCPZp9fabEBvNWnf2V4u0JwtfvQR0cf0uZ9XUqBTim2sPIw__ /
&Key-Pair-Id=APKAIZ3WPBE4R6SP555A'''
