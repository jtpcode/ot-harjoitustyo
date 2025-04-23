# from sqlite3 import Error
import requests
from utils.database.database_connection import get_database_connection
from config import USER_AGENT


class CardRepository:
    """Class responsible for fetching Magic cards from api.scryfall.com
    and storing them into database.

    Attributes:
        connection:
            Connection -object for the database connection.
    """

    def __init__(self, connection):
        """Class constructor. Creates a new card repository.

        Args:
            connection:
                Connection -object for the database connection.
        """

        self._connection = connection

        # api.scryfall.com requires these headers
        self._headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json"
        }

    def fetch_card_by_name_and_set(self, card_name, set_code):
        """Fetches a specific card based on card name and set code.

        Args:
            card_name (str):
            set_code (str):
        Returns:
            A Card object in json format.
        Raises:
            RequestException:
        """

        url = "https://api.scryfall.com/cards/named"

        try:
            response = requests.get(
                url,
                params={
                    "exact": card_name,
                    "set": set_code
                },
                headers=self._headers,
                timeout=10
            )
            response.raise_for_status()  # Throw exception for error in response
        except requests.exceptions.RequestException as e:
            print(f"Error in fetching a card: {e}")

        return response.json()

    def fetch_all_sets(self):
        """Fetches all available card sets.

        Returns:
            All card sets in json format.
        Raises:
            RequestException:
        """

        url = "https://api.scryfall.com/sets"

        try:
            response = requests.get(
                url,
                headers=self._headers,
                timeout=10
            )
            response.raise_for_status()  # Throw exception for error in response
        except requests.exceptions.RequestException as e:
            print(f"Error in fetching all card sets: {e}")

        return response.json()


card_repository = CardRepository(get_database_connection())
