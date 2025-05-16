import {instance} from '@/helpers/axiosHelpers';
import type { Attendance } from '@/models/attendance';
import type { ClassGroup } from '@/models/classGroup';
import type { ClassSession } from '@/models/classSession';
import type { Device } from '@/models/device';
import type { FullClassSession } from '@/models/fullClassSession';
import type { SessionRequest } from '@/models/requests/sessionRequest';
import type { AttendanceResponse } from '@/models/responses/attendanceResponse';
import type { ClassSessionResponse } from '@/models/responses/classSessionResponse';
import type { DeviceResponse } from '@/models/responses/deviceResponse';
import type { StudentResponse } from '@/models/responses/studentResponse';

export const getSessionsOfRoomDevice = async (device_id: string) => {
  try {
    const { data } = await instance.get(`/roomdevices/${device_id}/sessions`);

    const sessions: ClassSession[] = data.class_sessions.map((session: ClassSessionResponse) => {
      return {
        id: session.id,
        startTime: session.start_time,
        endTime: session.end_time,
        classgroupId: session.classgroup_id,
        roomDeviceId: session.room_device_id
      };
    })

    return sessions;
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
}

export const getSessionsCount = async (): Promise<number> => {
  try {
    const { data } = await instance.get('/classsessions');


    return data.total;
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
};

export const getAllSessionsFromClassgroup = async (classgroupId: string) /*Promise<FullClassSession[]>*/ => {
  try {
    const { data } = await instance.get(`/classgroups/${classgroupId}/sessions`);


    console.log(data)

    const sessions: FullClassSession[] =
      data.map((session: any) => {
        console.log('group', session)
        return {
          classgroup: session.classgroup as ClassGroup,
          roomDevice: {
            id: session.room_device.id,
            roomName: session.room_device.room_name,
            deviceIdentifier: session.room_device.device_identifier
          } as Device,
          attendances: session.attendances.map((attendance: AttendanceResponse) => {
            return {
              id: attendance.id,
              studentId: attendance.student_id,
              timestamp: attendance.timestamp,
              classSessionId: attendance.class_session_id
            } as Attendance
          }),
          classgroupId: session.classgroup_id,
          endTime: session.end_time,
          startTime: session.start_time,
          id: session.id,
          roomDeviceId: session.room_device_id,
        } as FullClassSession
      })


    console.log('ses', sessions)
    return sessions;
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
};




export const createSession = async (session: SessionRequest) => {
  try {
    console.log(session)
    await instance.post('/classsessions', session);
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
}

  /**
   * Gets a full ClassSession object by its id. Includes: Room Device, Classgroup and Attendances
   *
   * @param id the id of the ClassSession
   * @returns a FullClassSession object
   * @throws an error if the API request fails
   */
export const getFullSession = async (id: string) => {
  try {
    const { data } = await instance.get(`/classsessions/${id}/full`);

    const session: FullClassSession = {
      id: data.id,
      startTime: data.start_time,
      endTime: data.end_time,
      classgroupId: data.classgroup_id,
      roomDeviceId: data.room_device_id,
      classgroup: data.classgroup as ClassGroup,
      roomDevice: {
        id: data.room_device.id,
        roomName: data.room_device.room_name,
        deviceIdentifier: data.room_device.device_identifier
      } as Device,
      attendances: data.attendances.map((attendance: AttendanceResponse) => {
        return {
          id: attendance.id,
          studentId: attendance.student_id,
          timestamp: attendance.timestamp,
          classSessionId: attendance.class_session_id
        } as Attendance
      })
    };

    return session;
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
}
