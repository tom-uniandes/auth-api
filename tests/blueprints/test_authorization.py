import unittest
from unittest.mock import patch, MagicMock
from src.main import app
from faker import Faker

class TestAuthorizationBlueprint(unittest.TestCase):
    def setUp(self):
        self.data_factory = Faker()

    @patch('src.commands.login_command.requests.post')
    @patch('src.clients.manage_client.ManageClient.get_data_user')
    def test_verify_authorization(self, mock_get_user_data, mock_firebase_post):
        
        mock_response_firebase = MagicMock()
        mock_response_firebase.status_code = 200
        mock_response_firebase.json.return_value = {'idToken': self.data_factory.uuid4(), 
                                                    'localId': self.data_factory.uuid4(),
                                                    'expiresIn': '1700000'
                                                    }
        mock_firebase_post.return_value = mock_response_firebase

        mock_response_user_data = MagicMock()
        mock_response_user_data.status_code = 200
        mock_response_user_data.json.return_value = {'rol': self.data_factory.word(), 
                                                 'company': self.data_factory.company(),
                                                 'plan': self.data_factory.word()
                                                }
        mock_get_user_data.return_value = mock_response_user_data

        with app.test_client() as test_client:
            response = test_client.get('/auth/verify-authorization', 
                headers={'Authorization': "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzg5Mi1mamQtam5qbnItdWVpd3UifQ.ES_U94pHRusJTcIxQJxAySp62XNO7FLtwkaTWiRYri4"},
            )

        assert response.status_code == 200
