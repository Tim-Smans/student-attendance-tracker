import type { ClassGroup } from '@/models/classGroup';
import axios from 'axios';
import { createStudentsFromList } from './studentHelpers';
import { instance } from './axiosHelpers';

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
