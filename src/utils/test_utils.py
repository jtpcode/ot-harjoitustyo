import json
from entities.card import Card, CardStats


def create_fake_magic_card():
    """Creates a fake Magic the Gathering card for
    testing purposes.

    Returns:
        (Card): Fake Magic the Gathering card
    """
    stats = CardStats(
        mana_cost="{3}{R}{R}",
        cmc=5.0,
        power="4",
        toughness="4",
        colors=["Red"],
        color_identity=["R"]
    )

    fake_card = Card(
        name="Test_Dragon",
        released_at="2025-04-01",
        layout="normal",
        stats=stats,
        type_line="Creature — Dragon",
        oracle_text="When enters, deals 3 damage to opponent",
        keywords=json.dumps(["Flying"]),
        card_faces=None,
        all_parts=None,
        image_uris=json.dumps({
            "small": "https://example.com/card_small.jpg",
            "normal": "https://example.com/card_normal.jpg",
            "large": "https://example.com/card_large.jpg"
        }),
        set_code="TST",
        set_name="Test_set",
        rarity="rare",
        flavor_text="Fake text here.",
        prices=json.dumps({
            "usd": "0.99",
            "usd_foil": "1.49",
            "eur": "0.89",
            "eur_foil": "1.29"
        }),
        card_id=1
    )

    return fake_card
