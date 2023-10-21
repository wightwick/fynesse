"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config
from data import Track
from spotipy import Spotify, SpotifyOAuth
from state import State
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

recently_played = sp.current_user_recently_played(limit=50)['items']
rp_tracks = [json.dumps(Track(item['track']).__dict__) for item in recently_played]

state = State() 
state.rp_tracks = rp_tracks
# print(state.rp_tracks[0])

# print([t.name for t in State.rp_tracks])
# set_trace()


def colored_box(t: dict):
    td = json.loads(t)
    return rx.box(rx.text(t['name']))


def index() -> rx.Component:
    # print(sp.current_user_playing_track())

    # print(rp_tracks[0])

    # print(state)

    # print(state.rp_tracks)
    # print(state)

    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float="right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", font_size="2em"),
            rx.box("Get started by editing ", rx.code(filename, font_size="1em")),
            rx.box(
                "some additional shit",
                border_width='thin'
                ),
            rx.link(
                "Check out our docs!",
                href=docs_url,
                border="0.1em solid",
                padding="0.5em",
                border_radius="0.5em",
                _hover={
                    "color": rx.color_mode_cond(
                        light="rgb(107,99,246)",
                        dark="rgb(179, 175, 255)",
                    )
                },
            ),

            rx.vstack(
                    rx.foreach(state.rp_tracks, colored_box),
            ),

            # colored_box(rp_tracks[0])

        )
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.compile()
