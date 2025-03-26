from tkinter import ttk, constants


class LoginView:
    """User interface responsible for login."""

    def __init__(self, root, handle_login):
        """Class constructor. Creates a new login view.

        Args:
            root:
                TKinter -element, which initializes the user interface.
            handle_login:
                Event handler for user log in.
        """

        self._root = root
        self._handle_login = handle_login
        self._frame = None
        self._username_entry = None
        self._password_entry = None

        self._initialize()

    def pack(self):
        """Show current view."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Destroy current view."""
        self._frame.destroy()
    
    def _initialize_username(self):
        username_label = ttk.Label(master=self._frame, text="Username")
        self._username_entry = ttk.Entry(master=self._frame, width=30)

        username_label.grid(padx=10, pady=5, sticky=constants.W)
        self._username_entry.grid(padx=10, pady=5, sticky=constants.W)

    def _initialize_password(self):
        password_label = ttk.Label(master=self._frame, text="Password")
        self._password_entry = ttk.Entry(master=self._frame, width=30)

        password_label.grid(padx=10, pady=5, sticky=constants.W)
        self._password_entry.grid(padx=10, pady=5, sticky=constants.W)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._initialize_username()
        self._initialize_password()

        login_button = ttk.Button(master=self._frame, text="Login", width=20)
        create_user_button = ttk.Button(master=self._frame, text="Create user", width=20)

        self._frame.grid_columnconfigure(0, weight=1, minsize=350)

        login_button.grid(padx=10, pady=5, sticky=constants.W)
        create_user_button.grid(padx=10, pady=5, sticky=constants.W)
    