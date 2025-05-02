import os
from tkinter import ttk, Canvas, constants, StringVar
from ttkwidgets.autocomplete import AutocompleteCombobox
from PIL import Image, ImageTk
from services.magic_service import MagicService, CardExistsError
from repositories.card_repository import (
    card_repository,
    CardNotFoundError,
    SetsNotFoundError,
    DatabaseCreateError,
    DatabaseFindError,
    CardImageNotFoundError
)
from utils.ui_utils import center_window


class CardListView:
    """View for listing card images."""

    def __init__(self, root):
        """Class constructor. Creates a new card list view.

        Args:
            root:
                TKinter -element (cards_frame), which initializes the card view.
        """

        self._root = root
        self._frame = None
        self._content_frame = None
        self._scrollable_frame = None
        self._card_images = []
        self._image_labels = []
        self._images_dir = None
        self._thumbnail_size = None

        self._initialize()

    def pack(self):
        """"Shows the view."""

        self._frame.pack(fill="both", expand=True)

    def destroy(self):
        """"Destroy current view."""

        self._frame.destroy()

    # partially generated code begins
    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_rowconfigure(0, weight=1)

        self._images_dir = "./images"
        self._thumbnail_size = (100, 140)

        canvas = Canvas(master=self._frame)
        scrollbar = ttk.Scrollbar(
            master=self._frame,
            orient="vertical",
            command=canvas.yview
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        self._content_frame = ttk.Frame(master=canvas)
        canvas.create_window(
            (0, 0),
            window=self._content_frame,
            anchor="nw"
        )

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Bind scrollregion and layout refresh with window resize event "<Configure>"
        # NOTE: These binds need to be in different frames for scrollbar to work
        self._content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        self._frame.bind(
            "<Configure>",
            self._refresh_card_layout
        )

        self._load_card_images()
        self._refresh_card_layout()

    def _load_card_images(self):
        """Loads card images into memory as thumbnails."""

        self._image_labels = []
        for filename in sorted(os.listdir(self._images_dir)):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                path = os.path.join(self._images_dir, filename)
                img = Image.open(path)
                img.thumbnail(self._thumbnail_size)
                photo = ImageTk.PhotoImage(img)
                label = ttk.Label(self._content_frame, image=photo)

                # Only saves reference to photo -objects, so they arent't lost
                self._card_images.append(photo)

                self._image_labels.append(label)

    def _refresh_card_layout(self, event=None):
        """Dynamically creates layot for cards according to
        current window size.

        Args:
            event: Window resize event
        """

        for label in self._image_labels:
            label.grid_forget()

        # HACK: frame_width is shortened 50 units to compensate for scrollbar
        # and windows margins, since it's challenging to get self._content_frame
        # width reliably
        frame_width = (event.width if event else self._root.winfo_width()) - 50
        padding = 2
        thumb_width = self._thumbnail_size[0] + 2*padding
        max_columns = max(1, ((frame_width) // thumb_width))
        print(frame_width, thumb_width, max_columns*thumb_width,
              frame_width-max_columns*thumb_width, max_columns)

        row = 0
        col = 0

        for label in self._image_labels:
            label.grid(row=row, column=col, padx=padding, pady=padding)
            col += 1
            if col >= max_columns:
                col = 0
                row += 1
    # partially generated code ends


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
        self._cards_frame = None
        self._card_name_entry = None
        self._all_sets = {}
        self._selected_set = None
        self._set_list_dropdown = None
        self._card_list_view = None

        center_window(self._root, 800, 800)
        self._initialize()

    def pack(self):
        """Show current view."""

        self._frame.pack(fill="both", expand=True)

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
        if self._card_name_entry.get() == "" or set_selection not in self._all_sets:
            return

        card_name = self._card_name_entry.get()
        set_code = self._all_sets[set_selection]

        magic_service = MagicService(card_repository=card_repository)

        try:
            image_path = magic_service.fetch_card(
                card_name, set_code
            )
            # TBA: Notification for user on success/fail
            print(image_path)
        except CardExistsError as e:
            print(e)
        except CardNotFoundError:
            print("Check spelling of the card name")
        except DatabaseCreateError:
            print("Saving card into database failed.")
        except DatabaseFindError:
            print("Getting card from database failed.")
        except CardImageNotFoundError:
            print("Fetching card image failed.")

        # TBA: after adding card, fix card list update
        self._initialize_card_list()

    def initialize_sets(self):
        """Form a dictionary that can be used for populating a dropdown list for
        card set 'names' and also for fetching cards with 'code' in _submit_handler().

        Returns:
            A dictionary with all available card sets, with key = 'name'
            and value = 'code'.
        """

        try:
            sets = card_repository.fetch_all_sets()
            self._all_sets = {set["name"]: set["code"] for set in sets["data"]}
        except SetsNotFoundError:
            print("All sets couldn't be loaded")

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
        card_name_label = ttk.Label(master=center_frame, text="Card name : ")
        select_set_label = ttk.Label(master=center_frame, text="Set name : ")
        self._card_name_entry = ttk.Entry(master=center_frame, width=30)
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

        card_name_label.grid(
            row=0,
            column=0,
            padx=5
        )
        self._card_name_entry.grid(
            row=0,
            column=1,
            padx=5
        )
        select_set_label.grid(
            row=1,
            column=0,
            padx=5,
            pady=(10, 15)
        )
        self._set_list_dropdown.grid(
            row=1,
            column=1,
            padx=5,
            pady=(10, 15),
            sticky=constants.W
        )
        submit_button.grid(
            row=1,
            column=2,
            padx=10,
            pady=(10, 15)
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

    def _initialize_card_list(self):
        if self._card_list_view:
            self._card_list_view.destroy()

        self._card_list_view = CardListView(self._cards_frame)

        self._card_list_view.pack()

    def _initialize(self):
        # Initialize dropdown menu for Set selection
        self.initialize_sets()

        self._frame = ttk.Frame(master=self._root)
        self._frame.grid_rowconfigure(1, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)

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
        self._cards_frame = ttk.Frame(master=self._frame)
        self._cards_frame.grid_rowconfigure(0, weight=1)
        self._cards_frame.grid_columnconfigure(0, weight=1)
        self._cards_frame.grid(
            row=1,
            column=0,
            sticky=constants.NSEW,
            padx=10,
            pady=(0, 10)
        )

        self.initialize_label(top_frame)
        self.initialize_card_search(center_frame)
        self.initialize_logout(top_frame)
        self._initialize_card_list()
