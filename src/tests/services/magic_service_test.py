import unittest
from unittest.mock import Mock, patch
import os
from utils.database.initialize_database import initialize_database
from utils import test_utils
from repositories.user_repository import user_repository
from repositories.card_repository import card_repository
from entities.user import User

from services.magic_service import (
    MagicService,
    InvalidUsernameError,
    InvalidPasswordError,
    UsernameExistsError,
    UsernameTooShortError,
    PasswordTooShortError,
    CardExistsError
)


class TestMagicService(unittest.TestCase):
    def setUp(self):
        initialize_database()
        self.user_alfa = User('alfa', '1234alfa5678')
        user_repository.create(self.user_alfa)

        self.fake_card = test_utils.create_fake_magic_card()
        card_repository.create(self.fake_card)

        self.mock_response = Mock()
        self.user_repository_mock = Mock()
        self.card_repository_mock = Mock()
        self.magic_service = MagicService(
            user_repository=self.user_repository_mock,
            card_repository=self.card_repository_mock)

    def test_create_user_with_non_existing_username_and_valid_password(self):
        self.user_repository_mock.find_by_username.return_value = None
        self.user_repository_mock.create.return_value = self.user_alfa

        user = self.magic_service.create_user('alfa', '1234alfa5678')

        self.assertEqual(user.username, 'alfa')

    def test_create_user_with_existing_username(self):
        self.user_repository_mock.find_by_username.return_value = self.user_alfa

        self.assertRaises(
            UsernameExistsError,
            lambda: self.magic_service.create_user('alfa', '1234alfa5678')
        )

    def test_create_user_with_too_short_username(self):
        self.assertRaises(
            UsernameTooShortError,
            lambda: self.magic_service.create_user('al', '1234alfa5678')
        )

    def test_create_user_with_too_short_password(self):
        self.assertRaises(
            PasswordTooShortError,
            lambda: self.magic_service.create_user('alfa', '1234')
        )

    def test_get_current_user_success(self):
        self.user_repository_mock.find_by_username.return_value = self.user_alfa
        logged_user = self.magic_service.login(
            self.user_alfa.username, self.user_alfa.password
        )

        current_user = self.magic_service.get_current_user()

        self.assertEqual(current_user, logged_user)

    def test_login_with_valid_credentials(self):
        self.user_repository_mock.find_by_username.return_value = self.user_alfa

        user = self.magic_service.login(
            self.user_alfa.username,
            self.user_alfa.password
        )

        self.assertEqual(user.username, self.user_alfa.username)

    def test_login_with_invalid_username(self):
        self.user_repository_mock.find_by_username.return_value = None

        self.assertRaises(
            InvalidUsernameError,
            lambda: self.magic_service.login('foo', 'barbarbarbar')
        )

    def test_login_with_invalid_password(self):
        self.user_repository_mock.find_by_username.return_value = self.user_alfa

        self.assertRaises(
            InvalidPasswordError,
            lambda: self.magic_service.login('alfa', 'invalid_password')
        )

    @patch("services.magic_service.Card.from_scryfall_json")
    def test_fetch_card_success(self, mock_from_scryfall_json):
        self.card_repository_mock.fetch_card_by_name_and_set.return_value = {
            "name": "Fake Card"
        }
        self.card_repository_mock.find_by_card_name.return_value = None
        mock_from_scryfall_json.return_value = self.fake_card

        expected_image_path = os.path.join("images", "fake_card.png")
        self.card_repository_mock.save_card_image.return_value = expected_image_path

        image_path = self.magic_service.fetch_card(
            "Fake Card", "FAKE_SET_CODE"
        )

        self.assertEqual(expected_image_path, image_path)

    def test_fetch_card_fails_on_card_exists(self):
        self.card_repository_mock.fetch_card_by_name_and_set.return_value = {
            "name": "Fake Card"
        }
        self.card_repository_mock.find_by_card_name.return_value = "Fake Card"

        self.assertRaises(
            CardExistsError,
            lambda: self.magic_service.fetch_card(
                "Fake Card", "FAKE_SET_CODE"
            )
        )

    def test_logout_user_successfully(self):
        self.user_repository_mock.find_by_username.return_value = self.user_alfa

        self.magic_service.login(
            self.user_alfa.username,
            self.user_alfa.password
        )
        self.magic_service.logout()

        self.assertEqual(self.magic_service.get_current_user(), None)
