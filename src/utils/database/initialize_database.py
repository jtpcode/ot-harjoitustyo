from utils.database.database_connection import get_database_connection


def drop_tables(connection):
    """Drop database tables.

    Args:
        connection:
            Connection -object for the database connection.
    """

    cursor = connection.cursor()

    # NOTE: Drops UserCards first, since it depends on Users
    # and Cards (otherwise error will occur)
    cursor.executescript("""
        BEGIN;
        DROP TABLE IF EXISTS UserCards;
        DROP TABLE IF EXISTS Users;
        DROP TABLE IF EXISTS Cards;
        COMMIT;
    """)


def create_tables(connection):
    """Create database tables.

    Args:
        connection:
            Connection -object for the database connection.
    """

    cursor = connection.cursor()

    cursor.executescript("""
        BEGIN;
        CREATE TABLE Users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        );
        CREATE TABLE Cards (
            id INTEGER PRIMARY KEY,
            name TEXT,
            released_at TEXT,
            layout TEXT,
            mana_cost TEXT,
            cmc REAL,
            colors JSON,
            color_identity JSON,
            type_line TEXT,
            oracle_text TEXT,
            keywords JSON,
            card_faces JSON,
            all_parts JSON,
            power TEXT,
            toughness TEXT,
            image_uris JSON,
            set_code TEXT,
            set_name TEXT,
            rarity TEXT,
            flavor_text TEXT,
            prices JSON
        );
        CREATE TABLE UserCards (
            user_id INTEGER NOT NULL,
            card_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, card_id),
            FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
            FOREIGN KEY (card_id) REFERENCES Cards(id) ON DELETE CASCADE
        );
        COMMIT;
    """)


def initialize_database():
    """Initialize the database."""

    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)

    print("Database initialized.")


if __name__ == "__main__":
    initialize_database()
