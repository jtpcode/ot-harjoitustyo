from entities.user import User


class InvalidUsernameError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class UsernameExistsError(Exception):
    pass


class UsernameTooShortError(Exception):
    pass


class PasswordTooShortError(Exception):
    pass


class MagicService:
    """Class responsible for application logic."""

    def __init__(self, user_repository=None):
        """Class constructor. Creates a new service for the application logic.

        Args:
            user_repository: Repository responsible for user database actions.
        """

        self._user = None
        self._user_repository = user_repository

    def create_user(self, username, password):
        """Creates a new user

        Args:
            username (str)
            password (str)
        Returns:
            Created User -object
        Raises:
            UsernameExistsError:
                Username already exist.
            UsernameTooShortError:
                Username is too short (minimum 3 characters)
            PasswordTooShortError:
                Password is too short (minimum 12 characters)
        """

        if len(username) < 3:
            raise UsernameTooShortError(
                "Username must be at least 3 characters long"
            )
        if len(password) < 12:
            raise PasswordTooShortError(
                "Password must be at least 12 characters long"
            )
        if self._user_repository.find_by_username(username):
            raise UsernameExistsError(f"Username {username} exists already")

        user = self._user_repository.create(User(username, password))

        return user

    def login(self, username, password):
        """User login.

        Args:
            username (str)
            password (str)
        Returns:
            Logged in User -object
        Raises:
            InvalidUsernameError:
                Username doesn't match.
            InvalidPasswordError:
                Password doesn't match.
        """

        user = self._user_repository.find_by_username(username)

        if not user:
            raise InvalidUsernameError("Invalid username")
        if user.password != password:
            raise InvalidPasswordError("Invalid password")

        self._user = user

        return user

    def logout(self):
        """Logout current user.
        """

        self._user = None
