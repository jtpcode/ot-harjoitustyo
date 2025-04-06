class User:
    """Class for a single user

    Attributes:
        username: string
        password: string
    """

    def __init__(self, username, password):
        """Class constructor, creates a new user

        Args:
            username: string
            password: string
        """

        self.username = username
        self.password = password
