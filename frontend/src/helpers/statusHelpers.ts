import { instance } from './axiosHelpers';

export const isDeviceOnline = async (piId: string): Promise<boolean> => {
  try {
    const { data } = await instance.get(`/status/is_online/${piId}/`);

    console.log(data)
    return data.online;
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
};

