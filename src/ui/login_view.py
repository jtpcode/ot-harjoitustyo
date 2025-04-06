from tkinter import ttk, StringVar
from repositories.user_repository import user_repository
from services.magic_service import MagicService, InvalidUsernameError, InvalidPasswordError


class LoginView:
    """User interface for login."""

    def __init__(self, root, show_create_user_view, show_magic_card_view):
        """Class constructor. Creates a new login view.

        Args:
            root:
                TKinter -element, which initializes the user interface.
            show_create_user_view:
                Directs user to "Create new user" -view
        """

        self._root = root
        self._show_create_user_view = show_create_user_view
        self._show_magic_card_view = show_magic_card_view
        self._frame = None
        self._username_entry = None
        self._password_entry = None
        self._error_variable = None
        self._error_label = None

        # Center the window
        self._height = 500
        self._width = 500
        x = (self._root.winfo_screenwidth() // 2) - (self._width // 2)
        y = (self._root.winfo_screenheight() // 2) - (self._height // 2)
        self._root.geometry(f'{self._width}x{self._height}+{x}+{y}')

        self._initialize()

    def pack(self):
        """Show current view."""
        self._frame.place(relx=0.5, rely=0.5, anchor="center")

    def destroy(self):
        """Destroy current view."""
        self._frame.destroy()

    def _login_handler(self):
        username = self._username_entry.get()
        password = self._password_entry.get()
        magic_service = MagicService(user_repository)

        try:
            magic_service.login(username, password)
            self._show_magic_card_view()
        except InvalidUsernameError as e:
            self._show_error(str(e))
        except InvalidPasswordError as e:
            self._show_error(str(e))

    def _show_error(self, message):
        self._error_variable.set(message)
        self._error_label.pack()

    def _initialize_username(self):
        username_label = ttk.Label(master=self._frame, text="Username")
        self._username_entry = ttk.Entry(master=self._frame, width=30)

        username_label.pack()
        self._username_entry.pack()

    def _initialize_password(self):
        password_label = ttk.Label(master=self._frame, text="Password")
        self._password_entry = ttk.Entry(master=self._frame, width=30)

        password_label.pack(pady=(10, 0))
        self._password_entry.pack()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._error_variable = StringVar(self._frame)

        title_label = ttk.Label(
            master=self._frame,
            text="Magic Archive",
            font=("Arial", 24, "bold"),
        )
        title_label.pack(pady=(0, 60))

        self._initialize_username()
        self._initialize_password()
        login_button = ttk.Button(
            master=self._frame,
            text="Login",
            command=self._login_handler,
            width=20)
        login_button.pack(pady=(15, 0))

        # TBA: place in the middle
        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red"
        )
        self._error_label.pack(pady=(5, 0))

        new_user_label = ttk.Label(master=self._frame, text="New user? Create an account here:")
        new_user_label.pack(pady=(70, 10))
        create_user_button = ttk.Button(
            master=self._frame,
            text="Create user",
            command=self._show_create_user_view,
            width=20)
        create_user_button.pack()

        self._error_label.pack_forget()
