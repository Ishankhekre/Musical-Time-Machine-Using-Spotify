from pprint import pprint

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "f582fa1597cf406ca4f15fb2f0f43a83"
CLIENT_SECRET = "97faf2f79ee9434abd56d05e3840126e"
REDIRECT_URI = "http://example.com"
USER_ID = "312ccy5exs3mkzwnw56tec3ik6b4"

abc = "https://www.billboard.com/charts/hot-100/"
date = input("Which year do you want to travel to ? Type the Date in this format YYYY-MM-DD ")
URL = abc+date

response = requests.get(url=URL)
data = response.text

soup = BeautifulSoup(data, "html.parser")
abcd = soup.select("li ul li h3")
name_of_songs = []
for ab in abcd:
    text = ab.get_text().strip()
    name_of_songs.append(text)

pprint(name_of_songs)


#sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
#access_token = sp_oauth.get_access_token()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path=".cache"
    )
)

song_URIs = []
year = date.split("-")[0]
playlist = sp.user_playlist_create(user=USER_ID, name=f"{date} Billboard ", public=False)

for song in name_of_songs:
    result = sp.search(q=f"track:{song} year:{year}",type="track",)
    #pprint(result)
    try:
        uri= result["tracks"]["items"][0]["uri"]
        song_URIs.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

pprint(song_URIs)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_URIs)