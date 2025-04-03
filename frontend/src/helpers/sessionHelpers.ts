import {instance} from '@/helpers/axiosHelpers';
import type { ClassSession } from '@/models/classSession';
import type { Device } from '@/models/device';
import type { SessionRequest } from '@/models/requests/sessionRequest';
import type { ClassSessionResponse } from '@/models/responses/classSessionResponse';
import type { DeviceResponse } from '@/models/responses/deviceResponse';

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



export const createSession = async (session: SessionRequest) => {
  try {
    console.log(session)
    await instance.post('/classsessions/', session);
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
}

export const getFullSession = async (id: string) => {
  try {
    const { data } = await instance.get(`/classsessions/${id}`);

    const session: ClassSession = {
      id: data.id,
      startTime: data.start_time,
      endTime: data.end_time,
      classgroupId: data.classgroup_id,
      roomDeviceId: data.room_device_id
    };

    return session;
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
}
