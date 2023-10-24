# state.py
import reflex as rx
from spotipy import Spotify, SpotifyOAuth
from spotify_secrets import *
from .data import Track

scopes = [
    # 'ugc-image-upload',
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing',
    'app-remote-control',
    'streaming',
    'playlist-read-private',
    'playlist-read-collaborative',
    'playlist-modify-private',
    'playlist-modify-public',
    # 'user-follow-modify',
    # 'user-follow-read',
    'user-read-playback-position',
    'user-top-read',
    'user-read-recently-played',
    'user-library-modify',
    'user-library-read',
    # 'user-read-email',
    # 'user-read-private',
]

class State(rx.State):
    """The app state."""

    tracks: dict[str, list[Track]] = {'recent': [],}
    rp_tracks_have_genre: bool = False
    _sp = Spotify(
        auth_manager=SpotifyOAuth(
            scope=scopes,
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            open_browser=True
        )
    )

    selected_track_uris_with_source: list[tuple[str, str]]
    selected_genres: list[str]

    def add_uri(self, uri: str, source: str):
        if uri not in self.selected_track_uris_with_source:
            self.selected_track_uris_with_source = [*self.selected_track_uris_with_source, (uri, source)]

    def remove_uri(self, uri: str):
        self.selected_track_uris_with_source = [
            (u, s)
            for u, s
            in self.selected_track_uris_with_source
            if u != uri
        ]

    def add_genre(self, genre: str):
        if genre not in self.selected_genres:
            self.selected_genres = [*self.selected_genres, genre]

    def remove_genre(self, genre: str):
        self.selected_genres = [
            g for g in self.selected_genres
            if g != genre
        ]

    def fetch_rp_tracks(self):
        raw_rp_tracks = self._sp.current_user_recently_played(limit=50)['items']
        self.tracks['recent'] = [Track(item) for item in raw_rp_tracks]
        self.rp_tracks_have_genre = False

    def fetch_genres_rp(self):
        self.tracks['recent'] = [
            track.with_artist_genres(self._sp) for track
            in self.tracks['recent']
        ]
        self.rp_tracks_have_genre = True

    @rx.var
    def selected_tracks(self) -> list[Track]:
        all_tracks_flattened = [item for sublist in self.tracks.values() for item in sublist]
        return [
            [t.without_artist_genres() for t in all_tracks_flattened if t.uri == u][0]
            for u in self.selected_track_uris
        ]

    @rx.var
    def selected_track_uris(self) -> list[str]:
        return [uri for uri, source in self.selected_track_uris_with_source]

    @rx.var
    def rp_tracks(self) -> list[Track]:
        return self.tracks['recent']