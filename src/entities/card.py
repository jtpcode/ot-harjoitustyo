from dataclasses import dataclass
import json


@dataclass
class CardStats:
    mana_cost: str
    cmc: float
    power: str
    toughness: str
    colors: list
    color_identity: list
    type_line: str
    keywords: list


class Card:
    """Class for a Magic: The Gathering card.

    Attributes:
        name (str): Name of the card.
        released_at (str): Release date.
        layout (str): Card layout type.
        stats (CardStats): Card statistics.
        oracle_text (str): Oracle text.
        card_faces (list): Card face data.
        all_parts (list): Related parts/cards.
        image_uris (dict): Image URIs.
        set_code (str): Set code.
        set_name (str): Set name.
        rarity (str): Rarity.
        flavor_text (str): Flavor text.
        prices (dict): Prices.
        card_id (int): Id (primary key) in database. Defaults to None.
    """

    def __init__(self, name, released_at, layout, stats, oracle_text,
                 card_faces, all_parts, image_uris,
                 set_code, set_name, rarity, flavor_text,
                 prices, card_id=None):
        """Class Constructor, creates a new card object.

        Attributes:
            name (str): Name of the card.
            released_at (str): Release date.
            layout (str): Card layout type.
            stats (CardStats): Card statistics.
            oracle_text (str): Oracle text.
            card_faces (list): Card face data.
            all_parts (list): Related parts/cards.
            image_uris (dict): Image URIs.
            set_code (str): Set code.
            set_name (str): Set name.
            rarity (str): Rarity.
            flavor_text (str): Flavor text.
            prices (dict): Prices.
            card_id (int): Id (primary key) in database. Defaults to None.
        """

        self.name = name
        self.released_at = released_at
        self.layout = layout
        self.stats = stats
        self.oracle_text = oracle_text
        self.card_faces = card_faces
        self.all_parts = all_parts
        self.image_uris = image_uris
        self.set_code = set_code
        self.set_name = set_name
        self.rarity = rarity
        self.flavor_text = flavor_text
        self.prices = prices
        self.card_id = card_id

    @classmethod
    def from_scryfall_json(cls, data):
        """Creates a new Card -object based on card data fetched
        from api.scryfall.com.

        Args:
            data (dict):
                All card fields in dict.

        Returns:
                A new Card -object
        """

        stats = CardStats(
            mana_cost=data.get("mana_cost"),
            cmc=data.get("cmc"),
            power=data.get("power"),
            toughness=data.get("toughness"),
            colors=data.get("colors"),
            color_identity=data.get("color_identity"),
            type_line=data.get("type_line"),
            keywords=data.get("keywords")
        )

        return cls(
            name=data.get("name"),
            released_at=data.get("released_at"),
            layout=data.get("layout"),
            stats=stats,
            oracle_text=data.get("oracle_text"),
            card_faces=data.get("card_faces"),
            all_parts=data.get("all_parts"),
            image_uris=data.get("image_uris"),
            set_code=data.get("set"),
            set_name=data.get("set_name"),
            rarity=data.get("rarity"),
            flavor_text=data.get("flavor_text"),
            prices=data.get("prices")
        )

    @classmethod
    def from_database(cls, data):
        """Creates a new Card -object based on card data from local database.

        Args:
            data (sqlite3.Row):
                All card fields in dict-like Row -object.

        Returns:
                A new Card -object
        """

        stats = CardStats(
            mana_cost=data["mana_cost"],
            cmc=data["cmc"],
            power=data["power"],
            toughness=data["toughness"],
            colors=json.loads(data["colors"]),
            color_identity=json.loads(data["color_identity"]),
            type_line=data["type_line"],
            keywords=json.loads(data["keywords"])
        )

        return cls(
            name=data["name"],
            released_at=data["released_at"],
            layout=data["layout"],
            stats=stats,
            oracle_text=data["oracle_text"],
            card_faces=json.loads(data["card_faces"]),
            all_parts=json.loads(data["all_parts"]),
            image_uris=json.loads(data["image_uris"]),
            set_code=data["set_code"],
            set_name=data["set_name"],
            rarity=data["rarity"],
            flavor_text=data["flavor_text"],
            prices=json.loads(data["prices"]),
            card_id=data["id"]
        )
