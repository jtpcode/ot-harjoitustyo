from tkinter import ttk, constants, StringVar
from ttkwidgets.autocomplete import AutocompleteCombobox
from services.magic_service import MagicService, CardExistsError
from repositories.card_repository import card_repository
from utils.ui_utils import center_window


class MagicCardView:
    """User interface for managing 'Magic the Gathering' cards.

    Attributes:
        root:
            TKinter -element, which initializes the user interface.
        show_login_view:
            Direct user to "Login" view.
    """

    def __init__(self, root, show_login_view):
        """Class constructor. Creates a view for managing Magic the Gathering cards.

        Args:
            root:
                TKinter -element, which initializes the user interface.
            show_login_view:
                Direct user to "Login" view.
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
        """Logout current user."""

        magic_service = MagicService()
        magic_service.logout()
        self._show_login_view()

    def _submit_handler(self):
        """Fetch and save new card data into database
        and save card image on disk."""

        set_selection = self._selected_set.get()
        if self._card_search_entry.get() == "" or set_selection not in self._all_sets:
            return

        card_name = self._card_search_entry.get()
        set_code = self._all_sets[set_selection]

        magic_service = MagicService(card_repository=card_repository)

        try:
            image_path = magic_service.fetch_card(
                card_name, set_code
            )
            print(image_path)
        except CardExistsError as e:
            print(e)

    def initialize_sets(self):
        """Form a dictionary that can be used for populating a dropdown list for
        card set 'names' and also for fetching cards with 'code' in _submit_handler().

        Returns:
            A dictionary with all available card sets, with key = 'name'
            and value = 'code'.
        """

        sets = card_repository.fetch_all_sets()
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
        self._set_list_dropdown = AutocompleteCombobox(
            master=center_frame,
            textvariable=self._selected_set,
            completevalues=sorted(list(self._all_sets)),
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

    def initialize_show_cards(self, cards_frame):
        instruction = ttk.Label(
            cards_frame,
            text="""OHJE TESTAAJALLE:
                    käytä 'Card name' -kentässä tekstiä 'Firebolt'
                    ja valitse 'Set name' valikosta 'Eternal masters'.
                    Terminaaliin tulostuu kortin nimi. Voit toki käyttää
                    mitä tahansa muutakin settiä ja siihen kuuluvaa
                    korttia.""",
            relief="solid"
        )
        instruction.pack(fill="x", pady=2)

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
        self.initialize_show_cards(cards_frame)
