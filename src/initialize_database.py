from database_connection import get_database_connection


def drop_tables(connection):
    """Drop database tables

    Args:
        connection: Connection -object for the database connection
    """

    cursor = connection.cursor()

    cursor.execute("""
        DROP TABLE IF EXISTS Users;
    """)

    connection.commit()


def create_tables(connection):
    """Create database tables

    Args:
        connection: Connection -object for the database connection
    """

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE Users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        );
    """)

    connection.commit()


def initialize_database():
    """Initialize database"""

    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    initialize_database()
