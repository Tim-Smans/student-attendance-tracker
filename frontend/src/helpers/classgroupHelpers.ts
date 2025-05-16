import type { ClassGroup } from '@/models/classGroup';
import { createStudentsFromList } from './studentHelpers';
import {instance} from '@/helpers/axiosHelpers';
import type { ClassGroupResponse } from '@/models/responses/classGroupResponse';
import type { Student } from '@/models/student';
import type { StudentResponse } from '@/models/responses/studentResponse';

export const createClassgroup = async (classGroup: ClassGroup) => {
  await createStudentsFromList(classGroup.students);
  const studentIds = classGroup.students.map(student => student.studentNumber);

  const newClassGroup = {
    name: classGroup.name,
    student_ids: studentIds
  }

  console.log(newClassGroup)

  const response = await instance.post('/classgroups/', newClassGroup)


  if(response.status === 201) {
    return true
  }
  console.error(response.status + ": " + response.statusText);
  return false

}

export const getAllClassgroups = async (): Promise<ClassGroup[]> => {
  try {
    const { data } = await instance.get('/classgroups/');

    const classgroups: ClassGroup[] = data.items.map((classgroup: ClassGroupResponse) => {
      return {
        id: classgroup.id,
        name: classgroup.name
      };
    });

    return classgroups;
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
};


export const getClassgroupCount = async (): Promise<number> => {
  try {
    const { data } = await instance.get('/classgroups/');


    return data.total;
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
};

export const getClassgroupById = async (id: string): Promise<ClassGroup | null> => {
  try {
    const { data } = await instance.get(`/classgroups/${id}`);

    const classgroup: ClassGroup = {
      id: data.id,
      name: data.name,
      students: []
    };

    return classgroup;
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
}

/**
 * Retrieves a list of students from a specified class group.
 *
 * @param classGroupId - The ID of the class group.
 * @returns A promise that resolves to an array of students belonging to the class group.
 * @throws An error if the API request fails.
 */
export const getStudentsFromClassgroup = async (classGroupId: string): Promise<Student[]> => {
  try {
    let students: Student[] = []

    const { data } = await instance.get(`/classgroups/${classGroupId}/students/`)


    const pageStudents: Student[] = data.map((student: StudentResponse) => ({
      studentNumber: student.student_id,
      lastName: student.lastname,
      firstName: student.firstname,
      email: student.email,
      degreeProgramme: student.degree_programme,
    }))

    students = [...students, ...pageStudents]

    return students
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
};
