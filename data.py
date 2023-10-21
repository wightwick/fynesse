from spotipy import SpotifyOAuth
from dataclasses import dataclass
import reflex as rx

@dataclass(init=False)
class Track():
    uri: str
    name: str
    artist_names: list
    artist_uris: list
    album_name: str
    album_art: list
    spotify_url: str
    artist_genres: list = None

    raw_dict: dict = None

    def get_artist_genres(self, sp: SpotifyOAuth):
        artist_genre_lists = [sp.artist(uri)['genres'] for uri in self.artist_uris]
        self.artist_genres = [item for sublist in artist_genre_lists for item in sublist]
        return self.artist_genres

    def with_artist_genres(self, sp):
        self.get_artist_genres(sp)
        return self
    
    def __init__(self, track_dict, artist_genres=False, sp: SpotifyOAuth = None, keep_dict=False):
        if keep_dict:
            self.raw_dict = track_dict
        self.uri = track_dict['uri']
        self.name = track_dict['name']
        self.artist_names = [a['name'] for a in track_dict['artists']]
        self.artist_uris = [a['uri'] for a in track_dict['artists']]
        self.album_name = track_dict['album']['name']
        self.spotify_url = track_dict['external_urls']['spotify']
        
        if artist_genres:
            self.get_artist_genres(sp)

        self.album_art = track_dict['album']['images']


