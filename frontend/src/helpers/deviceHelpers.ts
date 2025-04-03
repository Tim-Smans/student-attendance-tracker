import {instance} from '@/helpers/axiosHelpers';
import type { Device } from '@/models/device';
import type { DeviceResponse } from '@/models/responses/deviceResponse';

export const getDevices = async () => {
  try {
    const { data } = await instance.get('/roomdevices/?page=1&limit=100');

    const devices: Device[] = data.items.map((device: DeviceResponse) => {
      return {
        id: device.id,
        roomName: device.room_name,
        deviceIdentifier: device.device_identifier
      };
    })

    return devices;
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
}
