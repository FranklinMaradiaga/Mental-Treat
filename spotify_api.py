import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

APP_CLIENT_ID = '0f476500fd7d4df98e568d18225b7287'
APP_CLIENT_SECRET = '78cece290a0f4925b90b9ad13554c9aa'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=APP_CLIENT_ID,
                                                           client_secret=APP_CLIENT_SECRET))

results = sp.search(q='weezer', limit=20)

for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])

url = requests.get('https://api.spotify.com/v1/audio-features/11dFghVXANMlKmJXsNCbNI')
print(url)

