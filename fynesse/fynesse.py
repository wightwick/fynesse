from fynesse.constants import APP_NAME
from rxconfig import config

import reflex as rx
from .constants import (
    CREATE_PLAYLIST_BUTTON_TEXT,
    GENERATE_RECOMMENDATIONS_BUTTON_TEXT,
    GERMINATE_HINT, 
    NUM_SEARCH_RESULTS_SLIDER_TEXT,
    PARAMETERS_SUB_PANE_HEADER_TEXT, 
    PLANT_SEEDS_HINT_TEXT,
    PLAY_ALL_TRACKS_BUTTON_TEXT,
    PLAYLIST_CREATE_DIALOG_HEADER_TEXT, 
    RESULTS_SUB_PANE_HEADER_TEXT, 
    SAVE_PLAYLIST_BUTTON_TEXT,
    SEARCH_HINT,
    SEARCH_RESULTS_TYPE_RADIO_TEXT,
    SEEDS_SUB_PANE_HEADER_TEXT,
    TARGET_ACOUSTICNESS_SLIDER_TEXT,
    TARGET_ENERGY_SLIDER_TEXT,
    TARGET_LIVENESS_SLIDER_TEXT,
    TOO_MANY_SEEDS_HEADER_TEXT
)
from .input import (
    param_slider,
    switchable_input_field,
    switchable_param_slider,
    track_add_seed_button,
    track_multi_button,
    track_play_button,
    track_queue_button,
    track_remove_seed_button
)
from .data import Track
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
        rx.flex(
            rx.heading(
                APP_NAME,
                size='3xl'
            ),
            rx.spacer(),
            rx.button(
                rx.icon(tag="moon"),
                on_click=rx.toggle_color_mode,
                size='sm',
                variant='ghost'
            ),
            width='100vw',
            padding_left=2,
            padding_right=2,
            align='center'
        ),
        margin_bottom=10,
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
                    html_width='100',
                    border_radius='md',
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

def artist_card_lg(
        artist: Artist,
        show_genres: bool=False,
    ):
    artist_uri_name = (artist.uri, artist.artist_name)

    return rx.box(
            rx.hstack(
                rx.image(
                    src_set=artist.images_srcset,
                    html_width='100',
                    border_radius='md'
                ),
                rx.vstack(
                    rx.box(
                        rx.text(
                            artist.artist_name,
                        ),
                        margin_top='0.5'
                    ),                    
                    rx.cond(
                        (artist.genres.length() > 0) & show_genres, 
                        rx.wrap(
                            rx.foreach(
                                artist.genres,
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
                rx.button(
                    '🌱',
                    on_click=State.add_artist_to_seeds(artist_uri_name),
                    is_disabled=State.seed_artist_uris.contains(artist_uri_name[0]),
                ),

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
                    margin_bottom='-12.5px',
                    margin_left=2,
                    z_index=2
                ),
                rx.box(
                    content,
                    border_width='medium',
                    border_radius='xl',
                    border_color=border_color,
                    padding=15,
                    # width=400,
                    z_index=1
                ),
                align_items='left'
            ),
            width='100%'
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
                hint_text(PLANT_SEEDS_HINT_TEXT),
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
                            State.seed_artists_uris_names,
                            lambda x: artist_card(x, False)
                        ),
                    ),
                    align_items='center'
                ),
            )
        )

def seeds_view() -> rx.Component:
    return rx.cond(
            State.too_many_seeds, 
            sub_pane_view(
                content=seeds_list(),
                heading=rx.text(TOO_MANY_SEEDS_HEADER_TEXT, color=SUB_PANE_WARNING_RED),
                border_color=SUB_PANE_WARNING_RED
            ),
            sub_pane_view(
                content=seeds_list(),
                heading=SEEDS_SUB_PANE_HEADER_TEXT,
            )

        )

def playlist_create_dialog(): 
    return rx.alert_dialog(
        rx.alert_dialog_overlay(
            rx.alert_dialog_content(
                rx.hstack(
                    rx.box(
                        rx.alert_dialog_header(
                            PLAYLIST_CREATE_DIALOG_HEADER_TEXT,
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
                        CREATE_PLAYLIST_BUTTON_TEXT,
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
                        TARGET_ACOUSTICNESS_SLIDER_TEXT,
                        state_value_setter=State.set_recc_target_acousticness_value,
                        state_enabled_var=State.recc_target_acousticness_enabled,
                        state_enable_disable_fn=State.enable_disable_recc_target_acousticness
                    ),
                    switchable_param_slider(
                        TARGET_ENERGY_SLIDER_TEXT,
                        state_value_setter=State.set_recc_target_energy_value,
                        state_enabled_var=State.recc_target_energy_enabled,
                        state_enable_disable_fn=State.enable_disable_recc_target_energy
                    ),
                    switchable_param_slider(
                        TARGET_LIVENESS_SLIDER_TEXT,
                        state_value_setter=State.set_recc_target_liveness_value,
                        state_enabled_var=State.recc_target_liveness_enabled,
                        state_enable_disable_fn=State.enable_disable_recc_target_liveness
                    ),
                    switchable_param_slider(
                        TARGET_DANCEABILITY_SLIDER_TEXT,
                        state_value_setter=State.set_recc_target_danceability_value,
                        state_enabled_var=State.recc_target_danceability_enabled,
                        state_enable_disable_fn=State.enable_disable_recc_target_danceability
                    ),
                    switchable_param_slider(
                        TARGET_INSTRUMENTALNESS_SLIDER_TEXT,
                        state_value_setter=State.set_recc_target_instrumentalness_value,
                        state_enabled_var=State.recc_target_instrumentalness_enabled,
                        state_enable_disable_fn=State.enable_disable_recc_target_instrumentalness
                    ),
                    param_slider(
                        text=f'{NUM_RECOMMENDED_TRACKS_SLIDER_TEXT}{State.num_recommendations}',
                        on_change=State.set_num_recommendations,
                        default_value=NUM_RECCOMENDATIONS_DEFAULT,
                        min_max=[1,100]
                    )
                ),

                heading=PARAMETERS_SUB_PANE_HEADER_TEXT
            ),
            pane_button(
                text=GENERATE_RECOMMENDATIONS_BUTTON_TEXT,
                on_click=State.fetch_recommendations(),
                is_disabled=State.too_many_seeds | State.too_few_seeds,
            ),
            rx.cond(
                State.recommendations_generated,
                sub_pane_view(
                    rx.vstack(
                        rx.hstack(
                            sub_pane_button(
                                text=PLAY_ALL_TRACKS_BUTTON_TEXT,
                                on_click=State.play_all_recommended_tracks
                            ),
                            sub_pane_button(
                                text=SAVE_PLAYLIST_BUTTON_TEXT,
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
                    heading=RESULTS_SUB_PANE_HEADER_TEXT, 
                    border_color=GREEN
                ),
                sub_pane_view(
                    rx.cond(
                        ~(State.too_few_seeds | State.too_many_seeds),
                        hint_text(GERMINATE_HINT),
                        rx.text('')
                    ),
                    heading=RESULTS_SUB_PANE_HEADER_TEXT, 
                ),
            ),
        ),
        playlist_create_dialog()
    )


def search_view():
    return rx.vstack(
        sub_pane_view(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text(SEARCH_RESULTS_TYPE_RADIO_TEXT),
                        rx.spacer(),
                        rx.radio_group(
                            rx.hstack(
                                rx.foreach(
                                    SEARCH_RESULTS_TYPE_OPTIONS,
                                    lambda option: rx.radio(option),
                                ),
                                spacing="2em",
                            ),
                            on_change=SearchState.set_search_results_type,
                            value=SearchState.search_results_type,
                            default_checked=True,
                        ),
                        width='100%',
                        padding_left=1,
                        padding_right=5,
                    ),
                    switchable_input_field(
                        name=SEARCH_ARTIST_FIELD_TEXT,
                        value=SearchState.search_artist,
                        on_change=SearchState.set_search_artist,
                        state_enabled_var=SearchState.artist_search_enabled,
                        state_toggle_fn=SearchState.toggle_artist_search,
                    ),
                    switchable_input_field(
                        name=SEARCH_TRACK_FIELD_TEXT,
                        value=SearchState.search_name,
                        on_change=SearchState.set_search_name,
                        state_enabled_var=SearchState.name_search_enabled,
                        state_toggle_fn=SearchState.toggle_name_search,
                    ),
                    switchable_input_field(
                        name=SEARCH_GENRE_FIELD_TEXT,
                        value=SearchState.search_genre,
                        on_change=SearchState.set_search_genre,
                        state_enabled_var=SearchState.genre_search_enabled,
                        state_toggle_fn=SearchState.toggle_genre_search,
                    ),
                    switchable_input_field(
                        name=SEARCH_YEAR_FIELD_TEXT,
                        value=SearchState.search_year,
                        on_change=SearchState.set_search_year,
                        state_enabled_var=SearchState.year_search_enabled,
                        state_toggle_fn=SearchState.toggle_year_search,
                    ),
                    param_slider(
                        text=f'{NUM_SEARCH_RESULTS_SLIDER_TEXT}{SearchState.num_results}',
                        on_change=SearchState.set_num_results,
                        default_value=NUM_SEARCH_RESULTS_DEFAULT,
                        min_max=[1,50]
                    )
                ),
            ),
            heading=PARAMETERS_SUB_PANE_HEADER_TEXT
        ),
        rx.cond(
            SearchState.results_fetched,
            sub_pane_view(
                rx.vstack(
                    rx.cond(
                        SearchState.search_results_type == SEARCH_RESULTS_TYPE_TRACKS,
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
                        rx.vstack(
                            rx.foreach(
                                SearchState.artist_results,
                                lambda x: artist_card_lg(x, show_genres=True)
                            ),
                        ),
                    ),
                    sub_pane_button(text=LOAD_MORE_BUTTON_TEXT, on_click=SearchState.fetch_more_search_results, is_disabled=~SearchState.more_results_exist),
                    width='100%'
                ),
                heading=RESULTS_SUB_PANE_HEADER_TEXT, 
                border_color=GREEN
            ),
            sub_pane_view(
                hint_text(SEARCH_HINT),
                   
                heading=RESULTS_SUB_PANE_HEADER_TEXT, 
            ),
        )
    )

def library_view() -> rx.Component:
    tabs = rx.tabs(
        rx.tab_list(
            rx.tab(LIKED_SONGS_TAB_NAME_TEXT),
            rx.tab(PLAYLIST_TAB_NAME_TEXT),
            rx.tab(RECENTLY_PLAYED_TAB_NAME_TEXT),
            rx.tab(TOP_TAB_NAME_TEXT),
        ),
        rx.tab_panels(
            rx.tab_panel(liked_songs_view_panel()),
            rx.tab_panel(playlist_browser_panel()),
            rx.tab_panel(recent_tracks_panel()),
            rx.tab_panel(top_tracks_panel())
        ),
        color_scheme='green',
        align='center'
    )
  
    return rx.box(
        tabs,
        width=410
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
                margin_left='19px',
                margin_bottom=-4,
                z_index=2,
            ),
            rx.box(
                content,
                border_width='thick',
                border_radius='3xl',
                padding=padding,
                z_index=1,
            ),
            align_items='left'
        ),
        margin_left=2,
        margin_right=2,
        width=420
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
            text=ARTIST_GENRES_BUTTON_TEXT,
            on_click=State.fetch_genres_recent_tracks,
            is_disabled=State.recent_tracks_have_genre,
        ),
        rx.vstack(
            rx.foreach(
                State.recent_tracks,
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

def top_tracks_panel() -> rx.Component:
    return rx.vstack(
        sub_pane_button(
            text=ARTIST_GENRES_BUTTON_TEXT,
            on_click=State.fetch_genres_top_tracks,
            is_disabled=State.top_tracks_have_genre,
        ),
        rx.vstack(
            rx.foreach(
                State.top_tracks,
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
                text=ARTIST_GENRES_BUTTON_TEXT,
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
            text=ARTIST_GENRES_BUTTON_TEXT,
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
            sub_pane_button(text=LOAD_MORE_BUTTON_TEXT, on_click=State.fetch_liked_tracks_batch),
            width='100%'
        ),
    )

def index() -> rx.Component:
    return rx.container(
            rx.vstack(
                header_bar(),
                rx.flex(
                    rx.spacer(),
                    pane_view(library_view(), LIBRARY_PANE_HEADER_TEXT, padding=None),
                    rx.spacer(),
                    pane_view(recommendations_view(), RECOMMENDATIONS_PANE_HEADER_TEXT),
                    rx.spacer(),
                    pane_view(search_view(), SEARCH_PANE_HEADER_TEXT),
                    rx.spacer(),
                    width='100vw'
                ),
                # width='100vw'

            ),
            # width='100vw'
    )

# Add state and page to the app.
app = rx.App()
app.add_page(index, on_load=State.on_load_library_fetch)
app.compile()
