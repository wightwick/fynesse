from spotipy import SpotifyOAuth
from datetime import datetime
import reflex as rx

class Track(rx.Base):
    uri: str
    track_name: str
    artist_names: list
    artist_uris: list
    album_name: str
    album_art: list[str]
    spotify_url: str
    artist_genres: list[str] = []
    album_art_srcset: str
    added_at: str

    raw_dict: dict = None

    def get_artist_genres(self, sp: SpotifyOAuth):
        artist_genre_lists = [sp.artist(uri)['genres'] for uri in self.artist_uris]
        self.artist_genres = [item for sublist in artist_genre_lists for item in sublist]
        return self.artist_genres

    def with_artist_genres(self, sp):
        self.get_artist_genres(sp)
        return self
    
    def without_artist_genres(self):
        self.artist_genres = []
        return self
    
    def __init__(
            self,
            item_dict,
            keep_dict=False
        ):
        track_dict = item_dict['track']
        uri = track_dict['uri']
        track_name = track_dict['name']
        artist_names = [a['name'] for a in track_dict['artists']]
        artist_uris = [a['uri'] for a in track_dict['artists']]
        album_name = track_dict['album']['name']
        spotify_url = track_dict['external_urls']['spotify']
        
        raw_album_art = track_dict['album']['images']

        album_art = [img['url'] for img in raw_album_art]

        album_art_srcset = ', '.join([
            f"{img['url']} {img['width']}w"
            for img in raw_album_art
        ])
        
        added_at_str = item_dict['added_at'] if 'added_at' in item_dict else item_dict['played_at']
        if added_at_str:
            added_at = added_at_str #datetime.fromisoformat(added_at_str)
        
        super().__init__(
            uri=uri,
            track_name=track_name,
            artist_names=artist_names,
            artist_uris=artist_uris,
            album_name=album_name,
            album_art=album_art,
            album_art_srcset=album_art_srcset,
            spotify_url=spotify_url,
            added_at=added_at
        )



