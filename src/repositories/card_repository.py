from sqlite3 import DatabaseError
import json
import os
import requests
from entities.card import Card
from utils.database.database_connection import get_database_connection
from config import USER_AGENT


class CardNotFoundError(Exception):
    pass


class SetsNotFoundError(Exception):
    pass


class DatabaseCreateError(Exception):
    pass


class DatabaseFindError(Exception):
    pass


class CardImageNotFoundError(Exception):
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
            Card data in dict format.
        Raises:
            CardNotFoundError:
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
            raise CardNotFoundError(
                "Incorrect card name or set."
            ) from e

        return response.json()

    def fetch_all_sets(self):
        """Fetches all available card sets.

        Returns:
            All card sets in dict format.
        Raises:
            SetsNotFoundError:
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
            raise SetsNotFoundError("All sets couldn't be loaded") from e

        return response.json()

    def create(self, card):
        """Save a new card into database

        Args:
            card:
                Card -object
        Returns:
            Card -object
        Raises:
            DatabaseCreateError:
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
                card.stats.mana_cost,
                card.stats.cmc,
                json.dumps(card.stats.colors),
                json.dumps(card.stats.color_identity),
                card.type_line,
                card.oracle_text,
                json.dumps(card.keywords),
                json.dumps(card.card_faces),
                json.dumps(card.all_parts),
                card.stats.power,
                card.stats.toughness,
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
            raise DatabaseCreateError(
                "Saving card into database failed."
            ) from e

        self._connection.commit()

        return card

    def get_card_id(self, card_name):
        """Returns cards database id.

        Args:
            card_name (str):
        Returns:
            The card id or None if not found.
        Raises:
            DatabaseError:
        """

        cursor = self._connection.cursor()

        try:
            cursor.execute(
                "SELECT id FROM Cards WHERE name = ?",
                (card_name,)
            )
        except DatabaseError as e:
            print("Database error in Card repository 'get_card_id':", e)

        row = cursor.fetchone()

        if row:
            return row[0]

        return None

    def find_by_card_name(self, card_name):
        """Returns a specific card.

        Args:
            card_name (str):
        Returns:
            A Card -object or None if not found.
        Raises:
            DatabaseFindError:
        """

        cursor = self._connection.cursor()

        try:
            cursor.execute(
                "SELECT * FROM Cards WHERE name = ?",
                (card_name,)
            )
        except DatabaseError as e:
            raise DatabaseFindError(
                "Getting card from database failed."
            ) from e

        row = cursor.fetchone()

        if row:
            return Card.from_database(row)

        return None

    def get_user_card_names(self, username):
        """Gets names of the cards owned by the user.

        Args:
            username (str):
        Returns:
            List of card names owned by the user,
            None if not found.
        Raises:
            DatabaseFindError:
        """

        cursor = self._connection.cursor()

        try:
            cursor.execute(
                """SELECT c.name
                FROM Users u
                LEFT JOIN UserCards uc ON u.id = uc.user_id
                LEFT JOIN Cards c ON c.id = uc.card_id
                WHERE u.username = ?""",
                (username,)
            )
        except DatabaseError as e:
            raise DatabaseFindError(
                "Getting users card names from database failed."
            ) from e

        rows = cursor.fetchall()

        if rows:
            return [row[0] for row in rows]

        return None

    def user_has_card(self, username, card_name):
        """Returns true of false based on whether current
        user already has the card in collection.

        Args:
            username (str):
            card_name (str):
        Returns:
            True or false.
        Raises:
            DatabaseFindError:
        """

        cursor = self._connection.cursor()

        try:
            cursor.execute(
                """SELECT uc.card_id
                FROM Users u
                LEFT JOIN UserCards uc ON u.id = uc.user_id
                LEFT JOIN Cards c ON c.id = uc.card_id
                WHERE u.username = ? AND c.name = ?""",
                (username, card_name)
            )
        except DatabaseError as e:
            raise DatabaseFindError(
                "Getting card from database failed."
            ) from e

        row = cursor.fetchone()

        if row:
            return True

        return False

    def add_card_to_user(self, user_id, card_id):
        """Add a new card into database for current user.

        Args:
            username (str):
            card_name (str):
        Returns:
            True if success.
        Raises:
            DatabaseCreateError:
        """

        cursor = self._connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO UserCards (user_id, card_id)
                VALUES (?, ?)""", (user_id, card_id)
                           )
        except DatabaseError as e:
            raise DatabaseCreateError(
                "Saving card for current user in database failed."
            ) from e

        self._connection.commit()

        return True

    def save_card_image(self, image_uri, card_name, save_dir="images"):
        """Saves card image into /images -folder

        Args:
            image_uri (str): Uri for downloading the card image.
            card_name (str): Name of the Magic card.
            save_dir (str): Folder to save images to.
        Returns:
            str: Image path.
        Raises:
            CardImageNotFoundError:
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
            raise CardImageNotFoundError("Fetching card image failed.") from e

        return image_path
        # Generated code ends


card_repository = CardRepository(get_database_connection())
