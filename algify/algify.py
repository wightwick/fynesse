"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config
from data import Track
from spotipy import Spotify, SpotifyOAuth
from spotify_secrets import *
from pdb import set_trace
import json
import reflex as rx

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"

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

# state.py
import reflex as rx
from spotipy import SpotifyOAuth


class TracksState(rx.State):
    rp_tracks: list[Track] = [Track(item['track']) for item in sp.current_user_recently_played(limit=50)['items']]

    def fetch_recently_played_tracks(self):
        recently_played = sp.current_user_recently_played(limit=50)['items']
        self.rp_tracks = [Track(item['track']) for item in recently_played]
        print(self.rp_tracks)

    def serve_tracks_data(self, track_list) -> list[list]:
        return [
            t.name
            for t in track_list
        ]



# State.fetch_recently_played_tracks()
#
# set_trace()

# set_trace()

# print(state.rp_tracks[0])

# print([t.name for t in State.rp_tracks])
# set_trace()

TracksState.fetch_recently_played_tracks()

def colored_box(t):
    return rx.box(rx.text(t.name))


def index() -> rx.Component:
    # print(sp.current_user_playing_track())

    # print(rp_tracks[0])

    # print(state)

    # print(state.rp_tracks)
    # print(state)

    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float="right"),
        rx.vstack(
            rx.text('abc'),
            rx.vstack(
                rx.foreach(
                    TracksState.rp_tracks,
                    colored_box
                ),
            )
        )
    )

set_trace()

# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.compile()
