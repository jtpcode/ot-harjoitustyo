import unittest
from unittest.mock import patch, Mock, mock_open
import os
import requests.exceptions
from utils.database.initialize_database import initialize_database
from utils import test_utils
from repositories.card_repository import (
    card_repository,
    CardNotFoundError,
    SetsNotFoundError,
    CardImageNotFoundError
)


class TestCardRepository(unittest.TestCase):
    def setUp(self):
        self.mock_response = Mock()
        initialize_database()

        self.fake_card = test_utils.create_fake_magic_card()
        self.card_id = card_repository.create(self.fake_card)

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

    def test_create_card(self):
        self.assertEqual(self.card_id, 1)

    def test_find_card_by_name_and_set(self):
        card = card_repository.find_card_by_name_and_set("Test_Dragon", "TST")

        self.assertEqual(card.card_id, self.card_id)

    @patch("repositories.card_repository.requests.get")
    @patch("repositories.card_repository.open", new_callable=mock_open)
    @patch("repositories.card_repository.os.makedirs")
    def test_save_card_image_successfully(self, mock_makedirs, mock_open_file, mock_get):
        self.mock_response.status_code = 200
        self.mock_response.content = b"fake_image_data"
        mock_get.return_value = self.mock_response

        image_uri = "http://example.com/card.png"
        card_name = "Fake Card"
        result = card_repository.save_card_image(image_uri, card_name)
        expected_path = os.path.join("images", "fake_card.png")

        mock_makedirs.assert_called_once_with("images", exist_ok=True)
        mock_open_file.assert_called_once_with(expected_path, "wb")
        mock_open_file().write.assert_called_once_with(b"fake_image_data")
        self.assertEqual(result, expected_path)

    @patch("repositories.card_repository.requests.get")
    @patch("repositories.card_repository.os.makedirs")
    def test_save_card_image_requests_error(self, mock_makedirs, mock_get):
        self.mock_response.raise_for_status.side_effect = requests.exceptions.RequestException(
            "404 error"
        )
        mock_get.return_value = self.mock_response

        self.assertLessEqual(mock_makedirs.call_count, 1)
        with self.assertRaises(CardImageNotFoundError):
            card_repository.save_card_image("http://invalid.url", "Fake Card")
