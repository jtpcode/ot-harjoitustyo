from tkinter import ttk, constants, StringVar
from services.magic_service import MagicService
from repositories.card_repository import card_repository
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
        self._card_search_entry = None
        self._all_sets = {}
        self._selected_set = None
        self._set_list_dropdown = None

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

    def _submit_handler(self):
        card_name = self._card_search_entry.get()
        set_code = self._all_sets[self._selected_set.get()]

        card = card_repository.fetch_card_by_name_and_set(card_name, set_code)
        print(card["name"])

    def initialize_sets(self):
        sets = card_repository.fetch_all_sets()

        # Form a dictionary that can be used for populating dropdown list with "name"
        # and also for fetching cards with "code" in _submit_handler
        self._all_sets = {set["name"]: set["code"] for set in sets["data"]}

    def initialize_label(self, top_frame):
        title_label = ttk.Label(
            master=top_frame,
            text="Magic Archive",
            font=("Arial", 14, "bold")
        )
        title_label.grid(
            row=0,
            column=0,
            padx=10,
            sticky=constants.NW
        )

    def initialize_card_search(self, center_frame):
        card_search_label = ttk.Label(master=center_frame, text="Card name : ")
        select_set_label = ttk.Label(master=center_frame, text="Set name : ")
        self._card_search_entry = ttk.Entry(master=center_frame, width=30)
        self._selected_set = StringVar(center_frame)
        self._set_list_dropdown = ttk.Combobox(
            master=center_frame,
            textvariable=self._selected_set,
            values=sorted(list(self._all_sets)),
            state="readonly",
            width=30
        )
        submit_button = ttk.Button(
            master=center_frame,
            text="Submit",
            command=self._submit_handler
        )

        card_search_label.grid(
            row=0,
            column=0,
            padx=5
        )
        self._card_search_entry.grid(
            row=0,
            column=1,
            padx=5
        )
        select_set_label.grid(
            row=1,
            column=0,
            padx=5,
            pady=(10, 5)
        )
        self._set_list_dropdown.grid(
            row=1,
            column=1,
            padx=5,
            pady=(10, 5),
            sticky=constants.W
        )
        submit_button.grid(
            row=1,
            column=2,
            padx=10,
            pady=(10, 5)
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
            sticky=constants.NE
        )

    def initialize_show_card(self, cards_frame):
        for i in range(10):
            card = ttk.Label(
                cards_frame, text=f"Magic card {i+1}", relief="solid", padding=5
            )
            card.pack(fill="x", pady=2)

    def _initialize(self):
        # Initialize dropdown menu for Set selection
        self.initialize_sets()

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
        top_frame.grid_columnconfigure(0, weight=1, minsize=170)
        top_frame.grid_columnconfigure(1, weight=2)
        top_frame.grid_columnconfigure(2, weight=1)

        # Center frame: card search options (in the middle of top frame)
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
        self.initialize_card_search(center_frame)
        self.initialize_logout(top_frame)
        self.initialize_show_card(cards_frame)
