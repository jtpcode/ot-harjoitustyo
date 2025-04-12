import unittest
from unittest.mock import Mock
import initialize_database
from repositories.user_repository import user_repository
from entities.user import User
from services.magic_service import (
    MagicService,
    InvalidUsernameError,
    InvalidPasswordError,
    UsernameExistsError,
    UsernameTooShortError,
    PasswordTooShortError
)


class TestMagicService(unittest.TestCase):
    def setUp(self):
        initialize_database.initialize_database()
        self.user_alfa = User('alfa', '1234alfa5678')
        user_repository.create(self.user_alfa)

        self.user_repository_mock = Mock()
        self.magic_service = MagicService(self.user_repository_mock)

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
