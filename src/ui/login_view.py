from tkinter import ttk, constants
from repositories.user_repository import user_repository
from services.magic_service import MagicService


class LoginView:
    """User interface for login."""

    def __init__(self, root):
        """Class constructor. Creates a new login view.

        Args:
            root:
                TKinter -element, which initializes the user interface.
            handle_login:
                Event handler for user login.
        """

        self._root = root
        self._frame = None
        self._username_entry = None
        self._password_entry = None
        self._new_username_entry = None
        self._new_password_entry = None

        # Center window in the screen
        height = 500
        width = 500
        x = (self._root.winfo_screenwidth() // 2) - (width // 2)
        y = (self._root.winfo_screenheight() // 2) - (height // 2)
        self._root.geometry(f'{width}x{height}+{x}+{y}')

        self._initialize()

    def pack(self):
        """Show current view."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Destroy current view."""
        self._frame.destroy()

    def _create_user_handler(self):
        username = self._new_username_entry.get()
        password = self._new_password_entry.get()
        magic_service = MagicService(user_repository)

        if len(username) == 0 or len(password) == 0:
            print("Username or password is missing!")
            return

        try:
            magic_service.create_user(username, password)
        except:
            print("Error in creating user!")
    
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

    def _initialize_new_username(self):
        new_username_label = ttk.Label(master=self._frame, text="Username")
        self._new_username_entry = ttk.Entry(master=self._frame, width=30)

        new_username_label.grid(padx=10, pady=5, sticky=constants.W)
        self._new_username_entry.grid(padx=10, pady=5, sticky=constants.W)

    def _initialize_new_password(self):
        new_password_label = ttk.Label(master=self._frame, text="Password")
        self._new_password_entry = ttk.Entry(master=self._frame, width=30)

        new_password_label.grid(padx=10, pady=5, sticky=constants.W)
        self._new_password_entry.grid(padx=10, pady=5, sticky=constants.W)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._frame.grid_columnconfigure(0, weight=1, minsize=350)

        # Login
        self._initialize_username()
        self._initialize_password()
        login_button = ttk.Button(
            master=self._frame,
            text="Login",
            command=None,
            width=20)
        login_button.grid(padx=10, pady=5, sticky=constants.W)

        # New user
        new_user_label = ttk.Label(master=self._frame, text="New user? Create credentials here:")
        new_user_label.grid(padx=10, pady=5, sticky=constants.W)
        self._initialize_new_username()
        self._initialize_new_password()
        create_user_button = ttk.Button(
            master=self._frame,
            text="Create user",
            command=self._create_user_handler,
            width=20)
        create_user_button.grid(padx=10, pady=5, sticky=constants.W)
        
    