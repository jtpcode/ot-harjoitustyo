import unittest
from unittest.mock import patch, Mock, mock_open
import os
import requests.exceptions
from utils.database.initialize_database import initialize_database
from utils import test_utils
from repositories.card_repository import (
    card_repository,
    IncorrectNameOrSetError,
    SetsNotFoundError,
    DatabaseCreateError,
    CardImageNotFoundError
)
from repositories.user_repository import user_repository
from entities.user import User


class TestCardRepository(unittest.TestCase):
    def setUp(self):
        self.mock_response = Mock()
        initialize_database()

        self.fake_card = None
        self.card_id = None
        self.user_alfa = None
        self.user_id = None

    def create_fake_card_and_user_and_assign(self):
        self.fake_card = test_utils.create_fake_magic_card()
        self.card_id = card_repository.create(self.fake_card)

        self.user_alfa = User('alfa', '1234alfa5678')
        self.user_id = user_repository.create(self.user_alfa)

        result = card_repository.add_card_to_user(
            self.user_id, self.card_id
        )

        return result

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

        with self.assertRaises(IncorrectNameOrSetError):
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
        self.create_fake_card_and_user_and_assign()

        self.assertEqual(self.card_id, 1)

    def test_find_card_by_name_and_set(self):
        self.create_fake_card_and_user_and_assign()
        card = card_repository.find_card_by_name_and_set("Test_Dragon", "TST")

        self.assertEqual(card.card_id, self.card_id)

    def test_add_card_to_user_success(self):
        result = self.create_fake_card_and_user_and_assign()

        self.assertEqual(result, True)

    def test_add_card_to_user_fail(self):
        with self.assertRaises(DatabaseCreateError):
            card_repository.add_card_to_user(
                "wrong_id", "wrong_id"
            )

    def test_delete_card_from_user_success(self):
        self.create_fake_card_and_user_and_assign()
        response = card_repository.delete_card_from_user(
            self.fake_card.card_id,
            self.user_alfa.user_id
        )

        self.assertEqual(response, True)

    def test_get_user_card_names_success(self):
        self.create_fake_card_and_user_and_assign()
        result = card_repository.get_user_card_names_and_set_codes(
            self.user_id)

        self.assertEqual(result[0][0], "Test_Dragon")

    def test_get_user_card_names_returns_none(self):
        result = card_repository.get_user_card_names_and_set_codes(-1)

        self.assertEqual(result, None)

    def test_user_has_card_success(self):
        self.create_fake_card_and_user_and_assign()
        result = card_repository.user_has_card(
            self.user_id, self.card_id
        )

        self.assertEqual(result, True)

    def test_user_has_card_returns_false(self):
        result = card_repository.user_has_card(
            -1, -2
        )

        self.assertEqual(result, False)

    @patch("repositories.card_repository.requests.get")
    @patch("repositories.card_repository.open", new_callable=mock_open)
    def test_save_card_image_successfully(self, mock_open_file, mock_get):
        self.mock_response.status_code = 200
        self.mock_response.content = b"fake_image_data"
        mock_get.return_value = self.mock_response

        image_uri = "http://example.com/card.png"
        card_name = "Fake Card"
        set_code = "FAKE"
        dirname = os.path.dirname(__file__)
        expected_path = os.path.abspath(
            os.path.join(
                dirname, "..", "..", "..", "images", "fake_card_FAKE.png"
            )
        )

        card_repository.save_card_image(
            image_uri, card_name, set_code
        )

        mock_open_file.assert_called_once_with(expected_path, "wb")
        mock_open_file().write.assert_called_once_with(b"fake_image_data")

    @patch("repositories.card_repository.requests.get")
    def test_save_card_image_requests_error(self, mock_get):
        self.mock_response.raise_for_status.side_effect = requests.exceptions.RequestException(
            "404 error"
        )
        mock_get.return_value = self.mock_response

        with self.assertRaises(CardImageNotFoundError):
            card_repository.save_card_image(
                "http://invalid.url",
                "Fake Card",
                "FAKE"
            )
