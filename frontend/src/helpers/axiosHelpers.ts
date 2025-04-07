import axios from 'axios';


export const instance = axios.create({
  baseURL: 'https://student-attendance-tracker-ungw.onrender.com',
  timeout: 1000,
  headers: {'x-api-key': `${import.meta.env.VITE_API_KEY}`}
});
