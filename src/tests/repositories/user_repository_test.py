import unittest
import initialize_database
from repositories.user_repository import user_repository
from entities.user import User


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        initialize_database.initialize_database()
        self.user_alfa = User('alfa', '1234alfa5678')
        self.user_beta = User('beta', '1234beta5678')

    def test_create(self):
        user_repository.create(self.user_alfa)
        user_repository.create(self.user_beta)
        users = user_repository.find_all()

        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].username, self.user_alfa.username)
        self.assertEqual(users[1].username, self.user_beta.username)
    
