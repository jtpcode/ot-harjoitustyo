from tkinter import ttk, constants
from services.magic_service import MagicService
from utils.ui_utils import center_window


class MagicCardView:
    """User interface for managing Magic the Gathering cards."""

    def __init__(self, root, show_login_view):
        """Class constructor. Creates a view for managing Magic the Gathering cards.

        Args:
            root:
                TKinter -element, which initializes the user interface.
            show_login_view:
                Direct user to "Login" view
        """

        self._root = root
        self._show_login_view = show_login_view
        self._frame = None
        self._card_input_entry = None

        center_window(self._root, 800, 800)
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

    def initialize_label(self, top_frame):
        title_label = ttk.Label(
            master=top_frame,
            text="Magic Archive",
            font=("Arial", 14, "bold")
        )
        title_label.grid(
            row=0,
            column=0,
            padx=(0, 10),
            sticky=constants.W
        )

    def initialize_card_input(self, center_frame):
        card_input_label = ttk.Label(master=center_frame, text="Card name: ")
        self._card_input_entry = ttk.Entry(master=center_frame, width=40)

        card_input_label.grid(
            row=0,
            column=0,
            padx=(5, 5)
        )
        self._card_input_entry.grid(
            row=0,
            column=1,
            padx=(5, 5)
        )

    def initialize_logout(self, top_frame):
        logout_button = ttk.Button(
            master=top_frame,
            text="Logout",
            command=self._logout_handler
        )

        logout_button.grid(
            row=0,
            column=2,
            padx=10,
            sticky=constants.E
        )

    def initialize_show_card(self, cards_frame):
        for i in range(10):
            card = ttk.Label(
                cards_frame, text=f"Magic card {i+1}", relief="solid", padding=5
            )
            card.pack(fill="x", pady=2)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_rowconfigure(1, weight=1)

        # Top frame: all the tools etc.
        top_frame = ttk.Frame(master=self._frame)
        top_frame.grid(
            row=0,
            column=0,
            pady=10,
            sticky=constants.EW
        )
        top_frame.grid_columnconfigure(0, weight=1, minsize=150)
        top_frame.grid_columnconfigure(1, weight=2)
        top_frame.grid_columnconfigure(2, weight=1)

        # Center frame: card input (label + entry)
        center_frame = ttk.Frame(top_frame)
        center_frame.grid(
            row=0,
            column=1,
            sticky=constants.EW
        )

        # Cards frame: show cards
        cards_frame = ttk.Frame(master=self._frame)
        cards_frame.grid(
            row=1,
            column=0,
            sticky=constants.NSEW,
            padx=10,
            pady=(0, 10)
        )

        self.initialize_label(top_frame)
        self.initialize_card_input(center_frame)
        self.initialize_logout(top_frame)
        self.initialize_show_card(cards_frame)
