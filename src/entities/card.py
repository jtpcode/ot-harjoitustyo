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

# Generated code begins


class Card:
    """Class for a Magic: The Gathering card.

    Attributes:
        name (str): Name of the card.
        released_at (str): Release date.
        layout (str): Card layout type.
        stats (CardStats): Card statistics.
        type_line (str): Type line.
        oracle_text (str): Oracle text.
        keywords (list): Keywords.
        card_faces (list): Card face data.
        all_parts (list): Related parts/cards.
        image_uris (dict): Image URIs.
        set_code (str): Set code.
        set_name (str): Set name.
        rarity (str): Rarity.
        flavor_text (str): Flavor text.
        prices (dict): Prices.
    """

    def __init__(self, name, released_at, layout, stats,
                 type_line, oracle_text, keywords,
                 card_faces, all_parts, image_uris,
                 set_code, set_name, rarity, flavor_text, prices):
        """Class Constructor, creates a new card object.

        Attributes:
            name (str): Name of the card.
            released_at (str): Release date.
            layout (str): Card layout type.
            stats (CardStats): Card statistics.
            type_line (str): Type line.
            oracle_text (str): Oracle text.
            keywords (list): Keywords.
            card_faces (list): Card face data.
            all_parts (list): Related parts/cards.
            image_uris (dict): Image URIs.
            set_code (str): Set code.
            set_name (str): Set name.
            rarity (str): Rarity.
            flavor_text (str): Flavor text.
            prices (dict): Prices.
        """

        self.name = name
        self.released_at = released_at
        self.layout = layout
        self.stats = stats
        self.type_line = type_line
        self.oracle_text = oracle_text
        self.keywords = keywords
        self.card_faces = card_faces
        self.all_parts = all_parts
        self.image_uris = image_uris
        self.set_code = set_code
        self.set_name = set_name
        self.rarity = rarity
        self.flavor_text = flavor_text
        self.prices = prices

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
            power=data.get("power") if "power" in data else None,
            toughness=data.get("toughness") if "toughness" in data else None,
            colors=json.dumps(data.get("colors", [])),
            color_identity=json.dumps(data.get("color_identity", []))
        )

        return cls(
            name=data.get("name"),
            released_at=data.get("released_at"),
            layout=data.get("layout"),
            stats=stats,
            type_line=data.get("type_line"),
            oracle_text=data.get(
                "oracle_text") if "oracle_text" in data else None,
            keywords=json.dumps(data.get("keywords", [])),
            card_faces=json.dumps(data.get("card_faces")
                                  ) if "card_faces" in data else None,
            all_parts=json.dumps(data.get("all_parts")
                                 ) if "all_parts" in data else None,
            image_uris=json.dumps(data.get("image_uris")
                                  ) if "image_uris" in data else None,
            set_code=data.get("set"),
            set_name=data.get("set_name"),
            rarity=data.get("rarity"),
            flavor_text=data.get(
                "flavor_text") if "flavor_text" in data else None,
            prices=json.dumps(data.get("prices")) if "prices" in data else None
        )
# Generated code ends
