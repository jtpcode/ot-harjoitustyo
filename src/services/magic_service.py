from entities.user import User


class InvalidUsernameError(Exception):
    pass

class InvalidPasswordError(Exception):
    pass


class MagicService:
    """Class responsible for application logic."""

    def __init__(self, user_repository):
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

        #TBA: existing user

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
