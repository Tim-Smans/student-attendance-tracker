import axios from 'axios';

export const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  timeout: 1000,
  headers: {'x-api-key': `${import.meta.env.VITE_API_KEY}`}
});
