from ui.login_view import LoginView
from ui.create_user_view import CreateUserView
from ui.magic_card_view import MagicCardView


class UI:
    """Class for the graphical user interface of the application."""

    def __init__(self, root):
        """Class constructor. Creates a new class for the user interface.

        Args:
            root:
                TKinter -element, which initializes the user interface.
        """
        self._root = root
        self._current_view = None

    def start(self):
        """Starts the user interface."""
        self._show_login_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_login_view(self):
        self._hide_current_view()

        self._current_view = LoginView(
            self._root,
            self._show_create_user_view,
            self._show_magic_card_view
        )

        self._current_view.pack()

    def _show_create_user_view(self):
        self._hide_current_view()

        self._current_view = CreateUserView(
            self._root
        )

        self._current_view.pack()

    def _show_magic_card_view(self):
        self._hide_current_view()

        self._current_view = MagicCardView(
            self._root
        )

        self._current_view.pack()
