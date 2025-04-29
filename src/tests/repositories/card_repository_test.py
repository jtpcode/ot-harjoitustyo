import unittest
from unittest.mock import patch, Mock
import requests.exceptions
from utils.database.initialize_database import initialize_database
from repositories.card_repository import (
    card_repository,
    CardNotFoundError,
    SetsNotFoundError
)


class TestCardRepository(unittest.TestCase):
    def setUp(self):
        self.mock_response = Mock()
        initialize_database()

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
