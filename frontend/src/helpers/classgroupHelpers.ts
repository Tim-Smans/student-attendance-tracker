import type { ClassGroup } from '@/models/classGroup';
import axios, { type AxiosResponse } from 'axios';
import { createStudentsFromList } from './studentHelpers';
import { instance } from './axiosHelpers';
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

export const getStudentsFromClassgroup = async (classGroupId: string): Promise<Student[]> => {
  try {
    const { data } = await instance.get(`/classgroups/${classGroupId}/students/`);

    const students: Student[] = data.items.map((student: StudentResponse) => {
      return {
        studentNumber: student.student_id,
        lastName: student.lastname,
        firstName: student.firstname,
        email: student.email,
        degreeProgramme: student.degree_programme,
      };
    });

    return students;
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
};
