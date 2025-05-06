import unittest
from utils.database.initialize_database import initialize_database
from repositories.user_repository import user_repository
from entities.user import User


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        initialize_database()
        self.user_alfa = User('alfa', '1234alfa5678')
        self.user_beta = User('beta', '1234beta5678')

    def test_find_all_success(self):
        user_repository.create(self.user_alfa)
        user_repository.create(self.user_beta)
        users = user_repository.find_all()

        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].username, "alfa")
        self.assertEqual(users[1].username, "beta")

    def test_find_all_returns_none(self):
        users = user_repository.find_all()

        self.assertEqual(users, None)

    def test_find_by_username_success(self):
        user_repository.create(self.user_alfa)
        user = user_repository.find_by_username("alfa")

        self.assertEqual(user.username, "alfa")

    def test_find_by_username_returns_none(self):
        user = user_repository.find_by_username("wrong")

        self.assertEqual(user, None)

    def test_create_success(self):
        user_id = user_repository.create(self.user_beta)

        self.assertEqual(user_id, 1)
