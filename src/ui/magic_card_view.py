from tkinter import ttk, StringVar, constants
from services.magic_service import MagicService

class MagicCardView:
    """User interface for managing Magic the Gathering cards."""

    def __init__(self, root, show_login_view):
        """Class constructor. Creates a view for managing Magic the Gathering cards.

        Args:
            root:
                TKinter -element, which initializes the user interface.
            show_login_view:
                Direct user to login view
        """

        self._root = root
        self._show_login_view = show_login_view
        self._frame = None

        # Center the window
        self._height = 500
        self._width = 500
        x = (self._root.winfo_screenwidth() // 2) - (self._width // 2)
        y = (self._root.winfo_screenheight() // 2) - (self._height // 2)
        self._root.geometry(f'{self._width}x{self._height}+{x}+{y}')

        self._initialize()

    def pack(self):
        """Show current view."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Destroy current view."""
        self._frame.destroy()
    
    def _logout_handler(self):
        magic_service = MagicService()
        magic_service.logout()
        self._show_login_view()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        title_label = ttk.Label(
            master=self._frame,
            text="Magic Archive",
            font=("Arial", 14, "bold"),
        )
        title_label.grid(
            padx=5,
            pady=5,
            column=0,
            row=0,
            sticky=constants.W
        )

        logout_button = ttk.Button(
            master=self._frame,
            text="Logout",
            command=self._logout_handler
        )

        logout_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky=constants.E
        )
