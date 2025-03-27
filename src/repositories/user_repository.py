from entities.user import User
from database_connection import get_database_connection


class UserRepository:
    """Class responsible for user database actions"""

    def __init__(self, connection):
        """Class constructor

        Args:
            connection: Connection -object for the database connection
        """

        self._connection = connection

    def create(self, user):
        """Save new user into database

        Args:
            user: User -object

        Returns:
            User -object
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user.username, user.password)
        )
        print(user.username, user.password)
        self._connection.commit()

        # return user
