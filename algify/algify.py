from rxconfig import config

import reflex as rx
from algify.data import Track
from icecream import ic
from .state import *
from .constants import *

PAGE_WIDTH = "100vw"
GREEN = '#1DB954'

def genre_card(genre: str):
    return rx.box(
        rx.hstack(
            rx.text('#' + genre, as_='small'),
                rx.button(
                    rx.icon(tag="search"),
                    on_click=SearchState.stage_genre_for_search(genre),
                    
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
        rx.heading(''),
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

def track_play_button(track: Track) -> rx.Component:
    return rx.button(
        rx.box(
            rx.icon(tag='triangle_down'),
            transform='rotate(-90deg)'
        ),
        on_click=State.play_track_uris([track.uri]),
    )

def track_queue_button(track: Track) -> rx.Component:
    return rx.button(
        rx.icon(tag='plus_square'),
        on_click=State.queue_track_uri(track.uri),
     )

def track_multi_button(track: Track) -> rx.Component:
    return rx.popover(
        rx.popover_trigger(
            rx.button(
                rx.icon(tag='triangle_down'),
                # on_click=State.queue_track_uri(track.uri),
            )
        ),
        rx.popover_content(
            rx.popover_header(height=8),
            rx.popover_body(
                rx.vstack(
                    track_add_seed_button(track, source='search'),
                    track_play_button(track),
                    track_queue_button(track),
                )
            ),
            rx.popover_close_button(),
            width='30'
        ),
    )

def track_card(
        track: Track,
        buttons: list[rx.Component],
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
                rx.vstack(*buttons)
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
                    margin_bottom='-13px',
                    margin_left=2,
                    z_index=2
                ),
                rx.box(
                    content,
                    border_width='medium',
                    border_radius='xl',
                    border_color=border_color,
                    padding=15,
                    width=400,
                    z_index=1
                ),
                align_items='left'
            ),
            
        )

def hint_text(text: str):
    return rx.text(
        text,
        opacity=0.3,
        text_align='center',
    )
    

def seeds_list() -> rx.Component:
    return rx.box(
            rx.cond(State.too_few_seeds,
                hint_text('plant some seeds'),
                rx.vstack(
                    rx.vstack(
                        rx.foreach(
                            State.seed_tracks,
                            lambda x: track_card(
                                    track=x,
                                    show_genres=False,
                                    artists_interactive=False,
                                    buttons=[track_remove_seed_button(x)]
                                )
                        ),
                        width='100%'
                    ),
                    rx.vstack(
                        rx.foreach(
                            State.seed_artists,
                            lambda x: artist_card(x, False)
                        ),
                    ),
                    align_items='center'
                ),
            )
        )

def seeds_view() -> rx.Component:
    return sub_pane_view(
        content=seeds_list(),
        heading='Seeds',
        border_color=rx.cond(State.too_many_seeds, 'red', '')
    )

def switchable_param_slider(
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

def param_slider(
        text: str,
        state_value_setter: callable,
        default_value: int,
        min_max: list[int]
    ):
    return rx.box(
        rx.vstack(
            rx.text(
                text,
                as_='b'
            ),
            rx.slider(
                    default_value=default_value,
                    on_change=state_value_setter,
                    min_=min_max[0],
                    max_=min_max[1]
            ),
            align_items='left'
        ),
        width='100%'
    )

def playlist_create_dialog(): 
    return rx.alert_dialog(
        rx.alert_dialog_overlay(
            rx.alert_dialog_content(
                rx.hstack(
                    rx.box(
                        rx.alert_dialog_header(
                            'Export to playlist',
                        ),
                        width='100%'
                    ),
                    rx.spacer(),
                    rx.box(
                        rx.button(
                            rx.icon(tag='close'),
                            on_click=PlaylistDialogState.change,
                        ),
                        padding_right=6
                    )
                ),
                rx.alert_dialog_body(
                    rx.input(
                        placeholder='name',
                        on_change=PlaylistDialogState.set_pl_name,
                    ),
                ),
                rx.alert_dialog_footer(
                    rx.button(
                        "Create playlist",
                        on_click=PlaylistDialogState.create_and_dismiss(),
                        is_disabled=PlaylistDialogState.name_invalid
                    )
                ),
            )
        ),
        is_open=PlaylistDialogState.show,
    )


def recommendations_view():
    return rx.box(
        rx.vstack(
            seeds_view(),
            sub_pane_view(
                content=rx.vstack(
                    switchable_param_slider(
                        'Target acousticness',
                        state_value_setter=State.set_recc_target_acousticness_value,
                        state_enabled_var=State.recc_target_acousticness_enabled,
                        state_enable_disable_fn=State.enable_disable_recc_target_acousticness
                    ),
                    switchable_param_slider(
                        'Target energy',
                        state_value_setter=State.set_recc_target_energy_value,
                        state_enabled_var=State.recc_target_energy_enabled,
                        state_enable_disable_fn=State.enable_disable_recc_target_energy
                    ),
                    switchable_param_slider(
                        'Target liveness',
                        state_value_setter=State.set_recc_target_liveness_value,
                        state_enabled_var=State.recc_target_liveness_enabled,
                        state_enable_disable_fn=State.enable_disable_recc_target_liveness
                    ),
                    switchable_param_slider(
                        'Target danceability',
                        state_value_setter=State.set_recc_target_danceability_value,
                        state_enabled_var=State.recc_target_danceability_enabled,
                        state_enable_disable_fn=State.enable_disable_recc_target_danceability
                    ),
                    switchable_param_slider(
                        'Target instrumentalness',
                        state_value_setter=State.set_recc_target_instrumentalness_value,
                        state_enabled_var=State.recc_target_instrumentalness_enabled,
                        state_enable_disable_fn=State.enable_disable_recc_target_instrumentalness
                    ),
                    param_slider(
                        text=f'Number of recommended tracks: {State.num_recommendations}',
                        state_value_setter=State.set_num_recommendations,
                        default_value=NUM_RECCOMENDATIONS_DEFAULT,
                        min_max=[1,100]
                    )
                ),

                heading='Parameters'
            ),
            pane_button(
                text='Generate',
                on_click=State.fetch_recommendations(),
                is_disabled=State.too_many_seeds | State.too_few_seeds,
            ),
            rx.cond(
                State.recommendations_generated,
                sub_pane_view(
                    rx.vstack(
                        rx.hstack(
                            sub_pane_button(
                                text='Play all',
                                on_click=State.play_all_recommended_tracks
                            ),
                            sub_pane_button(
                                text='Export to playlist',
                                on_click=PlaylistDialogState.change
                            ),
                            width='100%'
                        ),
                        rx.foreach(
                            State.recc_tracks,
                            lambda x: track_card(
                                track=x,
                                show_genres=True,
                                genres_interactive=False,
                                artists_interactive=False,
                                buttons=[
                                    track_play_button(x),
                                    track_queue_button(x)
                                ]
                            )
                        ),
                        width='100%'
                    ), 
                    heading='Results', 
                    border_color=GREEN
                ),
                sub_pane_view(
                    rx.cond(
                        ~(State.too_few_seeds | State.too_many_seeds),
                        hint_text('click generate'),
                        rx.text('')
                    ),
                    heading='Results', 
                ),
            )
            
        ),
        playlist_create_dialog()
    )

def switchable_input_field(
        name: str,
        value: callable,
        on_change: callable,
        state_enabled_var: callable,
        state_enable_disable_fn: callable,
    ):
    return rx.vstack(
        rx.text(
            name,
            margin_bottom=-3.5,
            margin_left=1,
            opacity=rx.cond(state_enabled_var, 1, 0.5)
        ),
        rx.hstack(
            rx.input(
                value=value,
                on_change=on_change,
                is_disabled=~state_enabled_var,
            ),
            rx.switch(
                is_checked=state_enabled_var,
                on_change=state_enable_disable_fn
            )
        ),
        align_items='left',
        width='100%'
    )

def search_view():
    return rx.vstack(
        sub_pane_view(
            rx.box(
                rx.vstack(
                    switchable_input_field(
                        name='Name',
                        value=SearchState.search_name,
                        on_change=SearchState.set_search_name,
                        state_enabled_var=SearchState.name_search_enabled,
                        state_enable_disable_fn=SearchState.toggle_name_search
                    ),
                    switchable_input_field(
                        name='Genre',
                        value=SearchState.search_genre,
                        on_change=SearchState.set_search_genre,
                        state_enabled_var=SearchState.genre_search_enabled,
                        state_enable_disable_fn=SearchState.toggle_genre_search
                    ),
                    switchable_input_field(
                        name='Year',
                        value=SearchState.search_year,
                        on_change=SearchState.set_search_year,
                        state_enabled_var=SearchState.year_search_enabled,
                        state_enable_disable_fn=SearchState.toggle_year_search
                    ),
                    param_slider(
                        text=f'Number of results: {SearchState.num_results}',
                        state_value_setter=SearchState.set_num_results,
                        default_value=NUM_SEARCH_RESULTS_DEFAULT,
                        min_max=[1,50]
                    )
                ),
            ),
            heading='Parameters'
        ),
        pane_button(
            text='Search', 
            on_click=SearchState.fetch_search_results(),
            is_disabled=SearchState.search_disabled
        ),
        rx.cond(
            SearchState.results_fetched,
            sub_pane_view(
                rx.vstack(
                    # rx.hstack(
                    #     sub_pane_button(
                    #         text='Play all',
                    #         on_click=State.play_all_recommended_tracks
                    #     ),
                    #     sub_pane_button(
                    #         text='Export to playlist',
                    #         on_click=PlaylistDialogState.change
                    #     ),
                    #     width='100%'
                    # ),
                    rx.foreach(
                        SearchState.search_result_tracks,
                        lambda x: track_card(
                            track=x,
                            show_genres=True,
                            genres_interactive=False,
                            artists_interactive=False,
                            buttons=[
                                track_multi_button(x)
                            ]
                        )
                    ),
                    width='100%'
                ), 
                heading='Results', 
                border_color=GREEN
            ),
            sub_pane_view(
                hint_text('search for something'),
                   
                heading='Results', 
            ),
        )
    )

def library_view() -> rx.Component:
    tabs = rx.tabs(
        rx.tab_list(
            rx.tab('Liked Songs'),
            rx.tab('Playlist'),
            rx.tab('Recently Played'),
        ),
        rx.tab_panels(
            rx.tab_panel(liked_songs_view_panel()),
            rx.tab_panel(playlist_browser_panel()),
            rx.tab_panel(recent_tracks_panel()),
        ),
    )
  
    return rx.box(
        tabs,
        width=400
    )
def pane_view(
        content: rx.component,
        heading_text: str,
        padding: int = 4
    ) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(
                heading_text,
                margin_left=4,
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
    
def sub_pane_button(
        text: str,
        on_click: callable,
        is_disabled: bool = False
    ):
    return rx.button(
        rx.text(text),
        on_click=on_click,
        size='md',
        is_disabled=is_disabled,
        width='100%'
    )

def pane_button(
        text: str,
        on_click: callable,
        is_disabled: bool = False
):
    return rx.button(
        text,
        on_click=on_click,
        is_disabled=is_disabled,
        width='100%',
        border_radius='xl'
    )


def recent_tracks_panel() -> rx.Component:
    return rx.vstack(
        sub_pane_button(
            text='See artist genres',
            on_click=State.fetch_genres_rp,
            is_disabled=State.rp_tracks_have_genre,
        ),
        rx.vstack(
            rx.foreach(
                State.rp_tracks,
                lambda x: track_card(
                                track=x,
                                show_genres=True,
                                artists_interactive=True,
                                buttons=[track_add_seed_button(x, source='recent')]
                            )
            ),
            width='100%'
        )
    )

def playlist_browser_panel() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.select(
                State.playlist_names,
                on_change=State.select_playlist,
            ),
            sub_pane_button(
                text='See artist genres',
                on_click=State.fetch_genres_selected_pl,
                is_disabled=State.selected_playlist.has_genres,
            )
        ),
        rx.foreach(
            State.selected_playlist_tracks,
            lambda x: track_card(
                            track=x,
                            show_genres=True,
                            artists_interactive=True,
                            buttons=[track_add_seed_button(x, source='playlist')]
                        ),
            width='100%'
        ),
        align_items='left',
    )

def liked_songs_view_panel() -> rx.Component:
    return rx.vstack(
        sub_pane_button(
            text='See artist genres',
            on_click=State.fetch_genres_liked,
            is_disabled=State.liked_tracks_have_genre,
        ),
        rx.vstack(
            rx.foreach(
                State.liked_tracks,
                lambda x: track_card(
                                track=x,
                                show_genres=True,
                                artists_interactive=True,
                                buttons=[track_add_seed_button(x, source='liked')]
                            )
            ),
            sub_pane_button(text='Load more', on_click=State.fetch_liked_tracks_batch),
            width='100%'
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
app.add_page(index, on_load=State.on_load_library_fetch)
app.compile()
