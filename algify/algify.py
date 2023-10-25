from rxconfig import config

import reflex as rx
from algify.data import Track
from icecream import ic
from .state import State

PAGE_WIDTH = "100vw"

def genre_card(genre: str):
    return rx.box(
        rx.hstack(
            rx.text('#' + genre, as_='small'),
                rx.button(
                    rx.icon(tag="search"),
                    on_click=State.stage_genre_for_search(genre),
                    
                    size='xs',
                    variant='ghost'
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
                    '🌱',
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
                                lambda x: rx.wrap_item(genre_card(x))
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
                        '🌱',
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

def seeds_view() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(
                'Seeds', 
                size='md',
                margin_bottom=-3,
                margin_left=2
            ),
            rx.box(
                rx.vstack(
                
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
                
                    rx.vstack(
                        rx.foreach(
                            State.seed_artists,
                            lambda x: rx.wrap_item(
                                artist_card(x, False)
                            ),
                        ),
                    ),
                    align_items='center'
                ),
                
                border_width='medium',
                border_radius='xl',
                padding='10px',
                width=400

            ),
            align_items='left'
        ),
        
    )

def recommendations_view():
    return rx.box(
        rx.vstack(
            seeds_view(),
            rx.button(
                'Generate',
                is_full_width=True
            ),
        ),
        padding='3'
    )

def search_view():
    return rx.box(
            rx.vstack(
                rx.input(
                    placeholder='Genre',
                    value=State.search_genre,
                    on_change=State.set_search_genre,    
                ),
            ),
            width=400
        )


def library_view() -> rx.Component:
    tabs = rx.tabs(
        rx.tab_list(
            rx.tab('Recently Played'),
            rx.tab('Liked Songs'),
            rx.tab('Playlist'),
        ),
        rx.tab_panels(
            rx.tab_panel(recent_tracks_panel()),
            rx.tab_panel(liked_songs_view_panel()),
            rx.tab_panel(playlist_browser_panel()),
        ),
    )
  
    return rx.box(
        tabs,
        width=400
    )
# rx.vstack(
#         rx.heading(
#             'Library',
#             margin_left='2',
#             margin_bottom='-4'
#         ),
#         rx.box(
#             tabs,
#             border_width='thick',
#             border_radius='xl',
#         ),
#         align_items='left'
#     )

def view_pane(content: rx.component, heading_text: str) -> rx.Component:
    return rx.vstack(
        rx.heading(
            heading_text,
            margin_left='2',
            margin_bottom='-4'
        ),
        rx.box(
            content,
            border_width='thick',
            border_radius='2xl',
        ),
        align_items='left'
    )

def recent_tracks_panel() -> rx.Component:
    return rx.vstack(
        rx.button(
            rx.text('Get genres'),
            on_click=State.fetch_genres_rp,
            size='md',
            is_disabled=State.rp_tracks_have_genre,
        ),
        rx.vstack(
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
        )
    )

def playlist_browser_panel() -> rx.Component:
    return rx.vstack(
        rx.hstack(
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
    )

def liked_songs_view_panel() -> rx.Component:
    return rx.vstack(
        rx.button(
            rx.text('Get genres'),
            on_click=State.fetch_genres_liked,
            size='md',
            is_disabled=State.liked_tracks_have_genre,
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
    )

def index() -> rx.Component:
    return rx.container(
            rx.vstack(
                rx.flex(
                    view_pane(library_view(), 'Library'),
                    view_pane(recommendations_view(), 'Recommendations'),
                    view_pane(search_view(), 'Search'),
                    align_items='top',
                ),
                rx.spacer(),
            ),
            
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index, on_load=State.on_load_fetch)
app.compile()
