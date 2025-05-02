from tkinter import ttk, StringVar
from repositories.user_repository import user_repository
from services.magic_service import MagicService, InvalidUsernameError, InvalidPasswordError
from utils.ui_utils import center_window


class LoginView:
    """User interface for login.

    Attributes:
        root:
            TKinter -element, which initializes the user interface.
        show_create_user_view:
            Directs user to "Create new user" view.
        show_magic_card_view:
            Directs user to "Magic card view" aka Main view.
        user_created (bool):
            Signals successfull new user creation.
    """

    def __init__(self, root, show_create_user_view, show_magic_card_view, user_created):
        """Class constructor. Creates a new login view.

        Args:
            root:
                TKinter -element, which initializes the user interface.
            show_create_user_view:
                Directs user to "Create new user" view.
            show_magic_card_view:
                Directs user to "Magic card view" aka Main view.
            user_created (bool):
                Signals successfull new user creation.
        """

        self._root = root
        self._show_create_user_view = show_create_user_view
        self._show_magic_card_view = show_magic_card_view
        self._user_created = user_created
        self._frame = None
        self._username_entry = None
        self._password_entry = None
        self._error_variable = None
        self._error_label = None

        center_window(self._root, 500, 500)
        self._initialize()

    def pack(self):
        """Show current view."""

        self._frame.place(relx=0.5, rely=0.5, anchor="center")

    def destroy(self):
        """Destroy current view."""

        self._frame.destroy()

    def _login_handler(self):
        """Login the user."""

        username = self._username_entry.get()
        password = self._password_entry.get()
        magic_service = MagicService(user_repository=user_repository)

        try:
            magic_service.login(username, password)
            self._show_magic_card_view()
        except InvalidUsernameError as e:
            self._show_error(str(e))
        except InvalidPasswordError as e:
            self._password_entry.delete(0, 'end')
            self._password_entry.focus_set()
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
        self._password_entry = ttk.Entry(
            master=self._frame,
            show="*",
            width=30
        )

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
        title_label.pack(pady=(0, 50))

        if self._user_created:
            self._user_created = False
            self._user_created_label = ttk.Label(
                master=self._frame,
                text="User created successfully",
                foreground="green"
            )
            self._user_created_label.pack(pady=(0, 10))

        self._initialize_username()
        self._initialize_password()
        login_button = ttk.Button(
            master=self._frame,
            text="Login",
            command=self._login_handler,
            width=20)
        login_button.pack(pady=(15, 0))

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red"
        )
        self._error_label.pack(pady=(10, 0))

        new_user_label = ttk.Label(
            master=self._frame,
            text="New user? Create an account here:"
        )
        new_user_label.pack(pady=(50, 10))
        create_user_button = ttk.Button(
            master=self._frame,
            text="Create user",
            command=self._show_create_user_view,
            width=20)
        create_user_button.pack()
