from spotifind.data import Track
from spotifind.state import State

import reflex as rx


def switchable_input_field(
        name: str,
        value: callable,
        on_change: callable,
        state_enabled_var: callable,
        state_toggle_fn: callable,
    ):
    
    return rx.vstack(
        rx.text(
            name,
            margin_bottom=-3.5,
            margin_left=1,
            opacity=rx.cond(state_enabled_var, 1, 0.3)
        ),
        rx.hstack(
            rx.debounce_input(
                rx.input(
                    value=value,
                    on_change=on_change,
                    is_disabled=~state_enabled_var,
                ),
                debounce_timeout=300
            ),
            rx.switch(
                is_checked=state_enabled_var,
                on_change=state_toggle_fn,
                color_scheme='green'
            )
        ),
        align_items='left',
        width='100%'
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
                    on_change=state_enable_disable_fn,
                    color_scheme='green'
                )

            ),
            rx.slider(
                    # value=initial_value,
                    default_value=0,
                    is_disabled=~state_enabled_var,
                    on_change=state_value_setter,
                    min_=0,
                    max_=100,
                    color_scheme='green',
            ),
            align_items='left'
        ),
        width='100%'
    )


def param_slider(
        text: str,
        on_change: callable,
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
                    on_change=on_change,
                    min_=min_max[0],
                    max_=min_max[1],
                    color_scheme='green',
            ),
            align_items='left'
        ),
        width='100%'
    )


def track_queue_button(track: Track) -> rx.Component:
    return rx.button(
        rx.icon(tag='plus_square'),
        on_click=State.queue_track_uri(track.uri),
     )


def track_play_button(track: Track) -> rx.Component:
    return rx.button(
        rx.box(
            rx.icon(tag='triangle_down'),
            transform='rotate(-90deg)'
        ),
        on_click=State.play_track_uris([track.uri]),
    )


def track_add_seed_button(track: Track, source: str) -> rx.Component:
    return rx.button(
        '🌱',
        on_click=State.add_track_uri_to_seeds(track.uri, source),
        is_disabled=State.seed_track_uris.contains(track.uri),
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


def track_remove_seed_button(track: Track) -> rx.Component:
    return rx.button(
        rx.icon(tag="minus"),
        on_click=State.remove_track_uri_from_seeds(track.uri),
    )