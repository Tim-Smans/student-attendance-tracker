import type { StudentRequest } from '@/models/requests/studentRequest';
import type { Student } from '@/models/student';
import {instance} from '@/helpers/axiosHelpers';
import axios from 'axios';

/**
 * Creates all students in the given list. Does not overwrite existing students.
 * @param students List of students to create
 * @returns Promise that resolves when all students have been created
 */
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

  const response = await instance.post('/students', newStudent);

  if(response.status === 201) {
    return true
  }
  console.error(response.status + ": " + response.statusText);
  return false

};

/**
 * Gets the total number of students in the database.
 * @returns Promise that resolves to the total number of students
 */
export const getTotalStudentCount = async () => {
  try {
    const { data } = await instance.get('/students');
    return data.total;
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
}





/**
 * Checks if a student with the given student_id exists in the database.
 * @param student_id The id of the student to check
 * @returns A promise that resolves to true if the student exists, false otherwise
 */
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
