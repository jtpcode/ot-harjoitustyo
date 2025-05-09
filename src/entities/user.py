class User:
    """Class for an application user.

    Attributes:
        username (str):
        password (str):
        user_id (int): Id (primary key) in database. Defaults to None.
    """

    def __init__(self, username, password, user_id=None):
        """Class constructor, creates a new user.

        Args:
            username (str):
            password (str):
            user_id (int): Id (primary key) in database. Defaults to None.
        """

        self.username = username
        self.password = password
        self.user_id = user_id
