import unittest
from unittest.mock import patch, Mock
import requests.exceptions
from utils.database.initialize_database import initialize_database
from repositories.card_repository import (
    card_repository,
    CardNotFoundError,
    SetsNotFoundError
)
from entities.card import Card


class TestCardRepository(unittest.TestCase):
    def setUp(self):
        self.mock_response = Mock()
        initialize_database()
        self.fake_card = Card(
            name="Test_Dragon",
            released_at="2025-04-01",
            layout="normal",
            mana_cost="{3}{R}{R}",
            cmc=5.0,
            colors=["Red"],
            color_identity=["R"],
            type_line="Creature — Dragon",
            oracle_text="When enters, deals 3 damage to opponent",
            keywords=["Flying"],
            card_faces=None,
            all_parts=None,
            power="4",
            toughness="4",
            image_uris={
                "small": "https://example.com/card_small.jpg",
                "normal": "https://example.com/card_normal.jpg",
                "large": "https://example.com/card_large.jpg"
            },
            set_code="TST",
            set_name="Test_set",
            rarity="rare",
            flavor_text="Fake text here.",
            prices={
                "usd": "0.99",
                "usd_foil": "1.49",
                "eur": "0.89",
                "eur_foil": "1.29"
            }
        )
        card_repository.create(self.fake_card)

    @patch("repositories.card_repository.requests.get")
    def test_fetch_card_by_name_and_set_with_valid_parameters(self, mock_get):
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = {"name": "Lightning Bolt"}
        mock_get.return_value = self.mock_response

        result = card_repository.fetch_card_by_name_and_set(
            "Lightning Bolt", "m10"
        )

        self.assertEqual(result, {"name": "Lightning Bolt"})

    @patch("repositories.card_repository.requests.get")
    def test_fetch_card_by_name_and_set_with_invalid_parameters(self, mock_get):
        self.mock_response.raise_for_status.side_effect = requests.exceptions.RequestException(
            "404 error"
        )
        mock_get.return_value = self.mock_response

        with self.assertRaises(CardNotFoundError):
            card_repository.fetch_card_by_name_and_set(
                "Invalid card name", "m10"
            )

    @patch("repositories.card_repository.requests.get")
    def test_fetch_all_sets_returns_json(self, mock_get):
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = {"data": ["set1", "set2"]}
        mock_get.return_value = self.mock_response

        result = card_repository.fetch_all_sets()

        self.assertEqual(result, {"data": ["set1", "set2"]})

    @patch("repositories.card_repository.requests.get")
    def test_fetch_all_sets_fails(self, mock_get):
        self.mock_response.raise_for_status.side_effect = requests.exceptions.RequestException(
            "404 error"
        )
        mock_get.return_value = self.mock_response

        with self.assertRaises(SetsNotFoundError):
            card_repository.fetch_all_sets()

    def test_find_by_card_name(self):
        card = card_repository.find_by_card_name("Test_Dragon")

        self.assertEqual(card.name, self.fake_card.name)

    def test_create_card(self):
        card = card_repository.find_by_card_name("Test_Dragon")

        self.assertEqual(self.fake_card.name, card.name)

    # TBA: test_save_card_image
