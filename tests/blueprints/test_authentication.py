import unittest
from unittest.mock import patch, MagicMock
from src.main import app
from faker import Faker

class TestAuthenticationBlueprint(unittest.TestCase):
    def setUp(self):
                self.data_factory = Faker()
    
    @patch('src.commands.register_command.requests.post')
    @patch('src.clients.manage_client.ManageClient.register_client')
    def test_register_user(self, mock_post_register, mock_firebase_post):

        mock_response_firebase = MagicMock()
        mock_response_firebase.status_code = 200
        mock_response_firebase.json.return_value = {'idToken': self.data_factory.uuid4(), 'localId': self.data_factory.uuid4()}
        mock_firebase_post.return_value = mock_response_firebase

        mock_post_register.return_value = MagicMock(status_code=201)

        with app.test_client() as test_client:
            response = test_client.post('/auth/register', 
                headers={'Content-Type': "application/json"},
                json={
                "name": self.data_factory.paragraph(nb_sentences=1),
                "email": self.data_factory.email(),
                "password": self.data_factory.password(),
                "idType": self.data_factory.word(),
                "idNumber": "1111111111",
                "phoneNumber": self.data_factory.phone_number(),
                "company": self.data_factory.company(),
                "rol":self.data_factory.word(),
                "plan":self.data_factory.word(),
                }
            )

        assert response.status_code == 201

    @patch('src.commands.login_command.requests.post')
    @patch('src.clients.manage_client.ManageClient.get_data_user')
    def test_login_user(self, mock_post_login, mock_firebase_post):

        mock_response_firebase = MagicMock()
        mock_response_firebase.status_code = 200
        mock_response_firebase.json.return_value = {'idToken': self.data_factory.uuid4(), 
                                                    'localId': self.data_factory.uuid4(),
                                                    'expiresIn': '1700000'
                                                    }
        mock_firebase_post.return_value = mock_response_firebase

        mock_response_login = MagicMock()
        mock_response_login.status_code = 200
        mock_response_login.json.return_value = {'rol': self.data_factory.word(), 
                                                 'company': self.data_factory.company(),
                                                 'plan': self.data_factory.word()
                                                }
        mock_post_login.return_value = mock_response_login

        with app.test_client() as test_client:
            response = test_client.post('/auth/login', 
                headers={'Content-Type': "application/json"},
                json={
                "email": self.data_factory.email(),
                "password": self.data_factory.password(),
                }
            )

        assert response.status_code == 200

    
    def test_logout_user(self):
        with app.test_client() as test_client:
            response = test_client.post('/auth/logout', 
                headers={'Authorization': self.data_factory.uuid4()},
                json={}
            )

        assert response.status_code == 200

