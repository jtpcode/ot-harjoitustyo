from sqlite3 import Error
import requests
from utils.database.database_connection import get_database_connection
from config import USER_AGENT


class CardRepository:
    """Class responsible for fetching and storing Magic cards"""

    def __init__(self, connection=None):
        """Class constructor

        Args:
            connection:
                Connection -object for the database connection
        """

        self._connection = connection
        self._headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json"
        }

    def fetch_card_by_name(self, name):
        url = f"https://api.scryfall.com/cards/named?fuzzy={name}"

        response = requests.get(
            url,
            headers=self._headers,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()
        raise requests.exceptions.RequestException(
            "Timeout 10 seconds: no response from api.Scryfall.com"
        )
