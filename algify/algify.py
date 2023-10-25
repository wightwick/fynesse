from rxconfig import config

import reflex as rx
from algify.data import Track
from icecream import ic
from .state import State
from .constants import *

PAGE_WIDTH = "60vw"
FULL = "100%"

def genre_card(genre: str, add_remove_button: bool):
    return rx.box(
        rx.hstack(
            rx.text('#' + genre, as_='small'),
            rx.cond(
                add_remove_button,
                rx.button(
                    rx.icon(tag="add"),
                    on_click=State.add_genre_to_seeds(genre),
                    is_disabled=State.seed_genres.contains(genre),
                    size='xs',
                    variant='ghost'
                ),
                rx.button(
                    rx.icon(tag="minus"),
                    on_click=State.remove_genre_from_seeds(genre),
                    size='xs',
                    variant='ghost'
                ),
            ),
        ),
        
        border_radius='lg',
        border_width='thin',
        padding_left='6px'
    )

def artist_card(artist_uri_name: tuple[str, str], add_remove_button: bool):
    return rx.box(
        rx.hstack(
            rx.text(artist_uri_name.__getitem__(1)),
            rx.cond(
                add_remove_button,
                rx.button(
                    rx.icon(tag="add"),
                    on_click=State.add_artist_to_seeds(artist_uri_name),
                    is_disabled=State.seed_artist_uris.contains(artist_uri_name.__getitem__(0)),
                    size='xs',
                    variant='ghost'
                ),
                rx.button(
                    rx.icon(tag="minus"),
                    on_click=State.remove_artist_from_seeds(artist_uri_name),
                    size='xs',
                    variant='ghost'
                ),
            ),
        ),
        
        border_radius='lg',
        border_width='thin',
        padding_left='6px'
    )
    

def track_card(
        track: Track,
        add_remove_button: bool,
        source: str,
        show_genres: bool,
        artists_interactive: bool,
    ):    
    return rx.box(
            rx.hstack(
                rx.image(
                    src_set=track.album_art_srcset,
                    html_width='100'
                ),
                rx.vstack(
                    rx.box(
                        rx.text(
                            track.track_name,
                            as_='strong'
                        ),
                        margin_top='0.5'
                    ),
                    rx.cond(
                        artists_interactive,
                        rx.wrap(
                            rx.foreach(
                                track.artist_uris_names,
                                #lambda x: rx.box(x, border_radius='xl', border_width='thin')
                                lambda x: rx.wrap_item(artist_card(x, True))
                            )
                        ),
                        rx.text(track.artist_names.join(', '))
                    ),
                    rx.box(
                        rx.text(
                            track.album_name,
                            as_='small'
                        )
                    ),
                    
                    rx.cond(
                        (track.artist_genres.length() > 0) & show_genres, 
                        rx.wrap(
                            rx.foreach(
                                track.artist_genres,
                                #lambda x: rx.box(x, border_radius='xl', border_width='thin')
                                lambda x: rx.wrap_item(genre_card(x, True))
                            ),
                            padding_bottom='1.5'
                        ),
                        rx.text('')
                    ),

                    align_items='left',
                ),
                rx.spacer(),
                rx.cond(
                    add_remove_button,
                    rx.button(
                        rx.icon(tag="add"),
                        on_click=State.add_track_uri_to_seeds(track.uri, source),
                        is_disabled=State.seed_track_uris.contains(track.uri),
                    ),
                    rx.button(
                        rx.icon(tag="minus"),
                        on_click=State.remove_track_uri_from_seeds(track.uri),
                    ),
                )
        ),
        border_width='medium',
        border_radius='lg',
        overflow='hidden',
        padding_right='3',
        width='100%',
    )

def seeds_view():
    return rx.box(
        rx.vstack(
            rx.heading('Seeds', size='md'),
            rx.hstack(
                rx.box(
                    rx.vstack(
                        rx.foreach(
                            State.seed_tracks,
                            lambda x: rx.wrap_item(
                                track_card(
                                    track=x,
                                    show_genres=False,
                                    source='',
                                    artists_interactive=False,
                                    add_remove_button=False
                                )
                            ),
                        ),
                    ),
                ),
                rx.box(
                    rx.vstack(
                        rx.foreach(
                            State.seed_genres,
                            lambda x: rx.wrap_item(
                                genre_card(x, False)
                            ),
                        ),
                    ),
                ),
                rx.box(
                    rx.vstack(
                        rx.foreach(
                            State.seed_artists,
                            lambda x: rx.wrap_item(
                                artist_card(x, False)
                            ),
                        ),
                    ),
                ),
            ),
        ),
        
        border_width='thick',
        border_radius='xl',
        padding='10px'
    )

def rp_tracks_list_view():
    stack = rx.vstack(
        rx.hstack(
            # rx.heading('Recently played', size='md'),
            rx.radio_group(
                rx.vstack(
                    rx.foreach(
                        RP_LIKED_OPTIONS,
                        lambda option: rx.radio(option, as_='strong'),
                    ),
                    align_items='left',
                ),
                default_value=RP_LIKED_OPTIONS[0],
                on_change=State.set_rp_liked_selection
            ),
            rx.spacer(),
            
            rx.cond(
                State.rp_liked_selection == RP_LIKED_OPTIONS[0],
                rx.button(
                    rx.text('Get genres'),
                    on_click=State.fetch_genres_rp,
                    size='md',
                    is_disabled=State.rp_tracks_have_genre,
                ),
                rx.button(
                    rx.text('Get genres'),
                    on_click=State.fetch_genres_liked,
                    size='md',
                    is_disabled=State.liked_tracks_have_genre,
                )
            ),
        ),
        rx.cond(
            State.rp_liked_selection == RP_LIKED_OPTIONS[0],
            rx.foreach(
                State.rp_tracks,
                lambda x: track_card(
                                track=x,
                                show_genres=True,
                                source='recent',
                                artists_interactive=True,
                                add_remove_button=True
                            )
            ),
            rx.vstack(
                rx.foreach(
                    State.liked_tracks,
                    lambda x: track_card(
                                    track=x,
                                    show_genres=True,
                                    source='recent',
                                    artists_interactive=True,
                                    add_remove_button=True
                                )
                ),
                rx.button('Load more', on_click=State.fetch_liked_tracks_batch)
            ),
        ),
        
        align_items='left',
        width=500,
    )
    
    return rx.box(
        stack,
        border_width='thick',
        border_radius='xl',
        padding='10px'
    )

def playlist_view():
    stack = rx.vstack(
        rx.hstack(
            rx.heading('Playlist', size='md'),
            rx.spacer(),
            rx.select(
                State.playlist_names,
                on_change=State.select_playlist,
            ),
            rx.spacer(),
            rx.button(
                rx.text('Get genres'),
                on_click=State.fetch_genres_selected_pl, size='md',
                is_disabled=State.selected_playlist.has_genres,
            )
        ),
        rx.foreach(
            State.selected_playlist_tracks,
            lambda x: track_card(
                            track=x,
                            show_genres=True,
                            source='recent',
                            artists_interactive=True,
                            add_remove_button=True
                        )
        ),
        align_items='left',
        width=500,
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
    return rx.container(
            rx.vstack(
                seeds_view(),
                rx.hstack(
                    rp_tracks_list_view(),
                    playlist_view(),
                    align_items='top'
                ),
                rx.spacer(),
                height="70%",
            ),
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index, on_load=State.on_load_fetch)
app.compile()
