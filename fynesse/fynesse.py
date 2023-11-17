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
    return rx.container(
            rx.vstack(
                rx.box(
                    rx.cond(
                        State.app_is_authenticated,
                        rx.box(on_mount=rx.redirect('/')), # clear url after auth
                        authenticate_alert(),
                    ),
                    width='60vw'
                ),
                rx.vstack(
                    header_bar(),
                    rx.flex(
                        rx.spacer(),
                        pane(library_view(), LIBRARY_PANE_HEADER_TEXT, padding=None),
                        rx.spacer(),
                        pane(recommendations_view(), RECOMMENDATIONS_PANE_HEADER_TEXT),
                        rx.spacer(),
                        pane(search_view(), SEARCH_PANE_HEADER_TEXT),
                        rx.spacer(),
                        width='100vw'
                    ),
                    opacity=rx.cond(State.app_is_authenticated, 1, 0.3)
                ),
            )
    )

app = rx.App()
app.add_page(index, on_load=State.on_load)
app.compile()
