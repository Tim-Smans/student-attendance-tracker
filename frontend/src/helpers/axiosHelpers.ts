import axios from 'axios';

const apiUrl = "https://tracker.timsmans.be/api";

export const instance = axios.create({
  baseURL: apiUrl,
  timeout: 1000,
  headers: {'x-api-key': `${import.meta.env.VITE_API_KEY}`}
});
