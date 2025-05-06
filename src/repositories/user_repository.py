from sqlite3 import DatabaseError
from utils.database.database_connection import get_database_connection
from entities.user import User


class DatabaseFindAllError(Exception):
    pass


class DatabaseFindByUsernameError(Exception):
    pass


class DatabaseCreateError(Exception):
    pass


class UserRepository:
    """Class responsible for user database actions.

    Attributes:
        connection:
            Connection -object for the database connection.
    """

    def __init__(self, connection):
        """Class constructor. Creates a new user repository.

        Args:
            connection:
                Connection -object for the database connection.
        """

        self._connection = connection

    def find_all(self):
        """Returns all users.

        Returns:
            A list of User -objects.
        Raises:
            DatabaseError:
        """

        cursor = self._connection.cursor()

        try:
            cursor.execute("SELECT * FROM Users")
        except DatabaseError as e:
            raise DatabaseFindAllError(
                "Database error in User repository 'find_all'"
            ) from e

        rows = cursor.fetchall()

        if rows:
            return [User(row[1], row[2], row[0]) for row in rows]

        return None

    def find_by_username(self, username):
        """Returns a specific user.

        Args:
            username (str):
        Returns:
            A User -object or None if not found.
        Raises:
            DatabaseError:
        """

        cursor = self._connection.cursor()

        try:
            cursor.execute(
                "SELECT * FROM Users WHERE username = ?",
                (username,)
            )
        except DatabaseError as e:
            raise DatabaseFindByUsernameError(
                "Database error in User repository 'find_by_username'"
            ) from e

        row = cursor.fetchone()

        if row:
            return User(row[1], row[2], row[0])

        return None

    def create(self, user):
        """Save new user into database.

        Args:
            user:
                User -object
        Returns:
            Id (primary key) of the user.
        Raises:
            DatabaseError:
        """

        cursor = self._connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO Users (username, password) VALUES (?, ?)",
                (user.username, user.password)
            )
        except DatabaseError as e:
            raise DatabaseCreateError(
                "Database error in User repository 'create'"
            ) from e

        self._connection.commit()

        return cursor.lastrowid


user_repository = UserRepository(get_database_connection())
