from entities.user import User
from entities.card import Card


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


class CardExistsError(Exception):
    pass


class MagicService:
    """Class responsible for 'Magic archive' application logic.

    Attributes:
        user_repository:
            Repository responsible for user database actions. Defaults to None.
        card_repository:
            Repository responsible for card operations: api.scryfall.com connection
            and database actions. Defaults to None.
    """

    def __init__(self, user_repository=None, card_repository=None):
        """Class constructor. Creates a new service for the application logic.

        Args:
            user_repository:
                Repository responsible for user database actions. Defaults to None.
            card_repository:
                Repository responsible for card operations: api.scryfall.com connection
                and database actions. Defaults to None.
        """

        self._user = None
        self._user_repository = user_repository
        self._card_repository = card_repository

    def create_user(self, username, password):
        """Creates a new user. First validates that username
        and password are valid.

        Args:
            username (str):
            password (str):
        Returns:
            User -object
        Raises:
            UsernameExistsError:
                Username already exist.
            UsernameTooShortError:
                Username is too short (minimum 3 characters).
            PasswordTooShortError:
                Password is too short (minimum 12 characters).
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

    def get_current_user(self):
        """Returns current user who's logged in.

        Returns:
            User -object.
        """

        return self._user

    def login(self, username, password):
        """User login.

        Args:
            username (str):
            password (str):
        Returns:
            User -object
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

    def fetch_card(self, card_name, set_code):
        """Fetches a new Magic card based on card name and set code.
        First checks if card already exists in database. If not,
        card is fetched from api.scryfall.com via card_repository
        and then saved into database.

        Args:
            card_name (str):
            set_code (str):
        Returns:

        """

        if self._card_repository.find_by_card_name(card_name):
            raise CardExistsError(f"Card '{card_name}' exists already")

        card_data = self._card_repository.fetch_card_by_name_and_set(
            card_name, set_code
        )
        card = Card.from_scryfall_json(card_data)
        self._card_repository.create(card)
        # TBA: fetch and save image into /images

        return card

    def logout(self):
        """Logout current user."""

        self._user = None
