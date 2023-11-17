"""
Main app script
"""
import reflex as rx

from .components.display import pane
from .views import *

from .state import *
from .constants import *

def index() -> rx.Component:
    return rx.container(
            rx.vstack(
                rx.cond(
                    ~State.app_is_authenticated,
                    rx.alert(
                        rx.alert_icon(),
                        rx.alert_title(AUTHENTICATE_DIALOG_HEADER_TEXT),
                        rx.alert_description(
                            rx.button(
                                AUTHENTICATE_BUTTON_TEXT,
                                on_click=rx.redirect(
                                    State.spotify_auth_url,
                                    external=True,
                                ),
                            ),
                        ),
                        status='error',
                    ),
                    rx.box()
                ),
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
            ),
    )

@rx.page(route='/sp_redirect')
def post():
    return rx.center(
        rx.text(State.callback_code_and_state)
    )

app = rx.App()
app.add_page(index, on_load=State.on_load)
app.compile()
