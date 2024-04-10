"""
Generic components for displaying information
"""
from fynesse.data import Track
from fynesse.state import Artist, SearchState, State, Track
from fynesse.constants import *

import reflex as rx


def genre_card(genre: str) -> rx.Component:
    """Small card showing genre name. Button displayed to right of name
    to bring the genre into the search field
    """
    return rx.chakra.box(
        rx.chakra.hstack(
            rx.chakra.text('#' + genre, as_='small'),
                rx.chakra.button(
                    rx.chakra.icon(tag="search"),
                    on_click=SearchState.stage_genre_for_search(genre),

                    size='xs',
                    variant='ghost'
                ),
            ),
        border_radius='lg',
        border_width='thin',
        padding_left='6px'
    )


def artist_card(
        artist_uri_name: list[str],
        add_remove_button: bool
    ) -> rx.Component:
    """Small card showing artist's name. If add_remove_button, add to seeds
    button displayed; otherwise remove from seeds button displayed
    """
    return rx.chakra.box(
        rx.chakra.hstack(
            rx.chakra.text(artist_uri_name.__getitem__(1)),
            rx.cond(
                add_remove_button,
                rx.chakra.button(
                    '🌱',
                    on_click=State.add_artist_to_seeds(artist_uri_name),
                    is_disabled=State.seed_artist_uris.contains(
                        artist_uri_name.__getitem__(0)
                    ),
                    size='xs',
                    variant='ghost'
                ),
                rx.chakra.button(
                    rx.chakra.icon(tag="minus"),
                    on_click=State.remove_artist_from_seeds_by_uri(
                        artist_uri_name.__getitem__(0)
                    ),
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
    """Card showing information about a track. Always shows name, artist name,
    album name. Genres clickable (if genres_interactive) otherwise displayed as 
    comma-separated text. Artists can be clickable to add seed (if
    artists_interactive) otherwise displayed as comma separated text. Buttons
    passed in via buttons are rendered in a vertical stack
    """
    return rx.chakra.box(
            rx.vstack(
                rx.chakra.hstack(
                    rx.chakra.image(
                        src_set=track.album_art_srcset,
                        html_width='100',
                        padding=1.5
                    ),
                    rx.chakra.vstack(
                        rx.chakra.box(
                            rx.chakra.text(
                                track.track_name,
                                as_='strong'
                            ),
                            margin_top=0.5,
                        ),
                        rx.cond(
                            artists_interactive,
                            rx.chakra.wrap(
                                rx.foreach(
                                    track.artist_uris_names,
                                    lambda x: rx.chakra.wrap_item(artist_card(x, True))
                                ),
                            ),
                            rx.chakra.text(track.artist_names.join(', '))
                        ),
                        rx.chakra.box(
                            rx.chakra.text(
                                track.album_name,
                                as_='small'
                            ),
                        ),

                        rx.cond(
                            (track.artist_genres.length() > 0) & show_genres,
                            rx.cond(
                                genres_interactive,
                                rx.chakra.wrap(
                                    rx.foreach(
                                        track.artist_genres,
                                        #lambda x: rx.chakra.box(x, border_radius='xl', border_width='thin')
                                        lambda x: rx.chakra.wrap_item(genre_card(x))
                                    ),
                                    padding_bottom='1.5'
                                ),
                                rx.chakra.text('#' + track.artist_genres.join(', #'), as_='small')
                            ),
                            rx.chakra.text('')
                        ),
                        text_align='left',
                        align_items='left',
                    ),
                    rx.chakra.spacer(),
                    rx.chakra.vstack(*buttons),
                    margin_right=3
            ),
            spotify_link_card_bottom_bar(link_url=track.track_url),
            spacing='0'
        ),
        border_width=2,
        border_radius='lg',
        overflow='hidden',
        # padding_right=3,
        width='100%',
            
    )


def artist_card_lg(
        artist: Artist,
        show_genres: bool=False,
    ):
    """Large artist card for display in search results. Shows name,
    artist image, clickable artist genres (if show_genres
    """
    return rx.chakra.box(
            rx.chakra.vstack(
                rx.chakra.hstack(
                    rx.chakra.image(
                        src_set=artist.images_srcset,
                        html_width='100',
                        border_radius='md'
                    ),
                    rx.chakra.vstack(
                        rx.chakra.box(
                            rx.chakra.text(
                                artist.artist_name,
                            ),
                            margin_top=0.5
                        ),
                        rx.cond(
                            (artist.genres.length() > 0) & show_genres,
                            rx.chakra.wrap(
                                rx.foreach(
                                    artist.genres,
                                    #lambda x: rx.chakra.box(x, border_radius='xl', border_width='thin')
                                    lambda x: rx.chakra.wrap_item(genre_card(x))
                                ),
                                padding_bottom='1.5'
                            ),
                            rx.chakra.text('')
                        ),
                        align_items='left',
                    ),
                    rx.chakra.spacer(),
                    rx.chakra.button(
                        '🌱',
                        on_click=State.add_artist_to_seeds([artist.uri, artist.artist_name]),
                        is_disabled=State.seed_artist_uris.contains(artist.uri),
                        margin_right=3
                    ),
            ),
            spotify_link_card_bottom_bar(artist.artist_url)
        ),
        border_width=2,
        border_radius='lg',
        overflow='hidden',
        width='100%',
    )


def spotify_link_card_bottom_bar(link_url: str) -> rx.Component:
        return rx.vstack(    
            rx.box(
                width='100%',
                height=0,
                border_width=0.5,
            ),
            rx.center(
                rx.chakra.button(
                    rx.chakra.hstack(
                        rx.text(
                            LISTEN_ON_SPOTIFY_TEXT,
                            size='1',
                            weight='regular'
                        ),
                        rx.color_mode_cond(
                            light=rx.chakra.image(src='Spotify_Icon_RGB_Black.png', height='12px'),
                            dark=rx.chakra.image(src='Spotify_Icon_RGB_White.png', height='12px'),
                        ),
                        align='center',
                        width='100%',
                        opacity=0.7,
                        spacing='1'
                    ),
                    width='100%',
                    height=5,
                    border_radius=0,
                    variant='ghost',
                    padding_left=2.5,
                    on_click=rx.redirect(
                        link_url,
                        external=True
                    )
                ),
                width='100%',
            ),
            spacing='0',
            width='100%'
        )


def pane(
        children: rx.Component,
        heading_text: str,
        padding: int = 4
    ) -> rx.Component:
    """Top-level view; displays arbitrary children with a text heading"""
    return rx.chakra.box(
        rx.chakra.vstack(
            rx.chakra.heading(
                heading_text,
                margin_left='19px',
                margin_bottom=-4,
                z_index=2,
            ),
            rx.chakra.box(
                children,
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


def sub_pane(
        children: rx.Component,
        heading: str,
        border_color: str = None,
        width='100%',
        **kwargs
    ) -> rx.Component:
    """Second-level view; displays arbitrary children with a text heading"""
    return rx.chakra.box(
            rx.chakra.vstack(
                rx.chakra.heading(
                    heading,
                    size='md',
                    margin_bottom='-12.5px',
                    margin_left=2,
                    z_index=2
                ),
                rx.chakra.box(
                    children,
                    border_width='medium',
                    border_radius='xl',
                    border_color=border_color,
                    padding=15,
                    # width=400,
                    z_index=1
                ),
                align_items='left'
            ),
            width=width,
            **kwargs
        )


def hint_text(text: str) -> rx.Component:
    return rx.chakra.text(
        text,
        opacity=0.3,
        text_align='center',
    )

def spotify_image_link(dark_mode: bool) -> rx.Component:
    img_src = 'Spotify_Logo_RGB_White.png' if dark_mode\
        else 'Spotify_Logo_RGB_Black.png'
    return rx.chakra.link(
        rx.chakra.image(src=img_src, height='21px'),
        href='https://open.spotify.com'
    )

def footer() -> rx.Component:
    return rx.chakra.center(
        rx.chakra.hstack(
            rx.chakra.text('all track, artist and genre information from'),
            rx.color_mode_cond(
                light=spotify_image_link(dark_mode=False),
                dark=spotify_image_link(dark_mode=True)
            )
        ),
        height=50,
        border_top_width='thin',
        width='100%',
        padding=8,
        padding_bottom=35,
        align='center'
    )
