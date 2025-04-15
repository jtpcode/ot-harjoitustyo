import unittest
from unittest.mock import patch, Mock
# from utils.database.initialize_database import initialize_database
from repositories.card_repository import card_repository


class TestCardRepository(unittest.TestCase):
    def setUp(self):
        # initialize_database()
        pass

    @patch("repositories.card_repository.requests.get")
    def test_fetch_card_by_name_and_set_with_valid_parameters(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"name": "Lightning Bolt"}
        mock_get.return_value = mock_response

        result = card_repository.fetch_card_by_name_and_set(
            "Lightning Bolt", "m10"
        )

        self.assertEqual(result, {"name": "Lightning Bolt"})
