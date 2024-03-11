"""
Main app script
"""
import reflex as rx

from .components.display import pane
from .views import *

from .state import *
from .constants import *

@rx.page(
    title=APP_NAME,
    description=APP_DESCRIPTION,
)
def index() -> rx.Component:
    return rx.chakra.container(
            rx.chakra.vstack(
                rx.chakra.box(
                    rx.cond(
                        State.app_is_authenticated,
                        rx.chakra.box(
                            on_mount=rx.redirect('/')
                            ), # clear url after auth
                        authenticate_alert(),
                    ),
                    width='60vw',
                    height='0vh'
                ),
                rx.chakra.vstack(
                    header_bar(),
                    rx.chakra.flex(
                        rx.chakra.spacer(),
                        pane(library_view(), LIBRARY_PANE_HEADER_TEXT, padding=None),
                        rx.chakra.spacer(),
                        pane(recommendations_view(), RECOMMENDATIONS_PANE_HEADER_TEXT),
                        rx.chakra.spacer(),
                        pane(search_view(), SEARCH_PANE_HEADER_TEXT),
                        rx.chakra.spacer(),
                        width='100vw'
                    ),
                    rx.chakra.spacer(),
                    footer(),
                    opacity=rx.cond(State.app_is_authenticated, 1, 0.3),
                    height='100%'
                ),
                height='100vh'
            )
    )

app = rx.App()
app.add_page(index, on_load=State.on_load)
