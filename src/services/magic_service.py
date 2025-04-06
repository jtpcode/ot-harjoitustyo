from entities.user import User


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
