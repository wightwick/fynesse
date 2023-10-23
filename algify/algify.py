"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config

import reflex as rx
from data import Track
from icecream import ic
from datetime import datetime
import pandas as pd
from spotipy import Spotify, SpotifyOAuth
from spotify_secrets import *

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

    tracks: dict = {'recent': [],}

    def fetch_rp_tracks(self):
        raw_rp_tracks = sp.current_user_recently_played(limit=50)['items']
        self.tracks['recent'] = [Track(item['track']) for item in raw_rp_tracks]
        # print(raw_rp_tracks)


    @rx.var
    def rp_tracks_data(self) -> list[list]:
        return [
            [t.name, t.uri]
            for t in self.tracks['recent']
        ]


def track_card(name):
    return rx.box(rx.text(name))

def rp_tracks_table():

    table = rx.data_table(
        columns=["Name", "Uri"],
        data=State.rp_tracks_data,
        pagination=True,
        sort=True,
        # search=True,
    )
    return table

def rp_tracks_cards():
    stack = rx.vstack(
        rx.foreach(
            State.rp_tracks_data,
            lambda x: rx.box(x[0])
        ), 
        
    )
    return stack

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            # rp_tracks_table(),
            rp_tracks_cards(),
            rx.spacer(),
            # width=PAGE_WIDTH,
            height="70%",
        ),
        height="100vh",
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index, on_load=State.fetch_rp_tracks)
app.compile()
