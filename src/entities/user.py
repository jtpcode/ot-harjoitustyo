class User:
    """Class for a single user

    Attributes:
        username (str):
        password (str):
    """

    def __init__(self, username, password):
        """Class constructor, creates a new user

        Args:
            username (str):
            password (str):
        """

        self.username = username
        self.password = password
