from database_connection import get_database_connection
from entities.user import User

class UserRepository:
    """Class responsible for user database actions"""

    def __init__(self, connection):
        """Class constructor

        Args:
            connection: Connection -object for the database connection
        """

        self._connection = connection

    def find_all(self):
        """Returns all users.

        Returns:
            A list of User -objects
        """

        cursor = self._connection.cursor()

        try:
            cursor.execute("SELECT * FROM Users")
        except Exception as e:
            print("Error:", e)

        rows = cursor.fetchall()

        return [User(row[1], row[2]) for row in rows]

    def find_by_username(self, username):
        """Returns a specific user.

        Returns:
            A User -object
        """

        cursor = self._connection.cursor()

        try:
            cursor.execute(
                "SELECT * FROM Users WHERE username = ?", 
                (username,)
            )
        except Exception as e:
            print("Error:", e)

        row = cursor.fetchone()

        if row:
            return User(row[1], row[2])
        return None


    def create(self, user):
        """Save new user into database

        Args:
            user: User -object

        Returns:
            User -object
        """

        cursor = self._connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO Users (username, password) VALUES (?, ?)",
                (user.username, user.password)
            )
        except Exception as e:
            print("Error:", e)

        self._connection.commit()

user_repository = UserRepository(get_database_connection())
