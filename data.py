from spotipy import SpotifyOAuth
from dataclasses import dataclass
import reflex as rx

class Track(rx.Base):
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
    
    def __init__(
            self,
            track_dict,
            keep_dict=False
        ):
        uri = track_dict['uri']
        name = track_dict['name']
        artist_names = [a['name'] for a in track_dict['artists']]
        artist_uris = [a['uri'] for a in track_dict['artists']]
        album_name = track_dict['album']['name']
        spotify_url = track_dict['external_urls']['spotify']
        
        album_art = track_dict['album']['images']

        super().__init__(
            uri=uri,
            name=name,
            artist_names=artist_names,
            artist_uris=artist_uris,
            album_name=album_name,
            album_art=album_art,
            spotify_url=spotify_url,
        )
