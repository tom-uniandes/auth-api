from src.main import app

class TestPing():
  def test_ping(self):
    with app.test_client() as test_client:
      response = test_client.get('/ping')
      assert response.status_code == 200