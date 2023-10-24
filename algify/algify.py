"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config

import reflex as rx
from data import Track
from icecream import ic
from datetime import datetime
import pandas as pd
from spotipy import Spotify, SpotifyOAuth
from spotify_secrets import *
from datetime import datetime

PAGE_WIDTH = "60vw"
FULL = "100%"


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

sp = Spotify(
    auth_manager=SpotifyOAuth(
        scope=scopes,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        open_browser=True
    )
)


class State(rx.State):
    """The app state."""

    tracks: dict[str, list[Track]] = {'recent': [],}
    rp_tracks_have_genre: bool = False

    def fetch_rp_tracks(self):
        raw_rp_tracks = sp.current_user_recently_played(limit=50)['items']
        self.tracks['recent'] = [Track(item) for item in raw_rp_tracks]
        self.rp_tracks_have_genre = False

    def fetch_genres_rp(self):
        self.tracks['recent'] = [
            track.with_artist_genres(sp) for track
            in self.tracks['recent']
        ]
        self.rp_tracks_have_genre = True

    @rx.var
    def rp_tracks_data(self) -> list[Track]:
        return self.tracks['recent']
        

def genre_card(genre: str):
    return rx.box(
        genre,
        border_radius='xl',
        border_width='thin',
        padding='6px 10px'
    )
    

def track_card(track: Track):    
    return rx.box(
            rx.hstack(
                rx.image(src_set=track.album_art_srcset, html_width='100'),
                rx.vstack(
                    rx.box(track.track_name),
                    # rx.text(track.added_at),
                    rx.box(track.artist_names.join(', ')),
                    rx.box(track.album_name),
                    
                    rx.cond(
                        track.artist_genres.length() > 0, 
                        rx.wrap(
                            rx.foreach(
                                track.artist_genres,
                                #lambda x: rx.box(x, border_radius='xl', border_width='thin')
                                lambda x: rx.wrap_item(genre_card(x))
                            )
                        ),
                        rx.text('')
                    ),

                    align_items='left',
                )
        ),
        border_width='thick',
        border_radius='lg'
    )


def rp_tracks_list_view():
    stack = rx.vstack(
        rx.button(
            rx.text('Get genres'),
            on_click=State.fetch_genres_rp, size='lg',
            is_disabled=State.rp_tracks_have_genre
        ),
        rx.foreach(
            State.rp_tracks_data,
            track_card
        ),
        align_items='left',
        width=500
    )
    return stack

# def selected_tracks_view():
#     return rx.text('Selected')

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rp_tracks_list_view(),
            rx.spacer(),
            height="70%",
        ),
        height="100vh",
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index, on_load=State.fetch_rp_tracks)
app.compile()
