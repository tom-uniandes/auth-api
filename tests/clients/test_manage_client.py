import unittest
from faker import Faker
from unittest.mock import patch, MagicMock
from src.clients.manage_client import ManageClient
import uuid

class TestManageClient(unittest.TestCase):
    def setUp(self):
            self.data_factory = Faker()

    @patch('src.clients.manage_client.requests.post')
    def test_register_user(self, mock_post):

        id = self.data_factory.uuid4()
        name = self.data_factory.name()

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id":id, "name":name}
        mock_post.return_value = mock_response

        data = {
            "id": id,
            "name": name
        }
        response = ManageClient().register_client(data)
        self.assertTrue(response)


    @patch('src.clients.manage_client.requests.get')
    def test_get_user_data(self, mock_get):

        id = uuid.uuid4()
        name = self.data_factory.name()

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id":id, "name":name}
        mock_get.return_value = mock_response

        response = ManageClient().get_data_user(id)
        self.assertTrue(response)