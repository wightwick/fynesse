"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config

import reflex as rx
from algify.data import Track
from icecream import ic
from .state import State

PAGE_WIDTH = "60vw"
FULL = "100%"

def genre_card(genre: str, add_remove_button: bool):
    return rx.box(
        rx.hstack(
            rx.text('#' + genre, as_='small'),
            rx.cond(
                add_remove_button,
                rx.button(
                    rx.icon(tag="add", width='10px'),
                    on_click=State.add_genre_to_seeds(genre),
                    is_disabled=State.selected_genres.contains(genre),
                    border="1px solid #ddd",
                    size='sm'
                ),
                rx.button(
                    rx.icon(tag="minus"),
                    on_click=State.remove_genre_from_seeds(genre),
                    border="1px solid #ddd",
                    size='sm'
                ),
            ),
        ),
        
        border_radius='sm',
        border_width='thin',
        padding='2px 4px'
    )
    

def track_card(track: Track, add_remove_button: bool, source: str):    
    return rx.box(
            rx.hstack(
                rx.image(src_set=track.album_art_srcset, html_width='100'),
                rx.vstack(
                    rx.box(
                        rx.text(
                            track.track_name,
                            as_='strong'
                        )
                    ),
                    # rx.text(track.added_at),
                    rx.box(track.artist_names.join(', ')),
                    rx.box(
                        rx.text(
                            track.album_name,
                            as_='small'
                        )
                    ),
                    
                    rx.cond(
                        track.artist_genres.length() > 0, 
                        rx.wrap(
                            rx.foreach(
                                track.artist_genres,
                                #lambda x: rx.box(x, border_radius='xl', border_width='thin')
                                lambda x: rx.wrap_item(genre_card(x, True))
                            )
                        ),
                        rx.text('')
                    ),

                    align_items='left',
                ),
                rx.cond(
                    add_remove_button,
                    rx.button(
                        rx.icon(tag="add"),
                        on_click=State.add_uri(track.uri, source),
                        is_disabled=State.selected_track_uris.contains(track.uri),
                        border="1px solid #ddd",
                    ),
                    rx.button(
                        rx.icon(tag="minus"),
                        on_click=State.remove_uri(track.uri),
                        # is_disabled=State.selected_track_uris.contains(track.uri),
                        border="1px solid #ddd",
                    ),
                )
        ),
        border_width='medium',
        border_radius='lg'
    )

def selections_view():
    return rx.box(
        rx.vstack(
            rx.heading('Selections'),
            rx.hstack(
                rx.wrap(
                    rx.foreach(
                        State.selected_tracks,
                        lambda x: rx.wrap_item(track_card(x, False, '')
                        )
                    )
                ),
                rx.wrap(
                    rx.foreach(
                        State.selected_genres,
                        lambda x: rx.wrap_item(genre_card(x, False)
                        )
                    )
                )
            )
        ),
        
        border_width='thick',
        border_radius='xl',
        padding='10px'
    )

def rp_tracks_list_view():
    stack = rx.vstack(
        rx.hstack(
            rx.heading('Recently played'),
            rx.spacer(),
            rx.button(
                rx.text('Get genres'),
                on_click=State.fetch_genres_rp, size='md',
                is_disabled=State.rp_tracks_have_genre,
            )
        ),
        rx.foreach(
            State.rp_tracks,
            lambda x: track_card(x, True, 'recent')
        ),
        align_items='left',
        width=500
    )
    
    return rx.box(
        stack,
        border_width='thick',
        border_radius='xl',
        padding='10px'
    )

# def selected_tracks_view():
#     return rx.text('Selected')

def index() -> rx.Component:
    return rx.center(
            rx.vstack(
                selections_view(),
                genre_card('test', True),
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
