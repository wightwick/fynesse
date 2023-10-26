from rxconfig import config

import reflex as rx
from algify.data import Track
from icecream import ic
from .state import State

PAGE_WIDTH = "100vw"
GREEN = '#1DB954'

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

def header_bar() -> rx.Component:
    return rx.center(
        rx.heading('algify'),
        size='5xl',
        margin_bottom='10',
        width='100%',
    )

def artist_card(
        artist_uri_name: tuple[str, str],
        add_remove_button: bool
    ) -> rx.Component:
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
    
def track_add_seed_button(track: Track, source: str) -> rx.Component:
    return rx.button(
        '🌱',
        on_click=State.add_track_uri_to_seeds(track.uri, source),
        is_disabled=State.seed_track_uris.contains(track.uri),
    )

def track_remove_seed_button(track: Track) -> rx.Component:
    return rx.button(
        rx.icon(tag="minus"),
        on_click=State.remove_track_uri_from_seeds(track.uri),
    )

def track_card(
        track: Track,
        button: rx.Component,
        artists_interactive: bool,
        show_genres: bool=False,
        genres_interactive: bool=True
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
                        
                        
                        rx.cond(
                            genres_interactive,
                            rx.wrap(
                                rx.foreach(
                                    track.artist_genres,
                                    #lambda x: rx.box(x, border_radius='xl', border_width='thin')
                                    lambda x: rx.wrap_item(genre_card(x))
                                ),
                                padding_bottom='1.5'
                            ),
                            rx.text('#' + track.artist_genres.join(', #'), as_='small')
                        ),
                        



                        rx.text('')
                    ),

                    align_items='left',
                ),
                rx.spacer(),
                button
        ),
        border_width=2,
        border_radius='lg',
        overflow='hidden',
        padding_right=3,
        width='100%',
    )

def sub_pane_view(
        content: rx.Component,
        heading: str,
        border_color: str = None
    ) -> rx.Component:
    return rx.box(
            rx.vstack(
                rx.heading(
                    heading,
                    size='md',
                    margin_bottom=-3,
                    margin_left=2
                ),
                rx.box(
                    content,
                    border_width='medium',
                    border_radius='xl',
                    border_color=border_color,
                    padding='10px',
                    width=400

                ),
                align_items='left'
            ),
            
        )

def seeds_list() -> rx.Component:
    return rx.box(
            rx.vstack(
            
                rx.vstack(
                    rx.foreach(
                        State.seed_tracks,
                        lambda x: rx.wrap_item(
                            track_card(
                                track=x,
                                show_genres=False,
                                artists_interactive=False,
                                button=track_remove_seed_button(x)
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
        )

def seeds_view() -> rx.Component:
    return rx.cond(
        State.too_many_seeds,
        sub_pane_view(
            content=seeds_list(),
            heading='Seeds',
            border_color='red'
        ),
        sub_pane_view(
            content=seeds_list(),
            heading='Seeds'
        )
    )

def param_slider(
        param_name: str,
        # initial_value: rx.var,
        state_value_setter: callable,
        state_enabled_var: callable,
        state_enable_disable_fn: callable
    ):

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(param_name, as_='b'),
                rx.switch(
                    is_checked=state_enabled_var,
                    on_change=state_enable_disable_fn
                )

            ),
            rx.slider(
                    # value=initial_value,
                    default_value=0,
                    is_disabled=~state_enabled_var,
                    on_change=state_value_setter,
                    min_=0,
                    max_=100
                    
            ),
            align_items='left'
        ),
        width='100%'
    )
            

def recommendations_view():
    return rx.box(
        rx.vstack(
            seeds_view(),
            sub_pane_view(
                content=rx.vstack(
                    param_slider(
                        'Target acousticness',
                        state_value_setter=State.set_recc_target_acousticness_value,
                        state_enabled_var=State.recc_target_acousticness_enabled,
                        state_enable_disable_fn=State.enable_disable_recc_target_acousticness
                    ),
                    param_slider(
                        'Target energy',
                        state_value_setter=State.set_recc_target_energy_value,
                        state_enabled_var=State.recc_target_energy_enabled,
                        state_enable_disable_fn=State.enable_disable_recc_target_energy
                    ),
                    param_slider(
                        'Target liveness',
                        state_value_setter=State.set_recc_target_liveness_value,
                        state_enabled_var=State.recc_target_liveness_enabled,
                        state_enable_disable_fn=State.enable_disable_recc_target_liveness
                    ),
                    param_slider(
                        'Target danceability',
                        state_value_setter=State.set_recc_target_danceability_value,
                        state_enabled_var=State.recc_target_danceability_enabled,
                        state_enable_disable_fn=State.enable_disable_recc_target_danceability
                    ),
                    param_slider(
                        'Target instrumentalness',
                        state_value_setter=State.set_recc_target_instrumentalness_value,
                        state_enabled_var=State.recc_target_instrumentalness_enabled,
                        state_enable_disable_fn=State.enable_disable_recc_target_instrumentalness
                    )

                ),

                heading='Parameters'
            ),
            rx.button(
                'Generate',
                on_click=State.fetch_recommendations(),
                is_disabled=State.too_many_seeds,
                width='100%',
                border_radius='xl'
            ),
            rx.cond(
                State.recommendations_generated,
                sub_pane_view(
                    rx.vstack(
                        rx.foreach(
                            State.recc_tracks,
                            lambda x: rx.wrap_item(
                                track_card(
                                    track=x,
                                    show_genres=True,
                                    genres_interactive=False,
                                    artists_interactive=False,
                                    button=track_remove_seed_button(x)
                                )
                            ),
                        ),
                    ), 
                    heading='Output', 
                    border_color=GREEN
                ),
                 sub_pane_view(
                    rx.text(''), 
                    heading='Output', 
                ),
            )
            
        )
    )

def search_view():
    return sub_pane_view(
        rx.box(
            rx.vstack(
                rx.input(
                    placeholder='Genre',
                    value=State.search_genre,
                    on_change=State.set_search_genre,    
                ),
            ),
            width=400
        ),
        heading='Parameters'
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

def pane_view(
        content: rx.component,
        heading_text: str,
        padding: int = 3
    ) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(
                heading_text,
                margin_left=2,
                margin_bottom=-4
            ),
            rx.box(
                content,
                border_width='thick',
                border_radius='3xl',
                padding=padding
            ),
            align_items='left'
        ),
        margin_left=1,
        margin_right=1
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
                                artists_interactive=True,
                                button=track_add_seed_button(x, source='recent')
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
                            artists_interactive=True,
                            button=track_add_seed_button(x, source='playlist')
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
                                artists_interactive=True,
                                button=track_add_seed_button(x, source='liked')
                            )
            ),
            rx.button('Load more', on_click=State.fetch_liked_tracks_batch)
        ),
    )

def index() -> rx.Component:
    return rx.container(
            rx.vstack(
                header_bar(),
                rx.flex(
                    pane_view(library_view(), 'Library', padding=None),
                    pane_view(recommendations_view(), 'Recommendations'),
                    pane_view(search_view(), 'Search'),
                    align_items='top',
                ),
                rx.spacer(),
            ),
            
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index, on_load=State.on_load_fetch)
app.compile()
