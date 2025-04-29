from sqlite3 import DatabaseError
import json
import os
import requests
from utils.database.database_connection import get_database_connection
from config import USER_AGENT
from entities.card import Card


class CardNotFoundError(Exception):
    pass


class SetsNotFoundError(Exception):
    pass


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
        """Fetches a specific card from api.scryfall.com
        based on card name and set code.

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
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise CardNotFoundError from e

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
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SetsNotFoundError from e

        return response.json()

    def create(self, card):
        """Save a new card into database

        Args:
            card:
                Card -object
        Returns:
            Card -object
        Raises:
            DatabaseError:
        """

        cursor = self._connection.cursor()

        try:
            # Generated code begins
            cursor.execute("""
                INSERT INTO Cards (
                    name, released_at, layout, mana_cost, cmc,
                    colors, color_identity, type_line, oracle_text, keywords,
                    card_faces, all_parts, power, toughness, image_uris,
                    set_name, set_code, rarity, flavor_text, prices
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                card.name,
                card.released_at,
                card.layout,
                card.mana_cost,
                card.cmc,
                json.dumps(card.colors),
                json.dumps(card.color_identity),
                card.type_line,
                card.oracle_text,
                json.dumps(card.keywords),
                json.dumps(card.card_faces),
                json.dumps(card.all_parts),
                card.power,
                card.toughness,
                json.dumps(card.image_uris),
                card.set_name,
                card.set_code,
                card.rarity,
                card.flavor_text,
                json.dumps(card.prices)
            )
            )
        # Generated code ends
        except DatabaseError as e:
            print("Database error in User repository 'create':", e)

        self._connection.commit()

        return card

    def find_by_card_name(self, card_name):
        """Returns a specific card.

        Args:
            card_name (str):
        Returns:
            A Card -object or None if not found.
        Raises:
            DatabaseError:
        """

        cursor = self._connection.cursor()

        try:
            cursor.execute(
                "SELECT * FROM Cards WHERE name = ?",
                (card_name,)
            )
        except DatabaseError as e:
            print("Database error in Card repository 'find_by_card_name':", e)

        row = cursor.fetchone()

        if row:
            return Card(*row[1:21])

        return None

    def save_card_image(self, image_uri, card_name, save_dir="images"):
        """Saves card image into /images -folder

        Args:
            image_uri (str): Uri for downloading the card image.
            card_name (str): Name of the Magic card.
            save_dir (str): Folder to save images to.
        Returns:
            str: Image path.
        Raises:
            RequestException:
        """

        # Generated code begins
        os.makedirs(save_dir, exist_ok=True)

        filename = f"{card_name.lower().replace(' ', '_')}.png"
        image_path = os.path.join(save_dir, filename)

        try:
            response = requests.get(image_uri, timeout=10)
            response.raise_for_status()
            with open(image_path, "wb") as f:
                f.write(response.content)
        except requests.exceptions.RequestException as e:
            print(f"Error in saving card image: {e}")

        return image_path
        # Generated code ends


card_repository = CardRepository(get_database_connection())
