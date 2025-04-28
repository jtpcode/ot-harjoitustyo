import json


# Generated code begins
class Card:
    """Class for a Magic: The Gathering card.

    Attributes:
        name (str): Name of the card.
        released_at (str): Release date.
        layout (str): Card layout type.
        mana_cost (str): Mana cost.
        cmc (float): Converted mana cost.
        colors (list): List of colors.
        color_identity (list): Color identity.
        type_line (str): Type line.
        oracle_text (str): Oracle text.
        keywords (list): Keywords.
        card_faces (list): Card face data.
        all_parts (list): Related parts/cards.
        power (str): Power (if creature).
        toughness (str): Toughness (if creature).
        image_uris (dict): Image URIs.
        set_code (str): Set code.
        set_name (str): Set name.
        rarity (str): Rarity.
        flavor_text (str): Flavor text.
        prices (dict): Prices.
    """

    def __init__(self, name, released_at, layout, mana_cost, cmc,
                 colors, color_identity, type_line, oracle_text, keywords,
                 card_faces, all_parts, power, toughness, image_uris,
                 set_code, set_name, rarity, flavor_text, prices):
        """Class Constructor, creates a new card object.

        Attributes:
            name (str): Name of the card.
            released_at (str): Release date.
            layout (str): Card layout type.
            mana_cost (str): Mana cost.
            cmc (float): Converted mana cost.
            colors (list): List of colors.
            color_identity (list): Color identity.
            type_line (str): Type line.
            oracle_text (str): Oracle text.
            keywords (list): Keywords.
            card_faces (list): Card face data.
            all_parts (list): Related parts/cards.
            power (str): Power (if creature).
            toughness (str): Toughness (if creature).
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
        self.mana_cost = mana_cost
        self.cmc = cmc
        self.colors = colors
        self.color_identity = color_identity
        self.type_line = type_line
        self.oracle_text = oracle_text
        self.keywords = keywords
        self.card_faces = card_faces
        self.all_parts = all_parts
        self.power = power
        self.toughness = toughness
        self.image_uris = image_uris
        self.set_code = set_code
        self.set_name = set_name
        self.rarity = rarity
        self.flavor_text = flavor_text
        self.prices = prices

    def __str__(self):
        return f"{self.name} ({self.set_name}) - {self.type_line} - {self.mana_cost}"

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
        return cls(
            name=data.get("name"),
            released_at=data.get("released_at"),
            layout=data.get("layout"),
            mana_cost=data.get("mana_cost"),
            cmc=data.get("cmc"),
            colors=json.dumps(data.get("colors", [])),
            color_identity=json.dumps(data.get("color_identity", [])),
            type_line=data.get("type_line"),
            oracle_text=data.get(
                "oracle_text") if "oracle_text" in data else None,
            keywords=json.dumps(data.get("keywords", [])),
            card_faces=json.dumps(data.get("card_faces")
                                  ) if "card_faces" in data else None,
            all_parts=json.dumps(data.get("all_parts")
                                 ) if "all_parts" in data else None,
            power=data.get("power") if "power" in data else None,
            toughness=data.get("toughness") if "toughness" in data else None,
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
