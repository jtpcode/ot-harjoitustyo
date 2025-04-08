from tkinter import ttk, StringVar
from repositories.user_repository import user_repository
from services.magic_service import MagicService, UsernameExistsError


class CreateUserView:
    """User interface for creating a new user."""

    def __init__(self, root, show_login_view):
        """Class constructor. Creates a new view for creating a new user.

        Args:
            root:
                TKinter -element, which initializes the user interface.
            show_login_view:
                Direct user to login view
        """

        self._root = root
        self._show_login_view = show_login_view
        self._frame = None
        self._new_username_entry = None
        self._new_password_entry = None
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

    def _create_user_handler(self):
        username = self._new_username_entry.get()
        password = self._new_password_entry.get()
        magic_service = MagicService(user_repository)

        if len(username) < 3:
            self._show_error("Username must be at least 3 characters long")
            return
        if len(password) < 12:
            self._show_error("Password must be at least 12 characters long")
            return

        try:
            magic_service.create_user(username, password)
            # TBA: "Account created successfully -alert"
            self._show_login_view()
        except UsernameExistsError as e:
            self._show_error(str(e))

    def _show_error(self, message):
        self._error_variable.set(message)
        self._error_label.pack()

    def _initialize_new_username(self):
        new_username_label = ttk.Label(master=self._frame, text="Username")
        self._new_username_entry = ttk.Entry(master=self._frame, width=30)

        new_username_label.pack()
        self._new_username_entry.pack()

    def _initialize_new_password(self):
        new_password_label = ttk.Label(master=self._frame, text="Password")
        self._new_password_entry = ttk.Entry(master=self._frame, width=30)

        new_password_label.pack(pady=(10, 0))
        self._new_password_entry.pack()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._error_variable = StringVar(self._frame)

        title_label = ttk.Label(
            master=self._frame,
            text="Create an account",
            font=("Arial", 24, "bold"),
        )
        title_label.pack(pady=(0, 20))

        self._initialize_new_username()
        self._initialize_new_password()
        create_user_button = ttk.Button(
            master=self._frame,
            text="Create user",
            command=self._create_user_handler,
            width=20)
        create_user_button.pack(pady=(15, 0))

        # TBA: button to Login view

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red"
        )
        self._error_label.pack(pady=(5, 0))

        self._error_label.pack_forget()
