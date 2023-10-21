# state.py
import reflex as rx
from spotipy import SpotifyOAuth


class State(rx.State):
    rp_tracks: list
    pass