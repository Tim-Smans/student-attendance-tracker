import axios from 'axios';

const apiUrl = import.meta.env.VITE_BASE_URL;

export const instance = axios.create({
  baseURL: apiUrl,
  timeout: 1000,
  headers: {'x-api-key': `${import.meta.env.VITE_API_KEY}`}
});
