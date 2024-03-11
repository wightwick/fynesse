
"""
Reusable input components: 
Buttons, sliders, fields
"""
from ..data import Track
from ..state import State

import reflex as rx

def switchable_text_input(
        name: str,
        value: callable,
        on_change: callable,
        state_enabled_var: callable,
        state_toggle_fn: callable,
    ) -> rx.Component:
    """Input field with a title displayed above uit and a switch to
    enable/disable it
    """ 
    return rx.chakra.vstack(
        rx.chakra.text(
            name,
            margin_bottom=-3.5,
            margin_left=1,
            opacity=rx.cond(state_enabled_var, 1, 0.3),
            z_index=2,
        ),
        rx.chakra.hstack(
            rx.debounce_input(
                rx.chakra.input(
                    value=value,
                    on_change=on_change,
                    is_disabled=~state_enabled_var,
                ),
                debounce_timeout=300
            ),
            rx.chakra.switch(
                is_checked=state_enabled_var,
                on_change=state_toggle_fn,
                color_scheme='green'
            ),
            z_index=1
        ),
        align_items='left',
        width='100%'
    )

def clickable_tooltip(text: str) -> rx.Component:
    return rx.chakra.popover(
        rx.chakra.popover_trigger(
            rx.chakra.icon(
                tag='question_outline'
            ),
        ),
        rx.chakra.popover_content(
            rx.chakra.popover_body(text),
            rx.chakra.popover_close_button(),
            padding_top=5
        ),
    )

def switchable_param_slider(
        param_name: str,
        value_setter: callable,
        enabled_var: callable,
        enable_disable_fn: callable,
        value: rx.var,
        hint: str = None,
        min_val: int = 0,
        max_val: int = 100
    ) -> rx.Component:
    """Slider with a title displayed above it and a switch
    to enable/disable it
    """
    return rx.chakra.box(
        rx.chakra.vstack(
            rx.chakra.hstack(
                rx.cond(enabled_var,
                    rx.chakra.hstack(
                        rx.chakra.text(param_name + ':', as_='b'),
                        rx.chakra.text(value),
                    ),
                    rx.chakra.text(param_name, as_='b'),
                ),
                clickable_tooltip(
                    hint,
                ),
                rx.chakra.switch(
                    is_checked=enabled_var,
                    on_change=enable_disable_fn,
                    color_scheme='green'
                )

            ),
            rx.chakra.slider(
                    # value=initial_value,
                    default_value=0,
                    is_disabled=~enabled_var,
                    on_change_end=value_setter,
                    min_=min_val,
                    max_=max_val,
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
    ) -> rx.Component:
    """Slider with a title displayed above it"""
    return rx.chakra.box(
        rx.chakra.vstack(
            rx.chakra.text(
                text,
                as_='b'
            ),
            rx.chakra.slider(
                    default_value=default_value,
                    on_change_end=on_change,
                    min_=min_max[0],
                    max_=min_max[1],
                    color_scheme='green',
            ),
            align_items='left'
        ),
        width='100%'
    )


def track_queue_button(track: Track) -> rx.Component:
    return rx.chakra.button(
        rx.chakra.vstack(
            rx.chakra.icon(tag='small_add'),
            rx.chakra.icon(tag='hamburger'),
            spacing='-1'
        ),
        on_click=State.queue_track_uri(track.uri),
     )


def track_play_button(track: Track) -> rx.Component:
    icon = rx.chakra.box(
        rx.chakra.icon(tag='triangle_down'),
        transform='rotate(-90deg)'
    )
    return rx.cond(
        State.active_device_exists,
        rx.chakra.button(
            icon,
            on_click=State.play_track_uris([track.uri]),
        ),
        rx.chakra.button(
            icon,
            on_click=rx.redirect(track.spotify_url, external=True)
        )
    )


def track_add_seed_button(track: Track, source: str) -> rx.Component:
    return rx.chakra.button(
        '🌱',
        on_click=State.add_track_uri_to_seeds(track.uri, source),
        is_disabled=State.seed_track_uris.contains(track.uri),
    )


def track_multi_button(track: Track) -> rx.Component:
    """Button to show popover with options to add seed, play, queue"""
    return rx.chakra.popover(
        rx.chakra.popover_trigger(
            rx.chakra.button(
                rx.chakra.icon(tag='triangle_down'),
                # on_click=State.queue_track_uri(track.uri),
            )
        ),
        rx.chakra.popover_content(
            rx.chakra.popover_header(height=8),
            rx.chakra.popover_body(
                rx.chakra.vstack(
                    track_add_seed_button(track, source='search'),
                    track_play_button(track),
                    track_queue_button(track),
                )
            ),
            rx.chakra.popover_close_button(),
            width='30'
        ),
    )


def track_remove_seed_button(track: Track) -> rx.Component:
    return rx.chakra.button(
        rx.chakra.icon(tag="minus"),
        on_click=State.remove_track_uri_from_seeds(track.uri),
    )


def pane_button(
        text: str,
        **kwargs
) -> rx.Component:
    """Button with larger corner radius styled for use in a pane"""
    return rx.chakra.button(
        text,
        width='100%',
        border_radius='xl',
        **kwargs
    )


def sub_pane_button(
        text: str,
        **kwargs
    ) -> rx.Component:
    """Button with smaller corner radius styled for use in a sub pane"""
    return rx.chakra.button(
        rx.chakra.text(text),
        size='md',
        width='100%',
        **kwargs
    )