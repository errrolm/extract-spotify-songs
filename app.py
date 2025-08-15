import csv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Config:
SPOTIFY_CLIENT_ID = "your-client-id"
SPOTIFY_CLIENT_SECRET = "your-client-secret"

# To get your client id and secret create an app on spotify's developer portal and choose the web api/sdk and put the redirect URI as given below

SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"

OUTPUT_FILE = "spotify_liked_songs.csv"


def get_spotify_liked_songs():
    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="user-library-read"
    ))

    liked_songs = []
    results = sp.current_user_saved_tracks(limit=50)

    while results:
        for item in results['items']:
            track = item['track']
            liked_songs.append({
                "title": track['name'],
                "artist": ", ".join([a['name'] for a in track['artists']]),
                "album": track['album']['name'],
                "spotify_url": track['external_urls']['spotify']
            })
        if results['next']:
            results = sp.next(results)
        else:
            break

    return liked_songs

def save_songs_to_csv(songs, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "artist", "album", "spotify_url"])
        writer.writeheader()
        for song in songs:
            writer.writerow(song)
    print(f"Saved {len(songs)} songs to {filename}")

if __name__ == "__main__":
    songs = get_spotify_liked_songs()
    save_songs_to_csv(songs, OUTPUT_FILE)
