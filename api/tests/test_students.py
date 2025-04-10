from fastapi.testclient import TestClient

from ..config import API_KEY
from ..main import app

client = TestClient(app)

new_student = {
  "student_id": "1234567891223",
  "lastname": "lasttest",
  "firstname": "firsttest",
  "email": "6Jt6A@example.com",
  "degree_programme": "testprogramme"
}
updated_student = {
  "student_id": "1234567891223",
  "lastname": "lasttestUPDATED",
  "firstname": "firsttestUPDATED",
  "email": "6Jt6A@example.com",
  "degree_programme": "testprogramme"
}

class TestStudentRoutes:
  def test_get_all_students(self):
    response = client.get("/students", headers={"x-api-key": API_KEY})
    assert response.status_code == 200

  def test_get_all_students_invalid_api_key(self):
    response = client.get("/students", headers={"x-api-key": "invalid"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid API Key"}
  
  def test_create_new_student(self):
    response = client.post(
        "/students/",
        headers={"x-api-key": API_KEY},
        json=new_student,    
    )

    assert response.status_code == 201
    assert response.json() == new_student

  def test_update_student(self):
    response = client.put(
        "/students/1234567891223",
        headers={"x-api-key": API_KEY},
        json=updated_student,  
    )

    assert response.status_code == 200
    assert response.json() == updated_student

  def test_delete_student(self):
    response = client.delete(
        "/students/1234567891223",
        headers={"x-api-key": API_KEY},   
    )

    assert response.status_code == 200
    