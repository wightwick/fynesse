import reflex as rx
from spotipy import Spotify, SpotifyOAuth
from spotify_secrets import *
from .data import Track, Playlist
from .utilities import *
from icecream import ic

scopes = [
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing',
    'app-remote-control',
    'streaming',
    'playlist-read-private',
    'playlist-read-collaborative',
    'playlist-modify-private',
    'playlist-modify-public',
    'user-read-playback-position',
    'user-top-read',
    'user-read-recently-played',
    'user-library-modify',
    'user-library-read',
]

class State(rx.State):
    """The app state."""
    
    _sp = Spotify(
        auth_manager=SpotifyOAuth(
            scope=scopes,
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            open_browser=True
        )
    )

    lib_tracks: dict[str, list[Track]] = {'____recent': [], '____liked': [], '': []}
    recc_tracks: list[Track] = []
    playlists: list[Playlist]
    rp_tracks_have_genre: bool = False
    liked_tracks_have_genre: bool = False

    seed_track_uris_with_source: list[tuple[str, str]]
    seed_genres: list[str]
    search_genre: str = ''
    seed_artists: list[tuple[str, str]]
    selected_playlist: Playlist = Playlist()
    _genre_lookup: dict[str, str] = dict()

    ### RECOMMENDATION PARAMETERS
    recc_target_acousticness_value: float = 0
    recc_target_acousticness_enabled: bool = False
    def enable_disable_recc_target_acousticness(self, enabled: bool):
        self.recc_target_acousticness_enabled = enabled
    def set_recc_target_acousticness_value(self, value: int):
        self.recc_target_acousticness_value = value / 100

    recc_target_energy_value: float = 0
    recc_target_energy_enabled: bool = False
    def enable_disable_recc_target_energy(self, enabled: bool):
        self.recc_target_energy_enabled = enabled
    def set_recc_target_energy_value(self, value: int):
        self.recc_target_energy_value = value / 100

    recc_target_liveness_value: float = 0
    recc_target_liveness_enabled: bool = False
    def enable_disable_recc_target_liveness(self, enabled: bool):
        self.recc_target_liveness_enabled = enabled
    def set_recc_target_liveness_value(self, value: int):
        self.recc_target_liveness_value = value / 100

    recc_target_danceability_value: float = 0
    recc_target_danceability_enabled: bool = False
    def enable_disable_recc_target_danceability(self, enabled: bool):
        self.recc_target_danceability_enabled = enabled
    def set_recc_target_danceability_value(self, value: int):
        self.recc_target_danceability_value = value / 100

    recc_target_instrumentalness_value: float = 0
    recc_target_instrumentalness_enabled: bool = False
    def enable_disable_recc_target_instrumentalness(self, enabled: bool):
        self.recc_target_instrumentalness_enabled = enabled
    def set_recc_target_instrumentalness_value(self, value: int):
        self.recc_target_instrumentalness_value = value / 100

    
    #### LIBRARY FROM API
    def fetch_rp_tracks(self):
        raw_rp_tracks = self._sp.current_user_recently_played(limit=50)['items']
        self.lib_tracks['____recent'] = [
            Track(item)
            for item
            in raw_rp_tracks
        ]
        self.rp_tracks_have_genre = False

    def fetch_liked_tracks_batch(self):
        raw_liked_tracks = self._sp.current_user_saved_tracks(
            limit=50,
            offset=len(self.lib_tracks['____liked'])
        )['items']
        self.lib_tracks['____liked'] = [
            *self.lib_tracks['____liked'],
            *[Track(item) for item in raw_liked_tracks]
        ]
        self.liked_tracks_have_genre = False

    def _update_genre_dict_from_artist_uris(
        self,
        a_uris: list[str],
        existing_genre_lookup: dict[str, str], 
    ):
        artists = []
        chunk_size = 50
        a_uris_subset = list(
            set(a_uris)
                .difference(
                    set(existing_genre_lookup.keys())
                )
        )

        for i in range(0, len(a_uris_subset), chunk_size):
            print('Fetching batch of artist genres')
            chunk = a_uris_subset[i:i + chunk_size] 
            output_chunk = self._sp.artists(chunk)
            artists.extend(output_chunk['artists'])

        genre_lookup_lists = [
            {a['uri']:a['genres']} for a in
            artists
        ]
        genre_lookup = {
            k: v
            for d
            in genre_lookup_lists
            for k, v
            in d.items()
        }
        genre_lookup.update(existing_genre_lookup)

        return genre_lookup


    def _fetch_genres_for_track_list(
            self,
            track_list: list[Track]
        ) -> list[Track]:
        artist_uris = flatten_list_of_lists(
            [
                t.artist_uris
                for t in track_list
            ]
        )
        self._genre_lookup = self._update_genre_dict_from_artist_uris(
            artist_uris,
            self._genre_lookup,
        )

        return [
            track.with_artist_genres(
                flat_genre_list_for_artist_uris(
                    track.artist_uris,
                    self._genre_lookup
                )
            )
            for track
            in track_list
        ]


    def _add_genres_to_lib_track_list(self, list_name: str):
        self.lib_tracks[list_name] = self._fetch_genres_for_track_list(
            self.lib_tracks[list_name]
        )

    def fetch_genres_rp(self):
        self._add_genres_to_lib_track_list('____recent')
        self.rp_tracks_have_genre = True

    def fetch_genres_liked(self):
        self._add_genres_to_lib_track_list('____liked')
        self.liked_tracks_have_genre = True

    def fetch_genres_selected_pl(self):
        self._add_genres_to_lib_track_list(self.selected_playlist.playlist_name)
        self.selected_playlist = self.selected_playlist.with_genre_flag_true()
        self.playlists = [
            pl if pl.playlist_name != self.selected_playlist.playlist_name else pl.with_genre_flag_true()
            for pl
            in self.playlists
        ]

    def fetch_playlists(self):
        print("Fetching playlist info")

        pl_results = self._sp.current_user_playlists()
        pl_items = pl_results['items']
        while pl_results['next']:
            pl_results = self._sp.next(pl_results)
            pl_items.extend(pl_results['items'])

        self.playlists = [Playlist(pl_dict) for pl_dict in pl_items]

        # ensure uniqueness of names
        playlist_counts = {}
        for playlist in self.playlists:
            name = playlist.playlist_name
            if name in playlist_counts:
                playlist_counts[name] += 1
                playlist.playlist_name = f"{name} ({playlist_counts[name]})"
            else:
                playlist_counts[name] = 1        

    def fetch_tracks_for_playlist(self, playlist: Playlist):
        print("Fetching playlist tracks for PL", playlist.playlist_name)

        pl_results = self._sp.playlist_items(playlist.uri)
        playlist_tracks = pl_results['items']
        while pl_results['next']:
            pl_results = self._sp.next(pl_results)
            playlist_tracks.extend(pl_results['items'])
        
        self.lib_tracks[playlist.playlist_name] = [
            Track(item)
            for item in playlist_tracks
            if item['track']
            and 'spotify:local' not in item['track']['uri']
        ]

    def on_load_library_fetch(self):
        self.fetch_rp_tracks()
        self.fetch_liked_tracks_batch()
        self.fetch_playlists()
        self.selected_playlist = self.playlists[0]
        self.fetch_tracks_for_playlist(self.selected_playlist)


    ### RECOMMENDATIONS FROM API
    def fetch_recommendations(
            self,
            limit = 20
        ):
        print(f'Fetching {limit} recommended tracks')
        
        generation_params_dict = {
            'seed_artists': self.seed_artist_uris,
            'seed_tracks': self.seed_track_uris,
            'limit': 20,
            'target_acousticness': self.recc_target_acousticness_value \
                if self.recc_target_acousticness_enabled else None,
            'target_energy': self.recc_target_energy_value \
                if self.recc_target_energy_enabled else None,
            'target_liveness': self.recc_target_liveness_value \
                if self.recc_target_liveness_enabled else None,
            'target_danceability': self.recc_target_danceability_value \
                if self.recc_target_danceability_enabled else None,
            'target_instrumentalness': self.recc_target_instrumentalness_value \
                if self.recc_target_instrumentalness_enabled else None,

        }
        
        ic(
            generation_params_dict
        )
        raw_recc_tracks = self._sp.recommendations(
            **generation_params_dict
        )
        recc_tracks_without_genre = [
            Track(track, track_enclosed_in_item=False)
            for track
            in raw_recc_tracks['tracks']
        ]

        self.recc_tracks = self._fetch_genres_for_track_list(
            recc_tracks_without_genre
        )

    ### PLAYBACK STATE
    def play_track_uri(self, track_uri: Track):
        print('Playing')
        ic(track_uri, self.active_devices)
        if len(self.active_devices) > 0:
            self._sp.start_playback(uris=[track_uri])

    def queue_track_uri(self, track_uri: Track):
        print('Queueing')
        ic(track_uri, self.active_devices)
        if len(self.active_devices) > 0:
            self._sp.add_to_queue(track_uri)

        
    ### PLAYLISTS
    def select_playlist(self, pl_name: str):
        self.selected_playlist = [
            pl 
            for pl 
            in self.playlists 
            if pl.playlist_name == pl_name
        ][0]

        if pl_name not in self.lib_tracks:
            self.fetch_tracks_for_playlist(self.selected_playlist)

    ### SEARCH STAGING
    def stage_genre_for_search(self, genre):
        self.search_genre = genre
    
    def clear_search_genre(self):
        self.search_genre = ''

    #### SEEDING
    def add_track_uri_to_seeds(self, uri: str, source: str):
        if uri not in self.seed_track_uris_with_source:
            self.seed_track_uris_with_source = [*self.seed_track_uris_with_source, (uri, source)]

    def remove_track_uri_from_seeds(self, uri: str):
        self.seed_track_uris_with_source = [
            (u, s)
            for u, s
            in self.seed_track_uris_with_source
            if u != uri
        ]

    def add_genre_to_seeds(self, genre: str):
        if genre not in self.seed_genres:
            self.seed_genres = [*self.seed_genres, genre]

    def remove_genre_from_seeds(self, genre: str):
        self.seed_genres = [
            g for g in self.seed_genres
            if g != genre
        ]

    def add_artist_to_seeds(self, artist: tuple[str, str]):
        if artist not in self.seed_artists:
            self.seed_artists = [*self.seed_artists, artist]
        # print(self.seed_artists)

    def remove_artist_from_seeds(self, artist: tuple[str, str]):
        self.seed_artists = [
            a for a in self.seed_artists
            if a != artist
        ]

    @rx.var
    def seed_tracks(self) -> list[Track]:
        all_tracks_flattened = [
            item for sublist
            in self.lib_tracks.values() 
            for item in sublist
        ]
        return [
            [t for t in all_tracks_flattened if t.uri == u][0]
            for u in self.seed_track_uris
        ]

    @rx.var
    def seed_track_uris(self) -> list[str]:
        return [uri for uri, source in self.seed_track_uris_with_source]
    
    @rx.var
    def seed_artist_uris(self) -> list[str]:
        return [uri for uri, name in self.seed_artists]

    @rx.var
    def rp_tracks(self) -> list[Track]:
        return self.lib_tracks['____recent']
    
    @rx.var
    def liked_tracks(self) -> list[Track]:
        return self.lib_tracks['____liked']

    @rx.var
    def selected_playlist_tracks(self) -> list[Track]:
        return self.lib_tracks[self.selected_playlist.playlist_name]

    @rx.var
    def playlist_names(self) -> list[str]:
        return [p.playlist_name for p in self.playlists]
    
    @rx.var
    def total_seeds(self) -> int:
        return len(self.seed_artists) + len(self.seed_tracks)
    @rx.var
    def too_many_seeds(self) -> bool:
        return self.total_seeds > 5
    
    @rx.var
    def too_few_seeds(self) -> bool:
        return self.total_seeds == 0

    @rx.var
    def recommendations_generated(self) -> bool:
        return len(self.recc_tracks) > 0
    
    @rx.var
    def active_devices(self) -> bool:
        return [d for d in self._sp.devices()['devices'] if d['is_active']]