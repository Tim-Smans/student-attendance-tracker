from fastapi.testclient import TestClient

from ..config import API_KEY
from ..main import app

client = TestClient(app)


class TestStudentRoutes:
  def test_get_all_attendances(self):
    response = client.get("/attendances", headers={"x-api-key": API_KEY})
    assert response.status_code == 200

  def test_get_all_attendances_invalid_api_key(self):
    response = client.get("/attendances", headers={"x-api-key": "invalid"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid API Key"}
  