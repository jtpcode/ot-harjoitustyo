from entities.user import User


class InvalidUsernameError(Exception):
    pass

class InvalidPasswordError(Exception):
    pass

class UsernameExistsError(Exception):
    pass


class MagicService:
    """Class responsible for application logic."""

    def __init__(self, user_repository = None):
        """Class constructor. Creates a new services for the application logic.

        Args:
            user_repository: Repository responsible for user database actions.
        """

        self._user = None
        self._user_repository = user_repository

    def create_user(self, username, password):
        """Creates a new user

        Args:
            username: string
            password: string
        """

        if self._user_repository.find_by_username(username):
            raise UsernameExistsError(f"Username {username} exists already")

        self._user_repository.create(User(username, password))

    def login(self, username, password):
        """User login.

        Args:
            username: string
            password: string
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

    def logout(self):
        """Logout current user.
        """
        self._user = None
