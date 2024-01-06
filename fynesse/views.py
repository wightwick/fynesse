"""
Components that display specific information
"""
from fynesse.components.display import *
from fynesse.components.input import *
from fynesse.constants import *
from fynesse.state import PlaylistDialogState, SearchState, State

import reflex as rx


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


def library_view() -> rx.Component:
    tabs = rx.tabs(
        rx.tab_list(
            rx.tab(LIKED_SONGS_TAB_NAME_TEXT),
            rx.tab(PLAYLIST_TAB_NAME_TEXT),
            rx.tab(RECENTLY_PLAYED_TAB_NAME_TEXT),
            rx.tab(TOP_TAB_NAME_TEXT),
            # spacing=10
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
        width='100%',
        min_width=370
    )


def search_view():
    return rx.vstack(
        sub_pane(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text(SEARCH_RESULTS_TYPE_RADIO_TEXT),
                        rx.spacer(),
                        rx.radio_group(
                            rx.hstack(
                                rx.foreach(
                                    SEARCH_RESULTS_TYPE_OPTIONS,
                                    lambda option: rx.radio(
                                        option,
                                        color_scheme='green'
                                    ),
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
                    switchable_text_input(
                        name=SEARCH_ARTIST_FIELD_TEXT,
                        value=SearchState.search_artist,
                        on_change=SearchState.set_search_artist,
                        state_enabled_var=SearchState.artist_search_enabled,
                        state_toggle_fn=SearchState.toggle_artist_search,
                    ),
                    switchable_text_input(
                        name=SEARCH_TRACK_FIELD_TEXT,
                        value=SearchState.search_name,
                        on_change=SearchState.set_search_name,
                        state_enabled_var=SearchState.name_search_enabled,
                        state_toggle_fn=SearchState.toggle_name_search,
                    ),
                    switchable_text_input(
                        name=SEARCH_GENRE_FIELD_TEXT,
                        value=SearchState.search_genre,
                        on_change=SearchState.set_search_genre,
                        state_enabled_var=SearchState.genre_search_enabled,
                        state_toggle_fn=SearchState.toggle_genre_search,
                    ),
                    switchable_text_input(
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
            sub_pane(
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
                border_color=SPOTIFY_GREEN
            ),
            sub_pane(
                hint_text(SEARCH_HINT),

                heading=RESULTS_SUB_PANE_HEADER_TEXT,
            ),
        ),
        min_width=320
    )


def seeds_list() -> rx.Component:
    return rx.box(
            rx.cond(State.too_few_seeds,
                rx.center(
                    rx.hstack(
                        hint_text(PLANT_SEEDS_HINT_TEXT),
                        rx.text('🌱', opacity=0.7)
                    ),
                ),
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
            sub_pane(
                children=seeds_list(),
                heading=rx.text(TOO_MANY_SEEDS_HEADER_TEXT, color=SUB_PANE_WARNING_RED),
                border_color=SUB_PANE_WARNING_RED
            ),
            sub_pane(
                children=seeds_list(),
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
                    rx.debounce_input(
                        rx.input(
                            placeholder='name',
                            on_change=PlaylistDialogState.set_pl_name,
                        ),
                        debounce_timeout=100
                    )
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
            sub_pane(
                children=rx.vstack(
                    switchable_param_slider(
                        TARGET_ACOUSTICNESS_SLIDER_TEXT,
                        value_setter=State.set_recc_target_acousticness_value,
                        enabled_var=State.recc_target_acousticness_enabled,
                        enable_disable_fn=State.enable_disable_recc_target_acousticness,
                        value=State.recc_target_acousticness_value,
                        hint=ACOUSTICNESS_DESC_TEXT
                    ),
                    switchable_param_slider(
                        TARGET_ENERGY_SLIDER_TEXT,
                        value_setter=State.set_recc_target_energy_value,
                        enabled_var=State.recc_target_energy_enabled,
                        enable_disable_fn=State.enable_disable_recc_target_energy,
                        value=State.recc_target_energy_value,
                        hint=ENERGY_DESC_TEXT
                    ),
                    switchable_param_slider(
                        TARGET_LIVENESS_SLIDER_TEXT,
                        value_setter=State.set_recc_target_liveness_value,
                        enabled_var=State.recc_target_liveness_enabled,
                        enable_disable_fn=State.enable_disable_recc_target_liveness,
                        value=State.recc_target_liveness_value,
                        hint=LIVENESS_DESC_TEXT
                    ),
                    switchable_param_slider(
                        TARGET_DANCEABILITY_SLIDER_TEXT,
                        value_setter=State.set_recc_target_danceability_value,
                        enabled_var=State.recc_target_danceability_enabled,
                        enable_disable_fn=State.enable_disable_recc_target_danceability,
                        value=State.recc_target_danceability_value,
                        hint=DANCEABILITY_DESC_TEXT
                    ),
                    switchable_param_slider(
                        TARGET_INSTRUMENTALNESS_SLIDER_TEXT,
                        value_setter=State.set_recc_target_instrumentalness_value,
                        enabled_var=State.recc_target_instrumentalness_enabled,
                        enable_disable_fn=State.enable_disable_recc_target_instrumentalness,
                        value=State.recc_target_instrumentalness_value,
                        hint=INSTRUMENTALNESS_DESC_TEXT
                    ),
                    rx.flex(
                        rx.hstack(
                        rx.text(
                                TARGET_TEMPO_INPUT_TEXT,
                                as_='b'
                            ),
                            rx.switch(
                                is_checked=State.recc_target_tempo_enabled,
                                on_change=State.enable_disable_recc_target_tempo,
                                color_scheme='green'
                            ),
                        ),
                        rx.spacer(),
                        rx.debounce_input(
                            rx.input(
                                value=State.recc_target_tempo_value.to_string(),
                                on_change=State.set_recc_target_tempo_value,
                                type_='number',
                                width='4em',
                                is_disabled=~State.recc_target_tempo_enabled,
                            ),
                            debounce_timeout=300
                        ),
                        text_align='left',
                        align='center',
                        width='100%'
                    ),
                    # rx.debounce_input(
                    #     rx.input(
                    #         value=value,
                    #         on_change=on_change,
                    #         is_disabled=~state_enabled_var,
                    #     ),
                    #     debounce_timeout=300
                    # ),

                    # switchable_param_slider(
                    #     TARGET_TEMPO_INPUT_NAME,
                    #     state_value_setter=State.set_recc_tempo_value,
                    #     state_enabled_var=State.recc_tempo_enabled,
                    #     state_enable_disable_fn=State.enable_disable_recc_tempo,
                    #     hint=TEMPO_DESC_TEXT,
                    #     min_val=0,
                    #     max_val=250
                    # ),
                    # rx.box(
                    #     rx.debounce_input(

                    #         rx.number_input(
                    #             default_value=140,
                    #             on_change=State.set_recc_tempo_value,
                    #             allow_mouse_wheel=True
                    #         ),
                    #         debounce_timeout=300
                    #     ),
                    # ),
                    # switchable_number_input(
                    #     TARGET_TEMPO_INPUT_NAME,
                    #     value=State.recc_tempo_value,
                    #     on_change=State.set_recc_tempo_value,
                    #     state_toggle_fn=State.enable_disable_recc_tempo,
                    #     state_enabled_var=State.recc_tempo_enabled
                    # ),

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
                sub_pane(
                    rx.vstack(
                        rx.hstack(
                            rx.cond(
                                State.active_device_exists,
                                sub_pane_button(
                                    text=PLAY_ALL_TRACKS_BUTTON_TEXT,
                                    on_click=State.play_all_recommended_tracks
                                ),
                                rx.popover(
                                    rx.popover_trigger(
                                        sub_pane_button(
                                            text=PLAY_ALL_TRACKS_BUTTON_TEXT,
                                        )
                                    ),
                                    rx.popover_content(
                                        rx.popover_header("active spotify device required to play multiple tracks"),
                                        rx.popover_close_button(),
                                    ),
                                )
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
                    border_color=SPOTIFY_GREEN,
                ),
                sub_pane(
                    rx.cond(
                        ~(State.too_few_seeds | State.too_many_seeds),
                        hint_text(GERMINATE_HINT),
                        rx.text('')
                    ),
                    heading=RESULTS_SUB_PANE_HEADER_TEXT,
                ),
            ),
            min_width=320
        ),
        playlist_create_dialog(),
    )

def active_device_view() -> rx.Component:

    return rx.text(
        rx.cond(
            State.active_device_exists,
            ACTIVE_DEVICE_NAME_TEXT + State.active_device_name,
            NO_ACTIVE_DEVICES_TEXT
        )
    )

def header_bar() -> rx.Component:
    return rx.center(
        rx.flex(
            rx.hstack(
                rx.heading(
                    'fy',
                    size='3xl',
                    color=SPOTIFY_GREEN
                ),
                rx.heading(
                    'nesse',
                    size='3xl'
                ),
                spacing='0'
            ),
            rx.spacer(min_width=10),
            active_device_view(),
            rx.spacer(min_width=10),
            rx.button(
                rx.color_mode_cond(
                    light=rx.hstack(
                        rx.text('dark'),
                        rx.icon(tag='moon')
                    ),
                    dark=rx.hstack(
                        rx.text('light'),
                        rx.icon(tag='sun')
                    ),
                ),
                on_click=rx.toggle_color_mode,
                size='sm',
                # variant='ghost'
            ),
            width='100vw',
            padding_left=4,
            padding_right=4,
            align='center'
        ),
        margin_bottom=10,
    )

def authenticate_alert() -> rx.Component:
    return rx.alert(
        rx.alert_icon(),
        rx.alert_title(AUTHENTICATE_DIALOG_HEADER_TEXT, width='100%'),
        rx.alert_description(
            rx.hstack(
                rx.spacer(),
                rx.button(
                    AUTHENTICATE_BUTTON_TEXT,
                    on_click=rx.redirect(
                        State.spotify_auth_url,
                        external=False,
                    ),
                ),
            ),
            width='100%'
        ),
        status='error',
        border_radius='lg',
        z_index=2
    )