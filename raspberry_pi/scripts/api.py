import requests
from .config import API_KEY, BASE_URL


def add_attendance(student_id: str, room):
  
  if check_student_exist(student_id) == False:
    idParts = student_id.split('.')
    institution_id = idParts[0]
    
    response = add_student(student_id, institution_id)
    
    if(response.status_code != 200):
      return
    


  payload = {
    "student_id": student_id,
    "room": room
  }

  response = requests.post(
    f"{BASE_URL}/attendance",
    json=payload, 
    headers=headers
  )


def add_student(student_id: str, institution_id: str):
  payload = {
    "student_id": student_id,
    "institution_id": institution_id
  }

  response = requests.post(
    f"{BASE_URL}/student",
    json=payload, 
    headers=headers
  )

  return response




def check_student_exist(student_id: str):
  response = requests.get(f"{BASE_URL}/student/{student_id}", headers=headers)
  if(response.status_code == 404):
    return False
  
  return True
  
