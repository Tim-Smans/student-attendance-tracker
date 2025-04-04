import type { ClassGroup } from '@/models/classGroup';
import type { Student } from '@/models/student';
import { read, utils } from "xlsx";
import { v4 as uuidv4 } from 'uuid';

/**
 * Maps an Excel row to a Student object.
 */
const mapExcelRowToStudent = (row: any): Student => ({
  studentNumber: row["Op.num"]?.toString() || "",
  lastName: row["Sukunimi"] || "",
  firstName: row["Etunimi"] || "",
  fullName: row["Nimi"] || "",
  email: row["Email"] || "",
  personalEmail: row["Koti kk. Email"] || "",
  arrivalGroup: row["Saapumisyhmä"] || "",
  administrativeGroup: row["Hall.ryhmät"] || "",
  degreeProgramme: row["Ohjelma"] || "",
  formOfEducation: row["Koulutusmuoto"] || "",
  enrollment: row["Ilmoittautuminen"] || "",
  assessment: row["Arviointi"] || "",
});

  /**
   * Reads an Excel file, creates a ClassGroup out of the data, and returns it.
   *
   * The function first reads the Excel file, then takes the first non-empty cell
   * of the first row as the title of the ClassGroup.
   *
   * Then, it maps the rest of the rows of the sheet to Student objects, using
   * the mapExcelRowToStudent function.
   *
   * Finally, it creates a ClassGroup object with the title and the students,
   * and returns it.
   *
   * @param file the Excel file to read
   * @returns a ClassGroup object
   */
export const readExcelFile = async (file: File): Promise<ClassGroup> => {
  const arrayBuffer = await file.arrayBuffer();
  const workbook = read(arrayBuffer, { type: "array" });
  const sheet = workbook.Sheets[workbook.SheetNames[0]];

  const titleRow = utils.sheet_to_json(sheet, {
    header: 1,
    range: "A1:Z1",
    defval: ""
  }) as string[][];

  const title = titleRow[0]?.find(cell => cell && cell.trim() !== "") || "Naamloos";

  const rawData = utils.sheet_to_json(sheet, {
    range: 1,
    defval: ""
  });

  const students: Student[] = rawData.map((row: any) => mapExcelRowToStudent(row));

  const classGroup: ClassGroup = {
    id: uuidv4(),
    name: title,
    students
  };

  return classGroup;
};
