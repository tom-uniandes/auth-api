import unittest
from faker import Faker
from unittest.mock import patch, MagicMock
from src.commands.login_command import Login
from src.errors.errors import ApiError

class TestLoginCommand(unittest.TestCase):
    def setUp(self):
        self.data_factory = Faker()

    def test_login_failed_communication_firebase(self):
        with self.assertRaises(ApiError):
            Login({}).execute()

    