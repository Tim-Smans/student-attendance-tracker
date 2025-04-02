import type { StudentRequest } from '@/models/requests/studentRequest';
import type { Student } from '@/models/student';
import {instance} from '@/helpers/axiosHelpers';
import axios from 'axios';

export const createStudentsFromList = async (students: Student[]) => {

  for(const student of students) {
    await createStudent(student)
  }

  console.log("created " + students.length + " students")
}

export const createStudent = async (student: Student) => {
  if(await checkIfStudentExists(student.studentNumber)) {
    console.log("student already exists")
    return false
  }

  const newStudent: StudentRequest = {
    student_id: student.studentNumber,
    degree_programme: student.degreeProgramme,
    email: student.email,
    firstname: student.firstName,
    lastname: student.lastName
  };

  console.log(newStudent)

  const response = await instance.post('/students/', newStudent);

  if(response.status === 201) {
    return true
  }
  console.error(response.status + ": " + response.statusText);
  return false

};


const checkIfStudentExists = async (student_id: string): Promise<boolean> => {
  try {
    const { data } = await instance.get(`/students/${student_id}`);
    return !!data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response?.status === 404) {
        return false;
      }
      console.error("API error:", error.response?.status, error.response?.data);
    } else {
      console.error("Unknown error:", error);
    }

    throw error;
  }
};
