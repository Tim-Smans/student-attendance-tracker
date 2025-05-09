import type { ClassGroup } from '@/models/classGroup';
import type { Student } from '@/models/student';
import { read, utils, type WorkBook } from "xlsx";
import * as ExcelJS from "exceljs"
import { v4 as uuidv4 } from 'uuid';
import type { FullClassSession } from '@/models/fullClassSession';
import { getStudentsFromClassgroup } from './classgroupHelpers';

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


export const createWorkbook = async (session: FullClassSession[]) =>{
  const workbook = new ExcelJS.Workbook();
  const workbookWithSheets = await createSessionSheet(workbook, session)

  if(workbookWithSheets == null){
    throw Error('No valid workbook created!')
  }

  await createDocument(workbookWithSheets)
}

const createSessionSheet = async (workbook: ExcelJS.Workbook, sessions: FullClassSession[]): Promise<ExcelJS.Workbook | null> => {
  if(sessions.length == 0) {
    return null
  }

  console.log(sessions)

  const students = await getStudentsFromClassgroup(sessions[0].classgroupId)

  sessions.forEach(session => {

    const attendedStudentIds = new Set(
      session.attendances
        .filter(x => x.classSessionId === session.id)
        .map(x => x.studentId)
    );

    const sheetName = session.id
    const worksheet = workbook.addWorksheet(sheetName);
    worksheet.addRow([`Session from: ${session.startTime} to ${session.endTime}`])
    worksheet.addRow([`Classgroup: ${session.classgroup.name}`])
    worksheet.addRow([''])

    // Voeg headers toe
    worksheet.addRow(['Student number', 'Last name', 'First name', 'Email', 'Degree programme', 'Attendance']);

    // Voeg studenten toe
    students.forEach(x => {
      const row = worksheet.addRow([
        x.studentNumber,
        x.lastName,
        x.firstName,
        x.email,
        x.degreeProgramme,
        attendedStudentIds.has(x.studentNumber) ? 'Attended' : 'Absent'
      ]);

      if (attendedStudentIds.has(x.studentNumber)) {
        row.eachCell(cell => {
          cell.fill = {
            type: 'pattern',
            pattern: 'solid',
            fgColor: { argb: 'FFCCFFCC' } // Licht green
          };
        });
      }
    });
  });


  // Write the file to download in browser
  return workbook
}


const createDocument = async (workbook: ExcelJS.Workbook) => {
  const buffer = await workbook.xlsx.writeBuffer();
  const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'attendance.xlsx';
  link.click();
}
